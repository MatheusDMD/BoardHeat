from board import Board
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def main():
    board = Board("info.txt")
    board.plot_animated()

main()