#!/bin/bash
# Example usage of data-viz skill

echo "=== Data Visualization Examples ==="
echo ""

# Ensure we're in the right directory
cd "$(dirname "$0")/.."
source venv/bin/activate

echo "1. Creating line chart of revenue trend..."
python viz.py line examples/sales_data.csv --x date --y revenue --title "Revenue Trend" --output examples/revenue_trend.png

echo ""
echo "2. Creating bar chart of sales by product..."
python viz.py bar examples/sales_data.csv --x product --y quantity --title "Quantity by Product" --output examples/quantity_by_product.png

echo ""
echo "3. Creating pie chart of revenue by category..."
python viz.py pie examples/sales_data.csv --labels category --values revenue --title "Revenue by Category" --output examples/revenue_by_category.png

echo ""
echo "4. Creating histogram of customer ages..."
python viz.py histogram examples/customers.csv --column age --title "Age Distribution" --output examples/age_distribution.png

echo ""
echo "5. Creating scatter plot of age vs spending..."
python viz.py scatter examples/customers.csv --x age --y spending --title "Age vs Spending" --output examples/age_vs_spending.png

echo ""
echo "6. Creating aggregated bar chart (revenue by product with sum)..."
python viz.py bar examples/sales_data.csv --group product --y revenue --agg sum --title "Total Revenue by Product" --output examples/total_revenue_by_product.png

echo ""
echo "7. Creating interactive plotly chart..."
python viz.py interactive examples/sales_data.csv --type line --x date --y revenue --title "Revenue Trend (Interactive)" --output examples/revenue_interactive.html

echo ""
echo "8. Creating bar chart of customer count by city..."
python viz.py bar examples/customers.csv --group city --y * --agg count --title "Customers by City" --output examples/customers_by_city.png

echo ""
echo "=== All examples complete! ==="
echo "Check the examples/ directory for generated charts"
ls -lh examples/*.png examples/*.html 2>/dev/null | grep -E '\.(png|html)$'
