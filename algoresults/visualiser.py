import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


class Visualiser:

    def __init__(self, path: str):
        self.data = pd.read_csv(path, delimiter = ';')
        self.products = self.data["product"].unique()
    
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