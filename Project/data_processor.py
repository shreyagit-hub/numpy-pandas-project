import numpy as np
import pandas as pd


class DataProcessor:
    def __init__(self, df):
        self.df = df.copy()
        self.original_shape = df.shape
    
    def handle_missing_values(self, strategy='forward_fill'):
        if strategy == 'forward_fill':
            self.df['price'] = self.df['price'].fillna(method='ffill').fillna(method='bfill')
        elif strategy == 'backward_fill':
            self.df['price'] = self.df['price'].fillna(method='bfill').fillna(method='ffill')
        elif strategy == 'mean':
            self.df['price'] = self.df['price'].fillna(self.df['price'].mean())
        
        return self
    
    def add_derived_features(self):
        # Extract date components 
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        self.df['quarter'] = self.df['date'].dt.quarter
        
        # Create price bins
        self.df['price_category'] = pd.cut(
            self.df['price'],
            bins=[0, 50, 150, 300, 500],
            labels=['Budget', 'Standard', 'Premium', 'Luxury']
        )
        
        # Calculate profit 
        self.df['profit'] = self.df['revenue'] * 0.30
        
        return self
    
    def normalize_columns(self, columns=None):
        if columns is None:
            columns = ['quantity', 'price', 'revenue']
        
        for col in columns:
            if col in self.df.columns:
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                self.df[f'{col}_normalized'] = (self.df[col] - min_val) / (max_val - min_val)
        
        return self
    
    def remove_outliers(self, column='revenue', threshold=3):
        z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
        self.df = self.df[z_scores < threshold]
        
        return self
    
    def get_summary(self):
        return {
            'original_rows': self.original_shape[0],
            'current_rows': self.df.shape[0],
            'rows_removed': self.original_shape[0] - self.df.shape[0],
            'missing_values': self.df.isnull().sum().sum(),
        }
    
    def get_dataframe(self):
        return self.df