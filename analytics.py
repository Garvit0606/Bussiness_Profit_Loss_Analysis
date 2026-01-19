import pandas as pd
import plotly.express as px

# HELPERS 
def clean_columns(df):
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def find_col(cols, keywords):
    for c in cols:
        for k in keywords:
            if k in c:
                return c
    return None

# CORE METRICS 
def overall_metrics(df):
    df = clean_columns(df)

    revenue_col = find_col(df.columns, ["revenue", "sales", "amount", "total"])
    cost_col = find_col(df.columns, ["cost", "expense", "purchase"])
    qty_col = find_col(df.columns, ["qty", "quantity", "units", "count"])

    revenue = df[revenue_col].fillna(0).sum() if revenue_col else 0
    cost = df[cost_col].fillna(0).sum() if cost_col else 0
    profit = revenue - cost
    total_sell = df[qty_col].fillna(0).sum() if qty_col else len(df)

    return revenue, profit, cost, total_sell

# TIME BASED 
def time_based(df, period="weekly"):
    df = clean_columns(df)

    date_col = find_col(df.columns, ["date", "order_date", "created"])
    revenue_col = find_col(df.columns, ["revenue", "sales", "amount", "total"])
    cost_col = find_col(df.columns, ["cost", "expense", "purchase"])

    if not date_col or not revenue_col:
        return None

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["profit"] = df[revenue_col].fillna(0) - (df[cost_col].fillna(0) if cost_col else 0)

    if period == "weekly":
        df["grp"] = df[date_col].dt.to_period("W").astype(str)
    elif period == "monthly":
        df["grp"] = df[date_col].dt.to_period("M").astype(str)
    else:
        df["grp"] = df[date_col].dt.to_period("Y").astype(str)

    return df.groupby("grp")[["profit"]].sum().reset_index()

# CHARTS 
def profit_loss_bar(df):
    return px.bar(df, x="grp", y="profit", title="Profit / Loss")

def profit_loss_pie(df):
    profit = df[df["profit"] > 0]["profit"].sum()
    loss = abs(df[df["profit"] < 0]["profit"].sum())
    return px.pie(
        names=["Profit", "Loss"],
        values=[profit, loss],
        title="Profit vs Loss"
    )

def total_sell_chart(df):
    df = clean_columns(df)
    qty_col = find_col(df.columns, ["qty", "quantity", "units", "count"])
    if not qty_col:
        return None
    return px.bar(df, y=qty_col, title="Total Sell")

def top_products(df):
    df = clean_columns(df)
    prod_col = find_col(df.columns, ["product", "item", "name"])
    qty_col = find_col(df.columns, ["qty", "quantity", "units", "count"])

    if not prod_col or not qty_col:
        return None, None

    grp = df.groupby(prod_col)[qty_col].sum().reset_index().sort_values(qty_col, ascending=False)

    bar = px.bar(grp, x=prod_col, y=qty_col, title="Most Selling Products")
    pie = px.pie(grp, names=prod_col, values=qty_col, title="Product Share")

    return bar, pie

