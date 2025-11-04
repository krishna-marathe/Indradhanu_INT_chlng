import os

def ensure_dir(path="visuals/"):
    if not os.path.exists(path):
        os.makedirs(path)

def plot_line(df, x, y, save_path="visuals/line_chart.png"):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    ensure_dir()
    plt.figure(figsize=(8,5))
    sns.lineplot(x=x, y=y, data=df)
    plt.title(f"Line Chart of {y} over {x}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"📈 Line chart saved → {save_path}")

def plot_bar(df, x, y, save_path="visuals/bar_chart.png"):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    ensure_dir()
    plt.figure(figsize=(8,5))
    sns.barplot(x=x, y=y, data=df)
    plt.title(f"Bar Chart of {y} vs {x}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"📊 Bar chart saved → {save_path}")

def plot_heatmap(df, save_path="visuals/correlation_heatmap.png"):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    ensure_dir()
    plt.figure(figsize=(8,6))
    numeric_df = df.select_dtypes(include='number')
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"🔥 Correlation heatmap saved → {save_path}")

def plot_interactive(df, x, y):
    import plotly.express as px
    
    fig = px.line(df, x=x, y=y, title=f"Interactive Line Chart: {y} vs {x}")
    fig.show()