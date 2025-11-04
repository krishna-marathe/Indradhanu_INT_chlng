def run_analysis(file_path):
    print("🚀 Starting Environmental Data Analysis...\n")
    
    # Lazy imports
    from data_loader import load_dataset
    from data_cleaner import clean_data
    from data_visualizer import plot_line, plot_bar, plot_heatmap, plot_interactive
    from data_insights import basic_summary, correlation_analysis, generate_insights
    
    # Load dataset
    df = load_dataset(file_path)
    if df is None:
        print("❌ Unable to continue — invalid dataset.")
        return
    
    # Clean data
    df = clean_data(df)
    
    # Generate basic summary and insights
    basic_summary(df)
    correlation_analysis(df)
    
    # Create visualizations if enough numeric columns exist
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 2:
        plot_line(df, numeric_cols[0], numeric_cols[1])
        plot_bar(df, numeric_cols[0], numeric_cols[1])
        plot_heatmap(df)
        plot_interactive(df, numeric_cols[0], numeric_cols[1])
    else:
        print("⚠️ Not enough numeric columns to visualize.")
    
    # Generate insights
    generate_insights(df)
    
    print("\n✅ Analysis completed successfully!")

if __name__ == "__main__":
    file_path = input("📂 Enter dataset file path (CSV/XLSX/JSON): ")
    run_analysis(file_path)