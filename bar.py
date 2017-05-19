"""Calc temperature on 1d bar."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


""" Global variables """
d = {}
list_prev = []
mult_lambda = 0
im = 0

def import_file(file_name):
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


def calc_item(list_prev, i, j, mult_lambda):
    """Calc temp to item."""
    blocked = [(0, 0), (d["col"] - 1, d["row"] - 1), (d["col"] - 1, 0), (0, d["row"] - 1)]
    if (i,j) in blocked:
        return list_prev[i][j]
    if (i == (d["row"] - 1) ):
        if ("flux_bottom" in d):
            return mult_lambda*(2*list_prev[i - 1][j]
                            + list_prev[i][j + 1]
                            - 2*d["d_x"]*d["flux_bottom"]
                            + list_prev[i][j - 1]) + ((1 - 4 * mult_lambda) * list_prev[i][j])
        else:
            return list_prev[i][j]
    elif ((j == 0) ):
        if ("flux_left" in d):
            return mult_lambda*(list_prev[i - 1][j]
                            + 2*list_prev[i][j + 1]
                            + list_prev[i + 1][j]
                            - 2*d["d_x"]*d["flux_left"]
                            + ((1 - 4 * mult_lambda) * list_prev[i][j]))
        else:
            return list_prev[i][j]
    elif (j == (d["col"] - 1)):
        if ("flux_right" in d):
            return mult_lambda*(list_prev[i - 1][j]
                            + list_prev[i + 1][j]
                            + 2*list_prev[i][j - 1]
                            - 2*d["d_x"]*d["flux_right"]
                            + ((1 - 4 * mult_lambda) * list_prev[i][j]))
        else:
            return list_prev[i][j]
    elif ((i == 0)):
        if ("flux_top" in d):
            return mult_lambda*(2*list_prev[i + 1][j]
                            + list_prev[i][j + 1]
                            + list_prev[i][j - 1]
                            - 2*d["d_x"]*d["flux_top"]
                            + ((1 - 4 * mult_lambda) * list_prev[i][j]))
        else:
            return list_prev[i][j]
    else:
        return mult_lambda*(list_prev[i + 1][j]
                        + list_prev[i - 1][j]
                        + list_prev[i][j + 1]
                        + list_prev[i][j - 1]) + ((1 - 4 * mult_lambda) * list_prev[i][j])


def create_bar(temp_top,
               temp_bottom,
               temp_left,
               temp_right,
               temp_init,
               col,
               row):
    """Create init bar."""
    list_main = [[temp_init]*(col)]*(row)
    list_main[0] = [temp_top] * (col)
    list_main[-1] = [temp_bottom] * (col)
    for i in range(row):
        list_main[i][0] = temp_left
        list_main[i][-1] = temp_right
    return list_main

def get_temps_in_time(list_prev, time, mult_lambda, row, col):
    """Calc temperatures on bar on time."""
    list_current = [x[:] for x in list_prev]
    for p in range(time):
        for i in range(0, row):
            for j in range(0, col):
                list_current[i][j] = calc_item(list_prev, i, j, mult_lambda)
        list_prev = [x[:] for x in list_current]
    return list_current

def updatefig(*args):
    """Calc temperatures on bar on time."""
    global d, list_prev, im, mult_lambda
    list_current = [x[:] for x in list_prev]
    for i in range(0, d["row"]):
        for j in range(0, d["col"]):
            list_current[i][j] = calc_item(list_prev, i, j, mult_lambda)
    list_prev = [x[:] for x in list_current]
    im.set_array(np.array(list_current))
    return im


def calc_mult_lambda(alpha, d_x, d_t):
    """Calc lambda constant."""
    return alpha * (d_t / ((d_x) ** 2))


def plot_color_gradients(gradient):
    """Plot color gradients."""
    gradient = np.array(gradient)
    gradient = np.delete(gradient, [0, len(gradient)], 0)
    gradient = np.delete(gradient, [0, len(gradient)], 1)
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.9, bottom=0, left=0, right=0.99)
    ax.set_title('Titulo', fontsize=14)
    ax.imshow(gradient, aspect='equal', cmap=plt.get_cmap('magma'))
    ax.set_axis_off()


def main():
    """Main func."""
    global d, mult_lambda, im, list_prev
    d = import_file("info.txt")
    mult_lambda = calc_mult_lambda(d["alpha"], d["d_x"], d["d_t"])
    if (mult_lambda > 0.25):
        print("Fourier Number is {0}, we don't ensure that your simulation converges.".format(fourier_number))
        return
    d["row"] = int( d["row_size"]/d["d_x"])
    d["col"] = int( d["col_size"]/d["d_x"])
    print(d["row"])
    list_prev = create_bar(d["temp_top"],
                           d["temp_bottom"],
                           d["temp_left"],
                           d["temp_right"],
                           d["temp_init"],
                           d["col"],
                           d["row"])

    # list_current = get_temps_in_time(list_prev, d["t"], mult_lambda, d["row"], d["col"])
    # for i in range(d["col"]):
    #     print(list_current[i])
    # plot_color_gradients(list_current)
    # plt.show()
    if  mult_lambda < 0.25:
        fig = plt.figure()
        im = plt.imshow(list_prev, animated=True, cmap=plt.get_cmap('magma'))
        ani = animation.FuncAnimation(fig, updatefig, interval=10)
        plt.colorbar()
        plt.show()
    else:
        print("Lambda too high to calculate: {0}.".format(mult_lambda))
        print("Equation for lambda: alpha * (d_t / ((d_x) ** 2))")
        print("must be lower than 0.25")

if __name__ == "__main__":
    main()
