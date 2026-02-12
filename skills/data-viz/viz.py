#!/usr/bin/env python3
"""
Data Visualization CLI Tool
Creates various types of charts from CSV/Excel/JSON data
"""

import argparse
import pandas as pd
import sys
from pathlib import Path


def load_data(filepath, sample=None):
    """Load data from file with automatic format detection"""
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Detect file type
    if filepath.suffix == '.csv':
        df = pd.read_csv(filepath)
    elif filepath.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    elif filepath.suffix == '.json':
        df = pd.read_json(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    # Sample if requested
    if sample and len(df) > sample:
        df = df.sample(n=sample, random_state=42)

    return df


def aggregate_data(df, group_col, agg_col, agg_func='mean'):
    """Aggregate data by a column"""
    if group_col not in df.columns:
        raise ValueError(f"Column '{group_col}' not found")

    agg_dict = {
        'sum': 'sum',
        'mean': 'mean',
        'avg': 'mean',
        'count': 'count',
        'median': 'median',
        'std': 'std',
        'min': 'min',
        'max': 'max'
    }

    func = agg_dict.get(agg_func.lower(), 'mean')

    if agg_col == '*':
        return df.groupby(group_col).size().reset_index(name='value')
    else:
        result = df.groupby(group_col)[agg_col].agg(func).reset_index()
        result.columns = [group_col, 'value']
        return result


def create_line_plot(df, x_col, y_cols, output, title=None, color=None, figsize=(10, 6)):
    """Create a line plot using matplotlib"""
    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)

    for y_col in y_cols.split(','):
        if y_col not in df.columns:
            print(f"Warning: Column '{y_col}' not found, skipping")
            continue
        plt.plot(df[x_col], df[y_col], label=y_col, color=color if color else None)

    plt.xlabel(x_col)
    plt.ylabel('Value')
    if title:
        plt.title(title)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Saved line plot to: {output}")


def create_bar_plot(df, x_col, y_col, output, title=None, color=None, figsize=(10, 6)):
    """Create a bar plot using matplotlib"""
    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)
    plt.bar(df[x_col], df[y_col], color=color)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    if title:
        plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Saved bar plot to: {output}")


def create_scatter_plot(df, x_col, y_col, output, title=None, color=None, figsize=(10, 6)):
    """Create a scatter plot using matplotlib"""
    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)
    plt.scatter(df[x_col], df[y_col], alpha=0.6, color=color)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    if title:
        plt.title(title)
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Saved scatter plot to: {output}")


def create_histogram(df, col, output, title=None, bins=30, color=None, figsize=(10, 6)):
    """Create a histogram using matplotlib"""
    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)
    plt.hist(df[col], bins=bins, color=color, edgecolor='black', alpha=0.7)
    plt.xlabel(col)
    plt.ylabel('Frequency')
    if title:
        plt.title(title)
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Saved histogram to: {output}")


def create_pie_plot(df, labels_col, values_col, output, title=None, figsize=(10, 6)):
    """Create a pie chart using matplotlib"""
    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)
    plt.pie(df[values_col], labels=df[labels_col], autopct='%1.1f%%', startangle=90)
    if title:
        plt.title(title)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Saved pie chart to: {output}")


def create_box_plot(df, x_col, y_col, output, title=None, figsize=(10, 6)):
    """Create a box plot using matplotlib"""
    import matplotlib.pyplot as plt

    plt.figure(figsize=figsize)
    if x_col:
        df.boxplot(column=y_col, by=x_col, figsize=figsize)
    else:
        df.boxplot(column=y_col, figsize=figsize)
    if title:
        plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"Saved box plot to: {output}")


def create_interactive_plot(df, chart_type, x_col, y_col, output, title=None):
    """Create an interactive plot using plotly"""
    import plotly.express as px

    if chart_type == 'line':
        fig = px.line(df, x=x_col, y=y_col, title=title)
    elif chart_type == 'bar':
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    elif chart_type == 'scatter':
        fig = px.scatter(df, x=x_col, y=y_col, title=title)
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=y_col if not x_col else x_col, title=title)
    elif chart_type == 'pie':
        fig = px.pie(df, names=x_col, values=y_col, title=title)
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    fig.write_html(output)
    print(f"Saved interactive {chart_type} plot to: {output}")


