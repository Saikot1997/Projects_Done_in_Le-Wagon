import pandas as pd
import numpy as np
from olist.data import Olist


class OlistAnalysis:
    def __init__(self):
        self.data = Olist().get_data()
        self.it_costs = 50000  # initial IT costs
        self.profit = self.compute_profit()

    def remove_sellers(self, sellers_to_remove):
        """
        Update IT costs after removing sellers and their products
        """
        # Find products to remove
        products_to_remove = self.data['order_items'].loc[
            self.data['order_items']['seller_id'].isin(sellers_to_remove), 'product_id'
        ].unique()

        # Compute IT cost impact
        it_cost_impact = len(products_to_remove) * 100

        # Update IT costs and profit
        self.it_costs -= it_cost_impact
        self.profit = self.compute_profit()

    def compute_profit(self):
        """
        Compute Olist global profit
        """
        # Compute revenue
        revenue = self.data['order_items']['price'].sum()

        # Compute costs
        costs = self.data['order_items']['price'].sum() * 0.8 + self.it_costs

        # Compute profit
        profit = revenue - costs

        return profit
