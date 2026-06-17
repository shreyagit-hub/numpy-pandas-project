import numpy as np
import pandas as pd

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
        self.insights = {}
    
    def basic_statistics(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        stats = {}

        for col in numeric_cols:
            stats[col] = {
                'mean': float(self.df[col].mean()),
                'std': float(self.df[col].std()),
                'max': float(self.df[col].max()),
                'q75': float(self.df[col].quantile(0.75)),
            }

        self.insights['basic_statistics'] = stats
    
        return self.insights
    
    def category_analysis(self):
        category_stats = self.df.groupby('category').agg({
            'revenue': ['sum', 'mean', 'count'],
            'quantity': 'sum',
            'profit': 'sum',
        }).round(2)

        category_stats.columns = ['Total_Revenue', 'Avg_Revenue', 'Count', 'Total_Qty', 'Total_Profit']
        category_stats['Profit_Margin'] = (
            (category_stats['Total_Profit'] / category_stats['Total_Revenue'] * 100)
            .round(2)
        )

        self.insights['category_stats'] = category_stats
        return category_stats.sort_values('Total_Revenue', ascending=False)
    
    def regional_analysis(self):
        regional_stats = self.df.groupby('region').agg({
            'revenue': ['sum', 'mean'],
            'quantity': 'sum',
            'customer_id': 'nunique',
        }).round(2)

        regional_stats.columns = ['Total_Revenue', 'Avg_Revenue', 'Total_Qty', 'Unique_Customers']

        self.insights['regional_stats'] = regional_stats
        return regional_stats
    
    def temporal_analysis(self):
        self.df['year_month'] = self.df['date'].dt.to_period('M')

        monthly_trend = self.df.groupby('year_month').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'customer_id': 'nunique',
        }).round(2)

        monthly_trend.columns = ['Monthly_Revenue', 'Monthly_Qty', 'Unique_Customers']

        self.insights['temporal_stats'] = monthly_trend
        return monthly_trend
    
    def customer_analysis(self):
        customer_stats = self.df.groupby('customer_id').agg({
            'revenue': ['sum', 'count', 'mean'],
            'quantity': 'sum',
        }).round(2)

        customer_stats.columns = ['Total_Spent', 'Num_Purchases', 'Avg_Purchase', 'Total_Items']
        customer_stats = customer_stats.sort_values('Total_Spent', ascending=False)

        # Calculate percentiles
        percentiles = {
            'top_10_percent': customer_stats['Total_Spent'].quantile(0.90),
            'top_25_percent': customer_stats['Total_Spent'].quantile(0.75),
            'median': customer_stats['Total_Spent'].median(),
        }

        self.insights['customer_stats'] = customer_stats
        self.insights['customer_percentiles'] = percentiles
        return customer_stats.head(10)
    
    def correlation_analysis(self):
        numeric_df = self.df.select_dtypes(include=[np.number])
        correlation = numeric_df.corr().round(3)

        self.insights['correlation'] = correlation
        return correlation
    
    def get_summary_report(self):
        return {
            'total_records': len(self.df),
            'total_revenue': float(self.df['revenue'].sum()),
            'avg_order_value': float(self.df['revenue'].mean()),
            'unique_customers': int(self.df['customer_id'].nunique()),
            'unique_categories': int(self.df['category'].nunique()),
            'unique_regions': int(self.df['region'].nunique()),
            'insights': self.insights,
        }
