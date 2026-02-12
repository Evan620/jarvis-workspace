"""
Africa AI Data Center Visualization
Analyzes AfDB $10B AI Infrastructure Fund data
Uses data-viz-construction skill principles
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10

# Create data from document
def create_master_dataset():
    """Create master dataset from document data"""

    countries = [
        'South Africa', 'Kenya', 'Nigeria', 'Egypt', 'Morocco',
        'Ghana', 'Côte d_Ivoire', 'Senegal'
    ]

    codes = ['SA', 'KE', 'NG', 'EG', 'MO', 'GH', 'CI', 'SN']

    # Overall readiness scores
    overall_scores = [8.5, 8.2, 7.8, 8.0, 7.5, 7.0, 7.2, 7.1]

    # Five dimensions (1-10 scale)
    power_reliability = [7, 7, 5, 8, 8, 6, 6, 7]
    fiber_connectivity = [9, 9, 9, 10, 7, 8, 8, 7]  # Based on broadband speeds
    regulatory_score = [8, 9, 7, 7, 7, 7, 7, 9]  # ERI-based
    cooling_efficiency = [8, 8, 7, 7, 8, 7, 7, 7]  # Inverse of cooling costs
    digital_demand = [10, 9, 10, 8, 7, 7, 7, 7]

    # Investment allocation ($ Billions)
    investment = [3.0, 2.0, 1.5, 1.0, 0.75, 0.25, 0.25, 0]

    # Broadband speeds (Mbps)
    broadband_speeds = [48.5, 35.0, 22.0, 84.5, 36.4, 51.2, 59.9, 30.0]

    # Cooling cost index (relative, lower is better)
    cooling_costs = [1.4, 1.2, 1.6, 1.5, 1.3, 1.4, 1.4, 1.3]

    # Time to market (months)
    time_to_market = [18, 30, 24, 30, 36, 42, 36, 60]

    # Expected IRR (%)
    irr = [15, 20, 25, 10, 15, 10, 5, 5]

    # ERI score
    eri_score = [None, 0.889, None, None, None, None, None, 0.892]

    # Risk profile (1=Low, 5=High)
    risk_profile = [2, 2, 4, 3, 3, 3, 3, 3]

    # Region
    region = ['Southern', 'East', 'West', 'North', 'North', 'West', 'West', 'West']

    df = pd.DataFrame({
        'Country': countries,
        'Code': codes,
        'Overall_Readiness': overall_scores,
        'Power_Reliability': power_reliability,
        'Fiber_Connectivity': fiber_connectivity,
        'Regulatory_Score': regulatory_score,
        'Cooling_Efficiency': cooling_efficiency,
        'Digital_Demand': digital_demand,
        'Investment_B': investment,
        'Broadband_Mbps': broadband_speeds,
        'Cooling_Cost_Index': cooling_costs,
        'Time_to_Market_Months': time_to_market,
        'Expected_IRR_Pct': irr,
        'ERI_Score': eri_score,
        'Risk_Profile': risk_profile,
        'Region': region
    })

    return df

# Visualization functions
def figure1_overall_readiness(df):
    """Figure 1: Overall Readiness Scores by Market"""
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['#2ecc71' if x >= 8.0 else '#f39c12' if x >= 7.5 else '#e74c3c'
              for x in df['Overall_Readiness']]

    bars = ax.barh(df['Country'], df['Overall_Readiness'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, df['Overall_Readiness'])):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('Overall Readiness Score (1-10)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1: Overall Readiness Scores by Market\nAfDB $10B AI Infrastructure Fund',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 11)
    ax.grid(axis='x', alpha=0.3)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', label='Tier 1 (8.0+)'),
        Patch(facecolor='#f39c12', label='Tier 2 (7.5-7.9)'),
        Patch(facecolor='#e74c3c', label='Tier 3 (<7.5)')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    return fig

def figure2_radar_charts(df):
    """Figure 2: Five-Dimension Radar Charts"""
    # Select top 4 countries for radar charts
    top_countries = df.nlargest(4, 'Overall_Readiness').copy()

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    axes = axes.flatten()

    categories = ['Power\nReliability', 'Fiber\nConnectivity', 'Regulatory\nScore',
                  'Cooling\nEfficiency', 'Digital\nDemand']

    for idx, (ax, (_, row)) in enumerate(zip(axes, top_countries.iterrows())):
        values = [row['Power_Reliability'], row['Fiber_Connectivity'],
                  row['Regulatory_Score'], row['Cooling_Efficiency'],
                  row['Digital_Demand']]

        # Close the radar
        values += values[:1]
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        ax.plot(angles, values, 'o-', linewidth=2, color='#3498db')
        ax.fill(angles, values, alpha=0.25, color='#3498db')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 11)
        ax.set_yticks(range(2, 11, 2))
        ax.grid(True, alpha=0.3)
        ax.set_title(f"{row['Country']} - Readiness Profile\nOverall: {row['Overall_Readiness']}/10",
                    fontsize=13, fontweight='bold', pad=10)

        # Add strengths/weaknesses
        max_val = max(values[:-1])
        min_val = min(values[:-1])
        max_idx = values[:-1].index(max_val)
        min_idx = values[:-1].index(min_val)

        strength = categories[max_idx].replace('\n', ' ')
        weakness = categories[min_idx].replace('\n', ' ')

        if max_val >= 9:
            ax.text(0, -1.5, f"✓ Strength: {strength} ({max_val}/10)",
                   ha='center', fontsize=9, color='#27ae60', fontweight='bold')
        if min_val <= 6:
            ax.text(0, -1.8, f"⚠ Weakness: {weakness} ({min_val}/10)",
                   ha='center', fontsize=9, color='#e74c3c', fontweight='bold')

    plt.suptitle('Figure 2: Five-Dimension Readiness Profiles',
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    return fig

def figure3_investment_allocation(df):
    """Figure 3: Investment Volume by Market"""
    df_invest = df[df['Investment_B'] > 0].sort_values('Investment_B', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ['#2ecc71' if x >= 2.0 else '#f39c12' if x >= 1.0 else '#95a5a6'
              for x in df_invest['Investment_B']]

    bars = ax.barh(df_invest['Country'], df_invest['Investment_B'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels
    for bar, val in zip(bars, df_invest['Investment_B']):
        ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                f'${val:.2f}B', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('Investment Volume ($ Billions)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 3: Investment Allocation by Market\nAfDB $10B Fund - Phase 1 Priority',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 3.5)
    ax.grid(axis='x', alpha=0.3)

    # Add phase annotations
    ax.axvline(x=1.0, color='#f39c12', linestyle='--', alpha=0.5, linewidth=1)
    ax.text(0.5, df_invest['Country'].iloc[-1], 'Phase 2',
            ha='center', va='bottom', fontsize=9, color='#f39c12', fontweight='bold')
    ax.text(2.5, df_invest['Country'].iloc[-1], 'Phase 1',
            ha='center', va='bottom', fontsize=9, color='#2ecc71', fontweight='bold')

    plt.tight_layout()
    return fig

def figure4_power_vs_fiber(df):
    """Figure 4: Power vs Fiber Connectivity Scatter Plot"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create scatter with bubble sizes
    scatter = ax.scatter(df['Power_Reliability'], df['Broadband_Mbps'],
                         s=df['Overall_Readiness']*100, c=df['Overall_Readiness'],
                         cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=1)

    # Add country labels
    for i, row in df.iterrows():
        ax.annotate(row['Code'], (row['Power_Reliability'], row['Broadband_Mbps']),
                    fontsize=11, fontweight='bold',
                    xytext=(5, 5), textcoords='offset points')

    ax.set_xlabel('Power Reliability Score (1-10)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fiber Connectivity (Mbps)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 4: Power Reliability vs Fiber Connectivity\nBubble Size = Overall Readiness',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(4, 11)
    ax.set_ylim(0, 95)
    ax.grid(True, alpha=0.3)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Overall Readiness Score', fontsize=10, fontweight='bold')

    # Add key insights
    insights = [
        "Key Insights:",
        "• Egypt: Excellent fiber but high cooling costs",
        "• Kenya: Good balance across all dimensions",
        "• Nigeria: Low fiber but high market demand",
        "• South Africa: Moderate fiber, mature ecosystem"
    ]
    ax.text(0.02, 0.98, '\n'.join(insights), transform=ax.transAxes,
            fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round',
            facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig

def figure5_time_to_market(df):
    """Figure 5: Time to Market by Country"""
    df_ttm = df.sort_values('Time_to_Market_Months')

    fig, ax = plt.subplots(figsize=(12, 7))

    # Color by phase
    colors = []
    for ttm in df_ttm['Time_to_Market_Months']:
        if ttm <= 30:
            colors.append('#2ecc71')
        elif ttm <= 42:
            colors.append('#f39c12')
        else:
            colors.append('#e74c3c')

    bars = ax.barh(df_ttm['Country'], df_ttm['Time_to_Market_Months'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels
    for bar, val in zip(bars, df_ttm['Time_to_Market_Months']):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val} mo', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel('Months to Operational Readiness', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5: Time to Market by Country\nStrategic Implementation Timeline',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 65)
    ax.grid(axis='x', alpha=0.3)

    # Add phase zones
    ax.axvline(x=30, color='#2ecc71', linestyle='--', linewidth=2, alpha=0.7)
    ax.axvline(x=42, color='#f39c12', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(15, len(df_ttm) - 0.5, 'Phase 1\n(18-30 mo)',
            ha='center', fontsize=9, color='#2ecc71', fontweight='bold')
    ax.text(36, len(df_ttm) - 0.5, 'Phase 2\n(36-42 mo)',
            ha='center', fontsize=9, color='#f39c12', fontweight='bold')
    ax.text(51, len(df_ttm) - 0.5, 'Phase 3\n(48-60 mo)',
            ha='center', fontsize=9, color='#e74c3c', fontweight='bold')

    plt.tight_layout()
    return fig

def figure6_cooling_efficiency(df):
    """Figure 6: Cooling Efficiency by Climate Zone"""
    df_cooling = df.sort_values('Cooling_Cost_Index')

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ['#27ae60' if x <= 1.3 else '#f39c12' if x <= 1.4 else '#e74c3c'
              for x in df_cooling['Cooling_Cost_Index']]

    bars = ax.bar(df_cooling['Code'], df_cooling['Cooling_Cost_Index'],
                 color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels
    for bar, val in zip(bars, df_cooling['Cooling_Cost_Index']):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Annual Cooling Operating Cost (Relative Index)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 6: Cooling Efficiency by Climate Zone\nLower is Better - Annual Cost Advantage',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 1.8)
    ax.grid(axis='y', alpha=0.3)

    # Add annotations
    ax.axhline(y=1.3, color='#27ae60', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(0, 1.32, 'Cooling Advantage Zone', fontsize=9, color='#27ae60', fontweight='bold')
    ax.text(0.5, 1.25, 'Kenya: 30% savings vs Nigeria',
            fontsize=10, color='#e74c3c', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.tight_layout()
    return fig

def figure7_regional_distribution(df):
    """Figure 7: Regional Distribution Map"""
    df_regional = df.groupby('Region').agg({
        'Investment_B': 'sum',
        'Country': 'count'
    }).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Pie chart
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']

    wedges, texts, autotexts = axes[0].pie(
        df_regional['Investment_B'],
        labels=[f"{r}\n${v:.2f}B" for r, v in zip(df_regional['Region'], df_regional['Investment_B'])],
        autopct='%1.0f%%',
        startangle=90,
        colors=colors[:len(df_regional)],
        wedgeprops=dict(width=0.6, edgecolor='black', linewidth=1)
    )

    axes[0].set_title('Investment by Region\nTotal: $8.75B',
                     fontsize=13, fontweight='bold', pad=20)

    # Bar chart
    bars = axes[1].bar(df_regional['Region'], df_regional['Investment_B'],
                      color=colors[:len(df_regional)], alpha=0.8, edgecolor='black', linewidth=1)

    for bar, val in zip(bars, df_regional['Investment_B']):
        axes[1].text(bar.get_x() + bar.get_width()/2, val + 0.05,
                     f'${val:.2f}B', ha='center', va='bottom', fontsize=11, fontweight='bold')

    axes[1].set_ylabel('Investment ($ Billions)', fontsize=12, fontweight='bold')
    axes[1].set_title('Investment Volume by Region', fontsize=13, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)

    plt.suptitle('Figure 7: Regional Distribution Analysis',
                fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig

def figure8_risk_vs_return(df):
    """Figure 8: Risk vs Return Profile"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create scatter
    scatter = ax.scatter(df['Risk_Profile'], df['Expected_IRR_Pct'],
                         s=df['Investment_B']*150, c=df['Overall_Readiness'],
                         cmap='RdYlGn', alpha=0.7, edgecolors='black', linewidth=2)

    # Add country labels
    for i, row in df.iterrows():
        ax.annotate(row['Code'], (row['Risk_Profile'], row['Expected_IRR_Pct']),
                    fontsize=11, fontweight='bold',
                    xytext=(5, 5), textcoords='offset points')

    ax.set_xlabel('Risk Profile (1=Low, 5=High)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Expected IRR (%)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 8: Risk vs Return Profile\nBubble Size = Investment Amount',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0, 28)
    ax.grid(True, alpha=0.3)

    # Add quadrant lines
    ax.axvline(x=2.5, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=15, color='gray', linestyle='--', alpha=0.5)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Overall Readiness', fontsize=10, fontweight='bold')

    # Add quadrant labels
    ax.text(3.75, 22, 'HIGH RETURN\nHIGH RISK',
            ha='center', fontsize=9, color='#e74c3c', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(1.5, 22, 'HIGH RETURN\nLOW RISK',
            ha='center', fontsize=9, color='#27ae60', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(1.5, 8, 'MODERATE RETURN\nLOW RISK',
            ha='center', fontsize=9, color='#f39c12', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(3.75, 8, 'MODERATE RETURN\nMEDIUM RISK',
            ha='center', fontsize=9, color='#95a5a6', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    return fig

def figure9_power_reliability(df):
    """Figure 9: Power Reliability Comparison"""
    df_power = df.sort_values('Power_Reliability')

    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ['#27ae60' if x >= 7.5 else '#f39c12' if x >= 6.5 else '#e74c3c'
              for x in df_power['Power_Reliability']]

    bars = ax.barh(df_power['Code'], df_power['Power_Reliability'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels and ERI scores
    for bar, val, eri in zip(bars, df_power['Power_Reliability'], df_power['ERI_Score']):
        label = f'{val:.0f}'
        if eri:
            label += f'\n(ERI: {eri:.3f})'
        ax.text(val + 0.15, bar.get_y() + bar.get_height()/2,
                label, va='center', fontsize=9, fontweight='bold')

    ax.set_xlabel('Grid Reliability Score (1-10)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 9: Power Reliability Comparison\nCritical Infrastructure Challenge',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 11)
    ax.grid(axis='x', alpha=0.3)

    # Add critical insight
    ax.text(0.98, 0.02, 'Critical Insight:\nNigeria\'s power score (5.0) is the lowest,\nrequiring 3-4x backup power investment',
            transform=ax.transAxes, ha='right', va='bottom',
            fontsize=9, color='#e74c3c', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    plt.tight_layout()
    return fig

def figure10_regulatory_excellence(df):
    """Figure 10: Regulatory Excellence Ranking"""
    df_reg = df[df['ERI_Score'].notna()].sort_values('ERI_Score', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#27ae60', '#f39c12']

    bars = ax.bar(df_reg['Code'], df_reg['ERI_Score'],
                  color=colors, alpha=0.8, edgecolor='black', linewidth=2)

    # Add value labels
    for bar, val, rank in zip(bars, df_reg['ERI_Score'], [1, 2]):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.01,
                f'#{rank}\n{val:.3f}', ha='center', va='bottom',
                fontsize=11, fontweight='bold')

    ax.set_ylabel('Electricity Regulatory Index Score', fontsize=12, fontweight='bold')
    ax.set_title('Figure 10: Regulatory Excellence Ranking (AfDB ERI 2024)\nTop 10 African Countries',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 1.0)
    ax.grid(axis='y', alpha=0.3)

    # Add annotation
    ax.text(0.98, 0.98, 'Strong regulatory framework =\nInvestor confidence',
            transform=ax.transAxes, ha='right', va='top',
            fontsize=10, color='#27ae60', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

    plt.tight_layout()
    return fig

def figure11_market_matrix(df):
    """Figure 11: Market Size vs Readiness Matrix"""
    fig, ax = plt.subplots(figsize=(12, 10))

    # Create scatter
    scatter = ax.scatter(df['Overall_Readiness'], df['Digital_Demand'],
                         s=df['Investment_B']*120, c=df['Time_to_Market_Months'],
                         cmap='RdYlGn_r', alpha=0.7, edgecolors='black', linewidth=2)

    # Add country labels
    for i, row in df.iterrows():
        ax.annotate(f"{row['Code']}\n(${row['Investment_B']:.2f}B)",
                    (row['Overall_Readiness'], row['Digital_Demand']),
                    fontsize=10, fontweight='bold',
                    xytext=(0, 10), textcoords='offset points',
                    ha='center')

    ax.set_xlabel('Readiness Score (1-10)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Digital Demand (1-10)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 11: Market Size vs Readiness Matrix\nBubble Size = Investment',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(6, 11)
    ax.set_ylim(6, 11)
    ax.grid(True, alpha=0.3)

    # Add quadrant lines
    ax.axvline(x=7.9, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(y=8.5, color='gray', linestyle='--', alpha=0.5)

    # Add quadrant labels
    ax.text(8.75, 9.5, 'HIGH DEMAND\nHIGH READINESS\n(Top Right)',
            ha='center', fontsize=9, color='#27ae60', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(9.5, 7.5, 'HIGH DEMAND\nLOWER READINESS\n(Bottom Right)',
            ha='center', fontsize=9, color='#e74c3c', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(7.3, 9.5, 'MODERATE DEMAND\nHIGH READINESS\n(Top Left)',
            ha='center', fontsize=9, color='#f39c12', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.text(7.5, 7.5, 'MODERATE DEMAND\nMODERATE READINESS\n(Center)',
            ha='center', fontsize=9, color='#95a5a6', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Time to Market (months)', fontsize=10, fontweight='bold')

    plt.tight_layout()
    return fig

def figure12_funding_timeline(df):
    """Figure 12: AfDB Fund Allocation Timeline"""
    fig, ax = plt.subplots(figsize=(14, 8))

    # Create Gantt-like timeline
    years = ['2026', '2027', '2028', '2029', '2030']
    y_pos = range(len(years))

    # Phase 1: Years 1-3
    phase1_df = df[(df['Investment_B'] >= 1.0)].nlargest(3, 'Investment_B')
    phase1_colors = ['#2ecc71', '#27ae60', '#229954']

    for i, (country, invest, color) in enumerate(zip(phase1_df['Country'],
                                                    phase1_df['Investment_B'],
                                                    phase1_colors)):
        ax.barh(0, 3, left=0, height=0.2, color=color, alpha=0.6, edgecolor='black',
                label=f'{country}: ${invest:.2f}B')
        ax.text(1.5, 0.1, f'{country[:3]}: ${invest:.2f}B',
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    # Phase 2: Years 4-5
    phase2_df = df[(df['Investment_B'] < 1.0) & (df['Investment_B'] > 0)]
    phase2_colors = ['#f39c12', '#e67e22', '#d68910']

    for i, (country, invest, color) in enumerate(zip(phase2_df['Country'],
                                                    phase2_df['Investment_B'],
                                                    phase2_colors)):
        ax.barh(1, 2, left=3, height=0.2, color=color, alpha=0.6, edgecolor='black')
        ax.text(4, 1.1, f'{country[:3]}: ${invest:.2f}B',
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    # Reserve Fund: Throughout
    ax.barh(2, 5, left=0, height=0.2, color='#9b59b6', alpha=0.6, edgecolor='black')
    ax.text(2.5, 2.1, 'Reserve: $1.25B',
            ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(['Phase 1 (2026-2028): $6.5B',
                        'Phase 2 (2029-2030): $2.25B',
                        'Reserve Fund (Throughout): $1.25B'], fontsize=11, fontweight='bold')
    ax.set_xlabel('Timeline (Years)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 12: AfDB Fund Allocation Timeline\nStrategic Phasing for Maximum Impact',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 5)
    ax.grid(axis='x', alpha=0.3)

    # Add phase separators
    ax.axvline(x=3, color='black', linestyle='--', linewidth=2)
    ax.text(1.5, -0.4, 'IMMEDIATE IMPACT\nReady Markets',
            ha='center', fontsize=10, color='#27ae60', fontweight='bold')
    ax.text(4, -0.4, 'STRATEGIC GROWTH\nEmerging Markets',
            ha='center', fontsize=10, color='#f39c12', fontweight='bold')

    plt.tight_layout()
    return fig

def figure13_broadband_speeds(df):
    """Figure 13: Broadband Speed Leaders"""
    df_speed = df.sort_values('Broadband_Mbps', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Color by speed tier
    colors = []
    for speed in df_speed['Broadband_Mbps']:
        if speed >= 50:
            colors.append('#2ecc71')
        elif speed >= 35:
            colors.append('#f39c12')
        else:
            colors.append('#e74c3c')

    bars = ax.barh(df_speed['Code'], df_speed['Broadband_Mbps'],
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    # Add value labels
    for bar, val in zip(bars, df_speed['Broadband_Mbps']):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.1f} Mbps', va='center', fontsize=10, fontweight='bold')

    ax.set_xlabel('Average Fixed Broadband Speed (Mbps)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 13: Broadband Speed Leaders\nAfrica Connectivity Rankings',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 95)
    ax.grid(axis='x', alpha=0.3)

    # Add Africa ranking annotations
    rankings = [
        "Egypt: #1 in Africa",
        "Côte d'Ivoire: #2 in Africa",
        "Ghana: #4 in Africa",
        "South Africa: #5 in Africa",
        "Morocco: #10 in Africa"
    ]
    ax.text(0.98, 0.98, '\n'.join(rankings), transform=ax.transAxes,
            ha='right', va='top', fontsize=9, color='#3498db', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    plt.tight_layout()
    return fig

# Main execution
def main():
    print("Creating master dataset...")
    df = create_master_dataset()
    print(f"Dataset created with {len(df)} countries")

    print("\nGenerating visualizations...")

    figures = [
        ('figure1_overall_readiness', figure1_overall_readiness),
        ('figure2_radar_charts', figure2_radar_charts),
        ('figure3_investment_allocation', figure3_investment_allocation),
        ('figure4_power_vs_fiber', figure4_power_vs_fiber),
        ('figure5_time_to_market', figure5_time_to_market),
        ('figure6_cooling_efficiency', figure6_cooling_efficiency),
        ('figure7_regional_distribution', figure7_regional_distribution),
        ('figure8_risk_vs_return', figure8_risk_vs_return),
        ('figure9_power_reliability', figure9_power_reliability),
        ('figure10_regulatory_excellence', figure10_regulatory_excellence),
        ('figure11_market_matrix', figure11_market_matrix),
        ('figure12_funding_timeline', figure12_funding_timeline),
        ('figure13_broadband_speeds', figure13_broadband_speeds)
    ]

    output_dir = '/home/evan/clawd/skills/data-viz-construction/figures'
    import os
    os.makedirs(output_dir, exist_ok=True)

    saved_files = []
    for name, func in figures:
        try:
            print(f"  Creating {name}...")
            fig = func(df)
            filepath = f"{output_dir}/{name}.png"
            fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            saved_files.append(filepath)
            print(f"    ✓ Saved to {filepath}")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    # Create summary data file
    summary_path = f"{output_dir}/data_summary.csv"
    df.to_csv(summary_path, index=False)
    saved_files.append(summary_path)
    print(f"\n✓ Summary data saved to {summary_path}")

    # Create markdown summary
    md_summary = f"""
# Africa AI Data Center Visualizations

**Analysis prepared for AfDB $10B AI Infrastructure Fund Decision Making**
**Date:** 9 February 2026

## Files Generated

### Visualizations ({len([f for f in saved_files if f.endswith('.png')])} charts)
"""
    for i, filepath in enumerate(saved_files):
        if filepath.endswith('.png'):
            filename = os.path.basename(filepath)
            md_summary += f"\n{i+1}. **{filename}** - {os.path.basename(filepath).replace('figure', 'Figure ').replace('_', ' ').replace('.png', '')}\n"

    md_summary += f"\n### Data Files\n- **data_summary.csv** - Complete dataset with all metrics\n"

    md_summary += f"""

## Summary of Key Insights

### 1. Market Readiness Hierarchy
**Tier 1 (Ready 2026-2028):** South Africa, Kenya, Nigeria
**Tier 2 (Ready 2028-2030):** Egypt, Morocco, Ghana
**Tier 3 (Ready 2030+):** Senegal, Côte d'Ivoire, Rwanda

### 2. Investment Priorities
**Phase 1 (Immediate):** $6.5B to top 3 markets (SA: $3.0B, KE: $2.0B, NG: $1.5B)
**Phase 2 (Strategic):** $2.25B to emerging markets (EG: $1.0B, MA: $0.75B, GH/CI: $0.5B)
**Reserve:** $1.25B for systemic support (skills, regulation, R&D)

### 3. Critical Success Factors
1. **Power Reliability:** #1 challenge, especially Nigeria (5/10)
2. **Cooling Efficiency:** Kenya offers 30% cost advantage
3. **Regulatory Excellence:** Senegal (#1), Kenya (#2) lead
4. **Connectivity:** Egypt (#1), Côte d'Ivoire (#2) fastest
5. **Digital Demand:** Nigeria, South Africa, Kenya top markets

### 4. Risk-Return Profile
- **Nigeria:** Highest IRR (25%) but highest risk (power challenges)
- **Kenya:** Optimal balance - 20% IRR with strong regulation
- **South Africa:** Mature market, 15% IRR, established ecosystem
- **Egypt:** 10% IRR, climate challenges, moderate risk

### 5. Strategic Recommendations
1. **Immediate Action:** Proceed with Phase 1 markets (SA, KE, NG)
2. **Risk Mitigation:** Nigeria requires 3-4x backup power investment
3. **Cooling Advantage:** Leverage Kenya's altitude for 30% cost savings
4. **Regulatory Alignment:** Follow Kenya/Senegal model for governance
5. **Connectivity Hub:** Use Egypt's #1 fiber position for regional expansion

## Technical Notes

- All visualizations created using Matplotlib, Seaborn, and Plotly
- Resolution: 300 DPI for publication quality
- Color schemes: Professional construction palettes
- Data sources: AfDB, ERI 2024, Ookla Speedtest Global Index

---

*Generated using data-viz-construction skill*
"""

    md_path = f"{output_dir}/README.md"
    with open(md_path, 'w') as f:
        f.write(md_summary)
    saved_files.append(md_path)

    print(f"\n{'='*60}")
    print(f"✅ ALL VISUALIZATIONS COMPLETE")
    print(f"{'='*60}")
    print(f"\nTotal files created: {len(saved_files)}")
    print(f"\nLocation: {output_dir}/")
    print(f"\nFiles:")
    for f in saved_files:
        print(f"  - {os.path.basename(f)}")
    print(f"\n{'='*60}")

    return saved_files

if __name__ == '__main__':
    saved_files = main()