def main():
    parser = argparse.ArgumentParser(description='Create data visualizations')
    subparsers = parser.add_subparsers(dest='command', help='Chart type')

    # Common arguments
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('data_file', help='Input data file (CSV, Excel, JSON)')
    common_parser.add_argument('--x', help='X-axis column')
    common_parser.add_argument('--y', help='Y-axis column(s), comma-separated for multiple')
    common_parser.add_argument('--output', '-o', help='Output file path')
    common_parser.add_argument('--title', help='Chart title')
    common_parser.add_argument('--color', help='Chart color')
    common_parser.add_argument('--sample', type=int, help='Sample N rows from data')

    # Aggregation
    agg_parser = argparse.ArgumentParser(add_help=False)
    agg_parser.add_argument('--group', help='Group by column')
    agg_parser.add_argument('--agg', default='mean',
                           choices=['sum', 'mean', 'count', 'median', 'std', 'min', 'max'],
                           help='Aggregation function')

    # Line plot
    parser_line = subparsers.add_parser('line', parents=[common_parser, agg_parser],
                                       help='Create a line plot')

    # Bar plot
    parser_bar = subparsers.add_parser('bar', parents=[common_parser, agg_parser],
                                      help='Create a bar plot')

    # Scatter plot
    parser_scatter = subparsers.add_parser('scatter', parents=[common_parser],
                                         help='Create a scatter plot')

    # Histogram
    parser_hist = subparsers.add_parser('histogram', parents=[common_parser],
                                       help='Create a histogram')
    parser_hist.add_argument('--column', help='Column to plot (instead of --y)')
    parser_hist.add_argument('--bins', type=int, default=30, help='Number of bins')

    # Pie chart
    parser_pie = subparsers.add_parser('pie', parents=[common_parser],
                                     help='Create a pie chart')
    parser_pie.add_argument('--labels', help='Labels column (instead of --x)')
    parser_pie.add_argument('--values', help='Values column (instead of --y)')

    # Box plot
    parser_box = subparsers.add_parser('box', parents=[common_parser],
                                      help='Create a box plot')

    # Interactive plot
    parser_interactive = subparsers.add_parser('interactive', parents=[common_parser],
                                              help='Create an interactive Plotly chart')
    parser_interactive.add_argument('--type', required=True,
                                    choices=['line', 'bar', 'scatter', 'histogram', 'pie'],
                                    help='Chart type')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Load data
    try:
        df = load_data(args.data_file, sample=args.sample)
        print(f"Loaded {len(df)} rows from {args.data_file}")
        print(f"Columns: {', '.join(df.columns)}")
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # Aggregate if needed
    if hasattr(args, 'group') and args.group:
        try:
            df = aggregate_data(df, args.group, args.y if hasattr(args, 'y') else args.y, args.agg)
            print(f"Aggregated to {len(df)} groups")
        except Exception as e:
            print(f"Error aggregating: {e}")
            sys.exit(1)

    # Create chart
    try:
        if args.command == 'line':
            create_line_plot(df, args.x, args.y, args.output or 'line.png',
                            args.title, args.color)
        elif args.command == 'bar':
            create_bar_plot(df, args.x, args.y, args.output or 'bar.png',
                           args.title, args.color)
        elif args.command == 'scatter':
            create_scatter_plot(df, args.x, args.y, args.output or 'scatter.png',
                               args.title, args.color)
        elif args.command == 'histogram':
            col = args.column or args.y
            create_histogram(df, col, args.output or 'histogram.png',
                           args.title, args.bins, args.color)
        elif args.command == 'pie':
            labels = args.labels or args.x
            values = args.values or args.y
            create_pie_plot(df, labels, values, args.output or 'pie.png', args.title)
        elif args.command == 'box':
            create_box_plot(df, args.x, args.y, args.output or 'boxplot.png', args.title)
        elif args.command == 'interactive':
            create_interactive_plot(df, args.type, args.x, args.y,
                                  args.output or f'{args.type}.html', args.title)
    except Exception as e:
        print(f"Error creating chart: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
