from data_generator import generate_sales_data
from data_processor import DataProcessor
from analysis import DataAnalyzer
from visualization import ReportGenerator


def main():
    print("\n" + "=" * 50)
    print("DATA ANALYSIS PIPELINE")
    print("=" * 50)
    
    
    print("\n[1/4] Generating synthetic sales data...")
    df = generate_sales_data(n_records=1000)
    print(f"✓ Generated {len(df)} records")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
    print(f"  Missing values: {df.isnull().sum().sum()}")
    
    
    print("\n[2/4] Processing and cleaning data...")
    processor = DataProcessor(df)
    (processor
     .handle_missing_values(strategy='mean')
     .add_derived_features()
     .normalize_columns()
     .remove_outliers(column='revenue', threshold=3))
    
    df_processed = processor.get_dataframe()
    summary = processor.get_summary()
    print(f"Processing complete")
    print(f" Original rows: {summary['original_rows']}")
    print(f" Current rows: {summary['current_rows']}")
    print(f" Rows removed: {summary['rows_removed']}")
    print(f" Missing values: {summary['missing_values']}")
    
    
    print("\n[3/4] Performing statistical analysis...")
    analyzer = DataAnalyzer(df_processed)
    
    
    analyzer.basic_statistics()
    analyzer.category_analysis()
    analyzer.regional_analysis()
    analyzer.temporal_analysis()
    analyzer.customer_analysis()
    analyzer.correlation_analysis()
    
    print("Analysis complete")
    print(" - Basic statistics calculated")
    print(" - Category performance analyzed")
    print(" - Regional trends identified")
    print(" - Temporal patterns extracted")
    print(" - Customer segmentation completed")
    print(" - Correlations computed")
    
    
    print("\n[4/4] Generating reports and visualizations...")
    report_gen = ReportGenerator(df_processed, analyzer)
    
    
    report_gen.print_report()
    
    
    report_gen.create_visualizations('analysis_report.png')
    
    print("\nANALYSIS PIPELINE COMPLETED SUCCESSFULLY")
    
    
    return {
        'data': df_processed,
        'analyzer': analyzer,
        'processor': processor,
    }


if __name__ == '__main__':
    results = main()