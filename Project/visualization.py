import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ReportGenerator:
    def __init__(self, df, analyzer):
        self.df = df
        self.analyzer = analyzer
    
    def create_text_report(self):
        report = []
        report.append("\nDATA ANALYSIS REPORT")
        report.append("-" * 60)
        
        summary = self.analyzer.get_summary_report()
        
        report.append("\nEXECUTIVE SUMMARY")
        report.append("-" * 50)
        report.append(f"Total Records: {summary['total_records']:,}")
        report.append(f"Total Revenue: ${summary['total_revenue']:,.2f}")
        report.append(f"Average Order Value: ${summary['avg_order_value']:,.2f}")
        report.append(f"Unique Customers: {summary['unique_customers']:,}")
        report.append(f"Categories: {summary['unique_categories']}")
        report.append(f"Regions: {summary['unique_regions']}")
        
        # Basic Statistics
        report.append("\nREVENUE STATISTICS")
        report.append("-" * 50)
        stats = summary['insights']['basic_stats']['revenue']
        report.append(f"Mean: ${stats['mean']:,.2f}")
        report.append(f"Median: ${stats['median']:,.2f}")
        report.append(f"Std Dev: ${stats['std']:,.2f}")
        report.append(f"Min: ${stats['min']:,.2f}")
        report.append(f"Max: ${stats['max']:,.2f}")
        
        # Category Performance
        report.append("\nTOP CATEGORIES BY REVENUE")
        report.append("-" * 50)
        category_stats = self.analyzer.category_analysis()
        for idx, (cat, row) in enumerate(category_stats.head(5).iterrows(), 1):
            report.append(f"{idx}. {cat}: ${row['Total_Revenue']:,.2f} ({int(row['Count'])} orders)")
        
        # Regional Performance
        report.append("\nREGIONAL PERFORMANCE")
        report.append("-" * 50)
        regional_stats = self.analyzer.regional_analysis()
        for region, row in regional_stats.iterrows():
            report.append(f"{region}: ${row['Total_Revenue']:,.2f} ({int(row['Unique_Customers'])} customers)")
        
        
        report.append("\nTOP 5 CUSTOMERS")
        report.append("-" * 50)
        customer_stats = self.analyzer.customer_analysis()
        for idx, (cust_id, row) in enumerate(customer_stats.head(5).iterrows(), 1):
            report.append(f"{idx}. Customer {cust_id}: ${row['Total_Spent']:,.2f} ({int(row['Num_Purchases'])} purchases)")
        
        report.append("\n" + "-" * 60)
        
        return "\n".join(report)
    
    def create_visualizations(self, output_file='analysis_report.png'):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Sales Data Analysis Dashboard', fontsize=16, fontweight='bold')
        
        
        category_stats = self.analyzer.category_analysis()
        axes[0, 0].bar(category_stats.index, category_stats['Total_Revenue'], color='steelblue')
        axes[0, 0].set_title('Revenue by Category', fontweight='bold')
        axes[0, 0].set_ylabel('Revenue ($)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        
        regional_stats = self.analyzer.regional_analysis()
        axes[0, 1].pie(regional_stats['Total_Revenue'], labels=regional_stats.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Revenue Distribution by Region', fontweight='bold')
        
        
        monthly_trend = self.analyzer.temporal_analysis()
        axes[1, 0].plot(range(len(monthly_trend)), monthly_trend['Monthly_Revenue'], marker='o', linewidth=2, color='green')
        axes[1, 0].set_title('Monthly Revenue Trend', fontweight='bold')
        axes[1, 0].set_ylabel('Revenue ($)')
        axes[1, 0].set_xlabel('Month')
        axes[1, 0].grid(True, alpha=0.3)
        
        
        quantity_by_cat = self.df.groupby('category')['quantity'].sum()
        axes[1, 1].barh(quantity_by_cat.index, quantity_by_cat.values, color='coral')
        axes[1, 1].set_title('Quantity Sold by Category', fontweight='bold')
        axes[1, 1].set_xlabel('Quantity')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved to '{output_file}'")
        plt.close()
    
    def print_report(self):
        print(self.create_text_report())