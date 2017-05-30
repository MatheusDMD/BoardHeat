from __future__ import print_function
# -*- coding: utf-8 -*-
__author__  = "Felipe Buniac, Marcelo Andrade, Matheus Marotzke, Rafael Molines"
__copyright__ = "Copyright 2017, " + __author__
__license__ = "GPLv3.0"

from board import Board
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from prettytable import PrettyTable
import sys, getopt

def main(argv):
    inputfile = ''
    plot = False
    try:
        opts, args = getopt.getopt(argv,"ti:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('usage: boardheat.py -i <inputfile>\n')
        print ('   -i             input file path')
        print ('   -t             plot in time\n')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('\nboardheat.py -i <inputfile>\n')
            print ('   -i             input file path')
            print ('   -t             plot in time\n')
            sys.exit()
        elif opt == '-t':
            plot = True
        elif opt in ("-i", "--ifile"):
            inputfile = arg

    truss_main(inputfile, plot)

def truss_main(inputfile, plot):
    board = Board(inputfile)
    if(board.good_to_go):
        if plot:
            board.plot_animated()
        else:
            board = board.get_temps_in_time()
            t = PrettyTable([x for x in range(len(board))])
            for item in board:
                t.add_row(["{0:.2f}".format(a) for a in item])
            print(t)


if __name__ == "__main__":
    main(sys.argv[1:])
