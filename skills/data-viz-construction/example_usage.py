"""
Example usage of the Data Visualization for Construction skill
Demonstrates key visualization functions with sample construction data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create sample construction data
def create_sample_data():
    """Generate sample construction project data"""
    np.random.seed(42)
    n_elements = 100

    categories = ['Structural', 'Architectural', 'MEP', 'Finishes', 'Foundation']
    materials = ['Concrete', 'Steel', 'Timber', 'Brick', 'Glass', 'Copper', 'Plastic']
    levels = list(range(1, 11))  # 10-floor building

    data = {
        'ElementId': [f'EL-{i:04d}' for i in range(n_elements)],
        'Category': np.random.choice(categories, n_elements),
        'Material': np.random.choice(materials, n_elements),
        'Level': np.random.choice(levels, n_elements),
        'Volume_m3': np.random.uniform(1, 50, n_elements),
        'Cost': np.random.uniform(1000, 50000, n_elements),
        'Weight_kg': np.random.uniform(100, 10000, n_elements)
    }

    df = pd.DataFrame(data)

    # Add some correlation between volume, cost, and weight
    df['Cost'] = df['Cost'] * (1 + df['Volume_m3'] / 50)
    df['Weight_kg'] = df['Weight_kg'] * (1 + df['Volume_m3'] / 50)

    return df

# Visualization functions (from SKILL.md)
def create_cost_breakdown_pie(df, cost_col='Cost', category_col='Category'):
    """Create pie chart for cost breakdown"""
    costs = df.groupby(category_col)[cost_col].sum()

    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        costs.values,
        labels=costs.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Set3.colors
    )

    ax.set_title('Cost Breakdown by Category', fontsize=14, fontweight='bold')

    ax.text(0, 0, f'Total: ${costs.sum():,.0f}',
            ha='center', va='center', fontsize=12)

    plt.tight_layout()
    return fig

def create_volume_bar_chart(df, volume_col='Volume_m3', category_col='Category'):
    """Create horizontal bar chart for volumes"""
    volumes = df.groupby(category_col)[volume_col].sum().sort_values()

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(volumes.index, volumes.values, color='steelblue')

    for bar, value in zip(bars, volumes.values):
        ax.text(value + volumes.max() * 0.01, bar.get_y() + bar.get_height()/2,
                f'{value:,.0f} m³', va='center', fontsize=10)

    ax.set_xlabel('Volume (m³)')
    ax.set_title('Material Volumes by Category', fontsize=14, fontweight='bold')
    ax.set_xlim(0, volumes.max() * 1.15)

    plt.tight_layout()
    return fig

def create_level_heatmap(df, level_col='Level', category_col='Category',
                          value_col='Volume_m3'):
    """Create heatmap for level-by-category analysis"""
    pivot = df.pivot_table(
        values=value_col,
        index=level_col,
        columns=category_col,
        aggfunc='sum',
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(
        pivot,
        annot=True,
        fmt=',.0f',
        cmap='YlOrRd',
        ax=ax,
        cbar_kws={'label': 'Volume (m³)'}
    )

    ax.set_title('Volume Distribution: Level × Category', fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig

# Main execution
if __name__ == '__main__':
    print("Generating sample construction data...")
    df = create_sample_data()
    print(f"Created dataset with {len(df)} elements")
    print(df.head())

    print("\nGenerating visualizations...")

    # Create cost breakdown pie chart
    print("1. Creating cost breakdown pie chart...")
    fig1 = create_cost_breakdown_pie(df)
    fig1.savefig('cost_breakdown.png', dpi=150, bbox_inches='tight')
    plt.close(fig1)
    print("   Saved to: cost_breakdown.png")

    # Create volume bar chart
    print("2. Creating volume bar chart...")
    fig2 = create_volume_bar_chart(df)
    fig2.savefig('volume_bars.png', dpi=150, bbox_inches='tight')
    plt.close(fig2)
    print("   Saved to: volume_bars.png")

    # Create level heatmap
    print("3. Creating level heatmap...")
    fig3 = create_level_heatmap(df)
    fig3.savefig('level_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close(fig3)
    print("   Saved to: level_heatmap.png")

    print("\nAll visualizations generated successfully!")
    print("\nData summary:")
    print(df.describe())
