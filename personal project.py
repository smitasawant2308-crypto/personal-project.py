## Retail Intelligence Analytics and Sales Forecasting Dashboard

import pandas as pd

# Check pandas version
print("Pandas Version:", pd.__version__)

# Read CSV file
df = pd.read_csv(r"C:/Users/hp/Documents/retail_sales.csv")

# Display column names
print("\nColumns in Dataset:")
print(df.columns.tolist())

# Create Sales column
df["Sales"] = df["Quantity"] * df["Price"]

# Save cleaned dataset
df.to_csv(r"C:/Users/hp/Documents/cleaned_sales.csv", index=False)

print("\nData Cleaned Successfully!")

# Display first 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Dataset Information
print("\nDataset Information:")
print(df.info())

# Statistical Summary
print("\nStatistical Summary:")
print(df.describe())

# -----------------------------
# Total Sales
# -----------------------------
print("\nTotal Sales:")
print(df["Sales"].sum())

# -----------------------------
# Sales by Category
# -----------------------------
print("\nSales by Category:")
print(df.groupby("Category")["Sales"].sum())

# -----------------------------
# Sales by Product
# -----------------------------
print("\nSales by Product:")
print(df.groupby("Product")["Sales"].sum())

# -----------------------------
# Sales by City
# -----------------------------
print("\nSales by City:")
print(df.groupby("City")["Sales"].sum())

# -----------------------------
# Quantity Sold by Product
# -----------------------------
print("\nQuantity Sold by Product:")
print(df.groupby("Product")["Quantity"].sum())

# -----------------------------
# Top 5 Customers by Sales
# -----------------------------
print("\nTop Customers:")
print(df.groupby("Customer")["Sales"].sum().sort_values(ascending=False).head())

# -----------------------------
# Top 5 Products by Sales
# -----------------------------
print("\nTop Products:")
print(df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head())

# -----------------------------
# Highest Sale
# -----------------------------
print("\nHighest Sale:")
print(df.loc[df["Sales"].idxmax()])

# -----------------------------
# Lowest Sale
# -----------------------------
print("\nLowest Sale:")
print(df.loc[df["Sales"].idxmin()])

print("\nAnalysis Completed Successfully!")





import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Read the dataset
df = pd.read_csv(r"C:\Users\hp\Documents\cleaned_sales.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Create Sales column if it doesn't exist
if "Sales" not in df.columns:
    df["Sales"] = df["Quantity"] * df["Price"]





# Create Month feature
df["Month"] = df["Date"].dt.month

# Features and Target
X = df[["Month"]]      # DataFrame (with column name)
y = df["Sales"]

# Train the model
model = LinearRegression()
model.fit(X, y)

# Future months (use a DataFrame, not a NumPy array)
future_months = pd.DataFrame({
    "Month": np.arange(2, 13)
})

# Predict
forecast = model.predict(future_months)

# Remove negative values
forecast = np.maximum(forecast, 0)

# Display results
forecast_df = pd.DataFrame({
    "Month": future_months["Month"],
    "Forecasted Sales": forecast.astype(int)
})

print("\nSales Forecast")
print(forecast_df)


##graphs

import matplotlib.pyplot as plt

category_sales = df.groupby("Category")["Sales"].sum()

plt.figure(figsize=(8,5))
plt.bar(category_sales.index, category_sales.values)
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.grid(axis="y")
plt.show()


product_sales = df.groupby("Product")["Sales"].sum()

plt.figure(figsize=(10,5))
plt.bar(product_sales.index, product_sales.values)
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.show()


city_sales = df.groupby("City")["Sales"].sum()

plt.figure(figsize=(10,5))
plt.bar(city_sales.index, city_sales.values)
plt.title("Sales by City")
plt.xlabel("City")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.show()

plt.figure(figsize=(7,7))
plt.pie(
    category_sales,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Category-wise Sales")
plt.show()


df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

monthly_sales = df.groupby(df["Date"].dt.month)["Sales"].sum()

plt.figure(figsize=(8,5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.grid(True)
plt.show()


forecast_df = pd.DataFrame({
    "Month": future_months["Month"],
    "Forecasted Sales": forecast
})



plt.figure(figsize=(8,5))
plt.plot(
    forecast_df["Month"],
    forecast_df["Forecasted Sales"],
    marker="o"
)
plt.title("Sales Forecast")
plt.xlabel("Month")
plt.ylabel("Forecasted Sales")
plt.grid(True)
plt.show()

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Read dataset
df = pd.read_csv(r"C:/Users/hp/Documents/cleaned_sales.csv")

# Convert Date column
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Remove invalid dates
df = df.dropna(subset=["Date"])

# Group by Date
daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

# Create Day column
daily_sales["Day"] = range(len(daily_sales))

# Features and Target
X = daily_sales[["Day"]]
y = daily_sales["Sales"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Create future days as a DataFrame (same column name as training)
future_days = pd.DataFrame({
    "Day": range(len(daily_sales), len(daily_sales) + 30)
})

# Predict
forecast = model.predict(future_days)

# Prevent negative predictions
forecast = np.maximum(forecast, 0)

# Show forecast
forecast_df = pd.DataFrame({
    "Future Day": future_days["Day"],
    "Forecasted Sales": forecast.astype(int)
})

print("\nForecasted Sales for Next 30 Days:")



import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Retail Intelligence Dashboard")

df = pd.read_csv("C:/Users/hp/Documents/cleaned_sales.csv")

total_sales = df["Sales"].sum()

total_orders = len(df)

st.metric("Total Sales", f"₹{total_sales:,}")
st.metric("Orders", total_orders)

sales_city = df.groupby("City")["Sales"].sum().reset_index()

fig = px.bar(
    sales_city,
    x="City",
    y="Sales",
    title="Sales by City"
)

st.plotly_chart(fig)

category = df.groupby("Category")["Sales"].sum().reset_index()

fig2 = px.pie(
    category,
    values="Sales",
    names="Category",
    title="Category Share"
)

st.plotly_chart(fig2)


print("Project Executed Successfully")
