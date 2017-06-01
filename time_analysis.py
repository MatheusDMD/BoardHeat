from board import Board
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def main():
    board = Board("board.in")
    #board.plot_animated()
    list_current = board.get_temps_in_time()
    if (list_current):
        for i in range(len(list_current)):
            print(list_current[i])

main()
