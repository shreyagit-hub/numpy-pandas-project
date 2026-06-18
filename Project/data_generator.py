import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_sales_data(n_records=1000, seed=42):
    np.random.seed(seed)
    
    categories = ['Electronics', 'Clothing', 'Food', 'Home', 'Sports']
    regions = ['North', 'South', 'East', 'West']
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=int(x)) for x in np.random.randint(0, 365, n_records)]
    
    data = {
        'date': dates,
        'category': np.random.choice(categories, n_records),
        'region': np.random.choice(regions, n_records),
        'quantity': np.random.randint(1, 20, n_records),
        'price': np.random.uniform(10, 500, n_records),
        'customer_id': np.random.randint(1000, 1500, n_records),
    }
    
    df = pd.DataFrame(data)
    
    
    df['revenue'] = df['quantity'] * df['price']
    
    missing_indices = np.random.choice(df.index, size=int(0.1 * len(df)), replace=False)
    df.loc[missing_indices, 'price'] = np.nan
    
    return df.sort_values('date').reset_index(drop=True)


if __name__ == '__main__':
    df = generate_sales_data()
    print("Sample Data:")
    print(df.head(10))
    print(f"\nDataset Shape: {df.shape}")
    print(f"Missing Values:\n{df.isnull().sum()}")