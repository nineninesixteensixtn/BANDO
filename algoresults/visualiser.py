import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Visualiser:
    def __init__(self, path):
        self.data = pd.read_csv(path, delimiter = ';')
    