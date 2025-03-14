import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
def fa(x = 1, y = 1, size = (7,7)):
    return plt.subplots(x,y,figsize = size)

class Visualiser:

    def __init__(self, path: str):
        self.data = pd.read_csv(path, delimiter = ';')
        self.products = self.data["product"].unique()
    
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
    
    def get_products_all(self):
        return self.data["product"].unique()

    def get_products(self):
        return self.products
    
    def set_products(self, products: list):
        self.products = products

    def plot_price(self, together: str = "N"):

        # Column groups
        price_columns = ["bid_price_1", "bid_price_2", "bid_price_3"]
        volume_columns = ["bid_volume_1", "bid_volume_2", "bid_volume_3"]

        # Dictionary to store weighted average prices per product
        product_weighted_avg_prices = {}

        for product in self.products:
            product_data = self.data[self.data["product"] == product] 

            weighted_price = sum(product_data[price] * product_data[volume] for price, volume in zip(price_columns, volume_columns))
            total_volume = product_data[volume_columns].sum(axis=1)

            weighted_avg_price = weighted_price / total_volume

            # Fill missing values forward (to handle missing timestamps)
            weighted_avg_price_filled = weighted_avg_price.fillna(method="ffill")

            product_weighted_avg_prices[product] = weighted_avg_price_filled

        # PLOTTING: Based on User Choice (Y means together, N means seperate)
        if together == "Y":
            # Plot all products on the same graph
            plt.figure(figsize=(12, 6))
            
            for product, weighted_avg_price in product_weighted_avg_prices.items():
                product_data = self.data[self.data["product"] == product]
                plt.plot(product_data["timestamp"], weighted_avg_price, label=product)

            # Formatting
            plt.xlabel("Timestamp")
            plt.ylabel("Weighted Avg Price")
            plt.title("Weighted Avg Price of Selected Products")
            plt.xticks(rotation=45)
            plt.legend()
            plt.grid(True)

            plt.show()

        else:
            # Plot each product separately
            num_products = len(product_weighted_avg_prices)
            fig, axes = plt.subplots(num_products, 1, figsize=(6 * num_products, 10), sharey=False)  # Separate y-scales

            # If only one product is selected, convert axes to a list for consistency
            if num_products == 1:
                axes = [axes]

            # Loop through each product and create a separate subplot
            for ax, (product, weighted_avg_price) in zip(axes, product_weighted_avg_prices.items()):
                product_data = self.data[self.data["product"] == product]
                ax.plot(product_data["timestamp"], weighted_avg_price, label=product)

                # Formatting for each subplot
                ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

                ax.set_xlabel("Timestamp")
                ax.set_ylabel("Weighted Avg Price")
                ax.set_title(f"Weighted Avg Price of {product}")
                ax.legend()
                ax.grid(True)
                
                ax.tick_params(axis='x', rotation=45)

            plt.tight_layout()
            plt.show()
