"""
M6 Plotly 互動儀表板 & Capstone — 課後作業
===========================================
情境：從原始資料到互動式儀表板，完成完整的資料分析 pipeline。

資料路徑：
  - datasets/ecommerce/orders_raw.csv（原始髒資料）
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_plotly_bar():
    """
    用 Plotly Express 畫出每個商品類別 (category) 的總營收長條圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.bar()
    """
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    revenue_by_cat = df.groupby('category')['amount'].sum().reset_index()
    fig = px.bar(revenue_by_cat, x='category', y='amount', title="Category Revenue")
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv", parse_dates=["order_date"])
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    revenue_by_month = df.groupby('month')['amount'].sum().reset_index()
    fig = px.line(revenue_by_month, x='month', y='amount', title="Monthly Revenue Trend")
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
    fig = px.pie(df, names='vip_level', title="Orders by VIP Level")
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：從髒資料到合併完成的 DataFrame
    1. 讀取 orders_raw.csv 並清理（欄位名稱、金額、日期、缺值、去重）
    2. 合併 customers.csv 和 products.csv
    回傳：合併後的 DataFrame
    """
  
    orders = pd.read_csv(raw_path)

    orders.columns = orders.columns.str.strip().str.lower().str.replace(' ', '_')
    
    if 'amount' in orders.columns and orders['amount'].dtype == 'object':
        orders['amount'] = orders['amount'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
        
    orders = orders.drop_duplicates().dropna()
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    
    df = orders.merge(customers, on='customer_id', how='left')
    df = df.merge(products, on='product_id', how='left')
    
    return df


def yellow_kpi_summary(df):
    """
    計算 4 個核心 KPI，回傳 dict：
    {
        "total_revenue": float,       # 總營收
        "order_count": int,           # 訂單數
        "active_customers": int,      # 不重複客戶數
        "avg_order_value": float,     # 平均客單價
    }
    """
    total_rev = float(df['amount'].sum())
    order_cnt = int(len(df))
    
    kpi_dict = {
        "total_revenue": total_rev,
        "order_count": order_cnt,
        "active_customers": int(df['customer_id'].nunique()),
        "avg_order_value": total_rev / order_cnt if order_cnt > 0 else 0.0
    }
    return kpi_dict


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖：
    - X：商品單價 (unit_price)
    - Y：訂單金額 (amount)
    - 顏色：商品類別 (category)
    - hover 顯示：商品名稱 (product_name)
    回傳 plotly Figure 物件
    提示：px.scatter(hover_data=['product_name'])
    """
    fig = px.scatter(
        df, 
        x='unit_price', 
        y='amount', 
        color='category', 
        hover_data=['product_name'],
        title="Unit Price vs Amount"
    )
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    """
    Capstone：完整的互動式儀表板

    流程：
    1. 清理 orders_raw.csv + 合併三張表
    2. 建立 2×2 subplot dashboard（用 plotly make_subplots）：
       - 左上：月營收趨勢 (line)
       - 右上：Top 10 商品營收 (bar)
       - 左下：各地區營收 (bar)
       - 右下：類別營收佔比 (pie/donut)
    3. 設定整體標題

    回傳 plotly Figure 物件
    提示：from plotly.subplots import make_subplots
    """
    # 1. 執行 ETL 取得乾淨合併的資料
    df = yellow_clean_and_merge(
        "datasets/ecommerce/orders_raw.csv",
        "datasets/ecommerce/customers.csv",
        "datasets/ecommerce/products.csv"
    )
    df['month'] = df['order_date'].dt.to_period('M').astype(str)

    # 2. 建立 2x2 子圖架構
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Monthly Revenue Trend", "Top 10 Products by Revenue", 
                        "Revenue by Region", "Revenue Share by Category"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}]]
    )

    # 左上：月營收趨勢 (line)
    m_rev = df.groupby('month')['amount'].sum().reset_index()
    fig.add_trace(go.Scatter(x=m_rev['month'], y=m_rev['amount'], mode='lines+markers', name="Trend"), row=1, col=1)

    # 右上：Top 10 商品營收 (bar)
    top10 = df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig.add_trace(go.Bar(x=top10['product_name'], y=top10['amount'], name="Top 10"), row=1, col=2)

    # 左下：各地區營收 (bar)
    reg_rev = df.groupby('region')['amount'].sum().reset_index()
    fig.add_trace(go.Bar(x=reg_rev['region'], y=reg_rev['amount'], name="Region"), row=2, col=1)

    # 右下：類別營收佔比 (pie/donut)
    cat_rev = df.groupby('category')['amount'].sum().reset_index()
    fig.add_trace(go.Pie(labels=cat_rev['category'], values=cat_rev['amount'], name="Category"), row=2, col=2)

    # 3. 設定整體標題與排版
    fig.update_layout(title_text="E-commerce Interactive Dashboard", height=800, showlegend=False)
     
    return fig