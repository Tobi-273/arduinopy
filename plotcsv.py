"""Functions for choosing a file and for 2D-plotting by selecting two columns of a .csv file"""

import pandas as pd
import plotly.express as px
import tkinter as tk
from tkinter import filedialog


def plot_from_csv(file, x='Timestamp', y='Value', title='Measurements'):
    """Plots a 2D-graph and shows it.
    Expects a file path, names of two columns for the kwargs x, y and a headline for the kwarg title"""
    df = pd.read_csv(file)
    fig = px.line(df, x=x, y=y, title=title)
    fig.show()


def choose():
    """Opens system dialog for choosing a file and returns its path"""
    root = tk.Tk()
    root.withdraw()
    file_path = tk.filedialog.askopenfilename()
    return file_path


def choose_and_plot(x='Timestamp', y='Value', title='Measurements'):
    """Lets you choose a file and plots it.
    Expects the same kwargs as plot_from_file, see docstring"""
    file_path = choose()
    plot_from_csv(file_path, x=x, y=y, title=title)


choose_and_plot(title='Messwerte')
