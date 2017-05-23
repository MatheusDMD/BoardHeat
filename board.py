"""Calc temperature on 1d bar."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Board:
    def __init__(self, file_name):
        self.d = self.import_file(file_name)
        self.fourier_number = self.calc_fourier_number()
        self.board = self.create_board()
        self.im = plt.imshow(self.board, animated=True, cmap=plt.get_cmap('magma'))

    def calc_fourier_number(self):
        """Calc lambda constant."""
        return self.d["alpha"] * (self.d["d_t"] / ((self.d["d_x"]) ** 2))


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
        return list_main
        
    def get_temps_in_time(self):
        """Calc temperatures on bar on time."""
        list_current = [x[:] for x in self.board]
        for p in range(self.d["t"]):
            for i in range(0, self.d["row"]):
                for j in range(0, self.d["col"]):
                    list_current[i][j] = self.calc_item(self.board, i, j, self.fourier_number)
            self.board = [x[:] for x in list_current]
        return list_current
    
    def __updatefig(*args):
        """Calc temperatures on bar on time."""
        list_current = [x[:] for x in self.board]
        for i in range(0, self.d["row"]):
            for j in range(0, self.d["col"]):
                list_current[i][j] = self.calc_item(self.board, i, j, self.fourier_number)
        self.board = [x[:] for x in list_current]
        self.im.set_array(np.array(list_current))

    def valid_fn(self):
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
        ani = animation.FuncAnimation(fig, self.__updatefig, interval=10)
        plt.colorbar()
        plt.show()

    def calc_item(self, i, j):
        """Calc temp to item."""
        blocked = [(0, 0), (self.d["col"] - 1, self.d["row"] - 1), (self.d["col"] - 1, 0), (0, self.d["row"] - 1)]
        if (i,j) in blocked:
            return self.board[i][j]
        if (i == (self.d["row"] - 1) ):
            if ("flux_bottom" in d):
                return self.fourir_number*(2*self.board[i - 1][j]
                                + self.board[i][j + 1]
                                - 2*self.d["d_x"]*self.d["flux_bottom"]
                                + self.board[i][j - 1]) + ((1 - 4 * self.fourir_number) * self.board[i][j])
            else:
                return self.board[i][j]
        elif ((j == 0) ):
            if ("flux_left" in d):
                return self.fourir_number*(self.board[i - 1][j]
                                + 2*self.board[i][j + 1]
                                + self.board[i + 1][j]
                                - 2*self.d["d_x"]*self.d["flux_left"]
                                + ((1 - 4 * self.fourir_number) * self.board[i][j]))
            else:
                return self.board[i][j]
        elif (j == (self.d["col"] - 1)):
            if ("flux_right" in d):
                return self.fourir_number*(self.board[i - 1][j]
                                + self.board[i + 1][j]
                                + 2*self.board[i][j - 1]
                                - 2*self.d["d_x"]*self.d["flux_right"]
                                + ((1 - 4 * self.fourir_number) * self.board[i][j]))
            else:
                return self.board[i][j]
        elif ((i == 0)):
            if ("flux_top" in d):
                return self.fourir_number*(2*self.board[i + 1][j]
                                + self.board[i][j + 1]
                                + self.board[i][j - 1]
                                - 2*self.d["d_x"]*self.d["flux_top"]
                                + ((1 - 4 * self.fourir_number) * self.board[i][j]))
            else:
                return self.board[i][j]
        else:
            return self.fourir_number*(self.board[i + 1][j]
                            + self.board[i - 1][j]
                            + self.board[i][j + 1]
                            + self.board[i][j - 1]) + ((1 - 4 * self.fourir_number) * self.board[i][j])
