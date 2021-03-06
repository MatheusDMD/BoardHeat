"""Calc temperature on 1d bar."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Board:
    def __init__(self, file_name):
        self.d = self.import_file(file_name)
        self.fourier_number = self.calc_fourier_number()
        self.error = 9223372036854775807
        self.board = self.create_board()
        #self.im = plt.imshow(self.board, animated=True, cmap=plt.get_cmap('magma'))
        if(self.fourier_number != "ERROR"):
            self.board = self.create_board()
            self.good_to_go = True
        else:
            self.good_to_go = False

    def calc_fourier_number(self):
        """Calc lambda constant."""
        if "alpha" in self.d:
            if "conductivity" in self.d or "specific_heat" in self.d or "conductivity" in self.d:
                print("Both: Thermal diffusivity and" +
                      "(Conductivity or Specific heat capacity or Density)\n" +
                      "Please only declare one of both")
                return "ERROR"
            else:
                return self.d["alpha"] * (self.d["d_t"] / ((self.d["d_x"]) ** 2))
        else:
            if "conductivity" in self.d and "specific_heat" in self.d and "density" in self.d:
                self.d["alpha"] = self.d["conductivity"]/(self.d["specific_heat"]*self.d["density"])
                return self.d["alpha"] * (self.d["d_t"] / ((self.d["d_x"]) ** 2))
            else:
                print("This specific values aren't declared:")
                if "conductivity" not in self.d:
                    print("Conductivity")
                if "specific_heat" not in self.d:
                    print("Specific heat")
                if "density" not in self.d:
                    print("Density")
                return "ERROR"


    def import_file(self, file_name):
        """Reads information from file."""
        with open(file_name) as f:
            content = f.readlines()
            content = [x.strip().split(" ") for x in content]
            for i in range(0,len(content)):
                if("." in content[i][1]):
                    content[i][1] = float(content[i][1])
                else:
                    content[i][1] = int(content[i][1])
            return dict(content)

    def create_board(self):
        """Create init bar."""
        self.d["row"] = int(self.d["row_size"] / self.d["d_x"])
        self.d["col"] = int(self.d["col_size"] / self.d["d_x"])
        list_main = [[self.d["temp_init"]]*(self.d["col"])]*(self.d["row"])
        list_main[0] = [self.d["temp_top"]] * (self.d["col"])
        list_main[-1] = [self.d["temp_bottom"]] * (self.d["col"])
        for i in range(self.d["row"]):
            list_main[i][0] = self.d["temp_left"]
            list_main[i][-1] = self.d["temp_right"]
        if "flux_left" in self.d:
            list_main[0][0] = self.d["temp_top"]
            list_main[-1][0] = self.d["temp_bottom"]
        if "flux_right" in self.d:
            list_main[0][-1] = self.d["temp_top"]
            list_main[-1][-1] = self.d["temp_bottom"]
        return list_main

    def get_temps_in_time(self):
        if (not self.valid_fn()):
            return None
        """Calc temperatures on bar on time."""
        list_current = [x[:] for x in self.board]
        for p in range(int(self.d["t"] / self.d["d_t"])):
            error = 0
            for i in range(0, self.d["row"]):
                for j in range(0, self.d["col"]):
                    list_current[i][j] = self.calc_item(i, j)
                    cur_error = abs(self.board[i][j] - list_current[i][j])
                    if cur_error > error:
                        error = cur_error
            if error < self.error:
                self.error = error
            if ("tolerance" in self.d):
                if (not self.check_tolerence()):
                    self.d["t"] = p 
                    print("The error has achieved the tolerence, T = {0}".format(p * self.d["d_t"]))
                    print("Error  = {0}".format(self.error))
                    return list_current
            self.board = [x[:] for x in list_current]
        print("\nTemperatures [C] after: " + str(self.d["t"]) + "s\n")
        print("Your error is {0}".format(self.error))
        return list_current

    def check_tolerence(self):
        if self.error < self.d["tolerance"]:
            return False
        else:
            return True

    def __updatefig(self, *args):
        """Calc temperatures on bar on time."""
        list_current = [x[:] for x in self.board]
        for i in range(0, self.d["row"]):
            for j in range(0, self.d["col"]):
                list_current[i][j] = self.calc_item(i, j)
        self.board = [x[:] for x in list_current]
        self.im.set_array(np.array(list_current))

    def valid_fn(self):
        print("Your fourier number is: {0}".format(self.fourier_number))
        """Check valid fourier number."""
        if self.fourier_number < 0.25:
            return True
        else:
            print("Lambda too high to calculate: {0}.".format(self.fourier_number))
            print("Equation for lambda: alpha * (d_t / ((d_x) ** 2))")
            print("must be lower than 0.25")
            return False

    def plot_animated(self):
        if not self.valid_fn():
            return
        fig = plt.figure()
        self.im = plt.imshow(self.board, animated=True, cmap=plt.get_cmap('magma'))
        ani = animation.FuncAnimation(fig, self.__updatefig, interval=10)
        plt.title('Board Heat Tranfer')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel('Temperature [C]')
        plt.show()

    def calc_item(self, i, j):
        """Calc temp to item."""
        blocked = [(0, 0), (self.d["col"] - 1, self.d["row"] - 1), (self.d["col"] - 1, 0), (0, self.d["row"] - 1)]
        if (i,j) in blocked:
            return self.board[i][j]
        if (i == (self.d["row"] - 1) ):
            if ("flux_bottom" in self.d):
                return self.fourier_number*(2*self.board[i - 1][j]
                                + self.board[i][j + 1]
                                - 2*self.d["d_x"]*self.d["flux_bottom"]
                                + self.board[i][j - 1]) + ((1 - 4 * self.fourier_number) * self.board[i][j])
            else:
                return self.board[i][j]
        if ((j == 0) ):
            if ("flux_left" in self.d):
                return self.fourier_number*(self.board[i - 1][j]
                                + (2*self.board[i][j + 1])
                                + self.board[i + 1][j]
                                - (2*self.d["d_x"]*self.d["flux_left"])) + ((1 - 4 * self.fourier_number) * self.board[i][j])
            else:
                return self.board[i][j]
        if (j == (self.d["col"] - 1)):
            if ("flux_right" in self.d):
                return self.fourier_number*(self.board[i - 1][j]
                                + self.board[i + 1][j]
                                + 2*self.board[i][j - 1]
                                - 2*self.d["d_x"]*self.d["flux_right"]) + ((1 - 4 * self.fourier_number) * self.board[i][j])
            else:
                return self.board[i][j]
        if ((i == 0)):
            if ("flux_top" in self.d):
                return self.fourier_number*(2*self.board[i + 1][j]
                                + self.board[i][j + 1]
                                + self.board[i][j - 1]
                                - 2*self.d["d_x"]*self.d["flux_top"]) + ((1 - 4 * self.fourier_number) * self.board[i][j])
            else:
                return self.board[i][j]
        else:
            return self.fourier_number*(self.board[i + 1][j]
                            + self.board[i - 1][j]
                            + self.board[i][j + 1]
                            + self.board[i][j - 1]) + ((1 - 4 * self.fourier_number) * self.board[i][j])
