import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
def fa(x = 1, y = 1, size = (7,7)):
    return plt.subplots(x,y,figsize = size)

class Visualiser:
    def __init__(self, path):
        self.data = pd.read_csv(path, delimiter = ';')
    
    def pnl(self, products = None):
        '''
        plots the profit and loss of products given data log
        `products`:list of strings corresponding to products of interest'''
        data = self.data
        productsdf = data['product'].unique()
        if products == None:
            n = len(productsdf)
            if n>2:
                f,a = fa(x = 2, y = (n+1//2), size = (14,((n+1//2))*6))
                for i in range(n):
                    sns.lineplot(data = data[data['product'] == productsdf[i]][['timestamp', 'profit_and_loss']], x= 'timestamp', y='profit_and_loss', ax = a[i//2, i%2])
                    a[i//2, i%2].set_title(f'{productsdf[i]}')
                    a[i//2, i%2].grid()
            else:
                
                f,a = fa(x = 2, y = 1, size = (14,((n+1//2))*6))
                for i in range(n):
                    sns.lineplot(data = data[data['product'] == productsdf[i]][['timestamp', 'profit_and_loss']], x= 'timestamp', y='profit_and_loss', ax = a[i])
                    a[i].set_title(f'{productsdf[i]}')
                    a[i].grid()

        else:
            n = len(products)
            if n>2:
                f,a = fa(x = 2, y = (n+1)//2 + 1, size = (14,(n+1//2)*6))
                for i in range(n):
                    sns.lineplot(data = data[data['product'] == products[i]][['timestamp', 'profit_and_loss']], x= 'timestamp', y='profit_and_loss', ax = a[i//2, i%2])
                    a[i//2, i%2].set_title(f'{products[i]}')
                    a[i//2, i%2].grid()
            else:
                f,a = fa(x = 2, y = 1, size = (14,6))
                for i in range(n):
                    sns.lineplot(data = data[data['product'] == products[i]][['timestamp', 'profit_and_loss']], x= 'timestamp', y='profit_and_loss', ax = a[i])
                    a[i].set_title(f'{products[i]}')
                    a[i].grid()

        return f
            
