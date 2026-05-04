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


def _load_enriched_data():
    """輔助函式：讀取已處理好的資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv", parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_plotly_bar():
    """
    用 Plotly Express 畫出每個商品類別 (category) 的總營收長條圖
    """
    df = _load_enriched_data()
    # 聚合資料
    res = df.groupby('category')['amount'].sum().reset_index()
    # 畫圖
    fig = px.bar(res, x='category', y='amount', title="Total Revenue by Category")
    return fig


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    """
    df = _load_enriched_data()
    # 建立月份標籤
    df['month'] = df['order_date'].dt.to_period('M').astype(str)
    res = df.groupby('month')['amount'].sum().reset_index()
    # 畫圖
    fig = px.line(res, x='month', y='amount', title="Monthly Revenue Trend")
    return fig


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    """
    df = _load_enriched_data()
    # 畫圖
    fig = px.pie(df, names='vip_level', title="Order Distribution by VIP Level")
    return fig


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：清理並合併三張表格
    """
    # 1. 讀取 orders_raw 並進行基本清理
    orders = pd.read_csv(raw_path)
    # 去除重複值與缺值
    orders = orders.drop_duplicates().dropna()
    # 轉換日期格式
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # 2. 讀取關聯表
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    
    # 3. 執行合併 (使用 left join 確保以訂單為主體)
    # 先併客戶資料
    df = orders.merge(customers, on='customer_id', how='left')
    # 再併商品資料
    df = df.merge(products, on='product_id', how='left')
    
    return df


def yellow_kpi_summary(df):
    """
    計算核心 KPI 並回傳字典
    """
    total_revenue = float(df['amount'].sum())
    order_count = int(len(df))
    active_customers = int(df['customer_id'].nunique())
    avg_order_value = total_revenue / order_count if order_count > 0 else 0.0
    
    return {
        "total_revenue": total_revenue,
        "order_count": order_count,
        "active_customers": active_customers,
        "avg_order_value": avg_order_value,
    }


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖
    """
    fig = px.scatter(
        df, 
        x='unit_price', 
        y='amount', 
        color='category',
        hover_data=['product_name'],
        title="Relationship between Unit Price and Order Amount"
    )
    return fig


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    """
    Capstone：建立 2x2 互動式儀表板
    """
    # 1. 準備資料
    df = yellow_clean_and_merge(
        "datasets/ecommerce/orders_raw.csv",
        "datasets/ecommerce/customers.csv",
        "datasets/ecommerce/products.csv"
    )
    df['month'] = df['order_date'].dt.to_period('M').astype(str)

    # 2. 建立子圖架構
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Monthly Revenue Trend", "Top 10 Products by Revenue", 
                        "Revenue by Region", "Revenue Share by Category"),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "pie"}]]
    )

    # 3. 計算各圖數據並加入 Trace
    # 左上：折線圖
    m_rev = df.groupby('month')['amount'].sum().reset_index()
    fig.add_trace(go.Scatter(x=m_rev['month'], y=m_rev['amount'], name="Revenue"), row=1, col=1)

    # 右上：Top 10 商品
    top10 = df.groupby('product_name')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig.add_trace(go.Bar(x=top10['product_name'], y=top10['amount'], name="Product"), row=1, col=2)

    # 左下：地區營收
    reg_rev = df.groupby('region')['amount'].sum().reset_index()
    fig.add_trace(go.Bar(x=reg_rev['region'], y=reg_rev['amount'], name="Region"), row=2, col=1)

    # 右下：類別佔比
    cat_rev = df.groupby('category')['amount'].sum().reset_index()
    fig.add_trace(go.Pie(labels=cat_rev['category'], values=cat_rev['amount']), row=2, col=2)

    # 4. 佈局設定
    fig.update_layout(height=900, title_text="E-commerce Business Insight Dashboard", showlegend=False)
    
    return fig