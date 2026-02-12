# Data Visualization Skill

A comprehensive Python-based data visualization toolkit for creating charts, graphs, and interactive visualizations from various data sources.

## Description

This skill provides easy-to-use tools for data visualization including:
- Static plots (matplotlib, seaborn)
- Interactive charts (plotly)
- Declarative visualizations (altair)
- Quick dashboards (streamlit)
- Data loading from CSV, Excel, JSON

## Installation

```bash
cd ~/clawd/skills/data-viz
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Basic Charts

```bash
# Create a line chart from CSV data
python viz.py line data.csv --x column_name --y value_column --output chart.png

# Create a bar chart
python viz.py bar data.csv --x category --y count --output bar.png

# Create a scatter plot
python viz.py scatter data.csv --x x_column --y y_column --output scatter.png

# Create a histogram
python viz.py histogram data.csv --column value_column --output hist.png

# Create an interactive plotly chart
python viz.py interactive data.csv --type line --x date --y price --output interactive.html
```

### Dashboard

```bash
# Launch a quick Streamlit dashboard
python dashboard.py data.csv
```

### Advanced Options

```bash
# Custom styling
python viz.py line data.csv --x month --y sales --title "Monthly Sales" --color "blue" --output sales.png

# Group by and aggregate
python viz.py bar data.csv --x category --y revenue --agg sum --output revenue_by_category.png

# Multiple series
python viz.py line data.csv --x date --y column1,column2 --label Series1,Series2 --output multi.png
```

## Features

- **Multiple chart types:** line, bar, scatter, histogram, pie, boxplot, heatmap
- **Multiple backends:** matplotlib (static), plotly (interactive), altair (declarative)
- **Data formats:** CSV, Excel, JSON
- **Aggregation:** sum, mean, count, median, std
- **Customization:** titles, colors, labels, themes
- **Export formats:** PNG, SVG, PDF, HTML (interactive)

## Examples

### Example 1: Sales Data
```bash
# Create sales dashboard
python viz.py line sales.csv --x date --y revenue --title "Revenue Trend" --output revenue_trend.png
python viz.py bar sales.csv --x product --y quantity --title "Sales by Product" --output product_sales.png
python viz.py pie sales.csv --labels product --values revenue --title "Revenue Distribution" --output revenue_pie.png
```

### Example 2: Customer Data
```bash
# Analyze customer demographics
python viz.py histogram customers.csv --column age --title "Age Distribution" --output age_dist.png
python viz.py bar customers.csv --x city --agg count --title "Customers by City" --output customers_by_city.png
python viz.py scatter customers.csv --x age --y spending --title "Age vs Spending" --output age_spending.png
```

### Example 3: Time Series
```bash
# Time series analysis
python viz.py line timeseries.csv --x timestamp --y value --title "Time Series" --output timeseries.png
python viz.py heatmap timeseries.csv --x day --y hour --values metric --title "Heatmap" --output heatmap.png
```

## Dependencies

- pandas, numpy - Data handling
- matplotlib, seaborn - Static plotting
- plotly - Interactive charts
- altair - Declarative visualization
- streamlit - Quick dashboards
- Pillow, openpyxl, xlrd - File I/O

## File Structure

```
data-viz/
├── SKILL.md
├── requirements.txt
├── viz.py              # Main CLI tool
├── dashboard.py        # Streamlit dashboard
├── examples/
│   ├── sample_data.csv
│   └── example_usage.py
└── venv/
```

## Tips

- Use `--help` with any command to see all options
- For large datasets, use `--sample N` to randomly sample N rows
- Use `--agg` to aggregate data before plotting (sum, mean, count, etc.)
- Plotly charts (HTML) are interactive - hover to see values, zoom/pan
- Streamlit dashboard automatically explores your data
