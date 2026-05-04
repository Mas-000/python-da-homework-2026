"""
M5 Matplotlib & Seaborn 視覺化 — 課後作業
==========================================
情境：把分析結果做成圖表，用視覺化說故事。

資料路徑：datasets/ecommerce/orders_enriched.csv
"""
import matplotlib
matplotlib.use("Agg")  # 無 GUI 環境也能跑
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _load_data():
    """輔助函式：讀取資料"""
    return pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                       parse_dates=["order_date"])


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_bar_category():
    """
    畫出每個商品類別 (category) 的訂單數長條圖
    回傳 matplotlib Figure 物件
    提示：sns.countplot 或 value_counts().plot.bar()
    """
    df = _load_data()
    plt.figure(figsize=(8, 5))
    sns.countplot(x='category', data=df)
    plt.title('Number of Orders by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Orders')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()  

def green_hist_amount():
    """
    畫出訂單金額 (amount) 的分佈直方圖，分 20 個 bin
    回傳 matplotlib Figure 物件
    提示：sns.histplot(bins=20) 或 plt.hist()
    """
    df = _load_data()
    plt.figure(figsize=(8, 5))
    sns.histplot(df['amount'], bins=20, kde=False)
    plt.title('Distribution of Order Amount')
    plt.xlabel('Order Amount')
    plt.ylabel('Frequency')
    plt.tight_layout()
    return plt.gcf()  


def green_set_labels():
    """
    建立一個簡單的長條圖（內容不限），但必須設定：
    - 圖標題 (title)
    - X 軸標籤 (xlabel)
    - Y 軸標籤 (ylabel)
    回傳 matplotlib Figure 物件
    """
    df = _load_data()
    plt.figure(figsize=(8, 5))
    sns.countplot(x='region', data=df)
    plt.title('Number of Orders by Region')
    plt.xlabel('Region')
    plt.ylabel('Number of Orders')
    plt.tight_layout()
    return plt.gcf()


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_line_region_trend():
    """
    畫折線圖：比較 North 和 South 兩個地區的月營收趨勢
    - X 軸：月份
    - Y 軸：該月總營收
    - 兩條線，有圖例 (legend)
    回傳 matplotlib Figure 物件
    提示：分別 groupby 再 plot，或用 sns.lineplot(hue='region')
    """
    df = _load_data()
    df['order_date'] = pd.to_datetime(df['order_date'])
    df.set_index('order_date', inplace=True)
    monthly_revenue = df.groupby(['region', pd.Grouper(freq='M')'])['amount'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='order_date', y='amount', hue='region', data=monthly_revenue)
    plt.title('Monthly Revenue Trend by Region')
    plt.xlabel('Month')
    plt.ylabel('Total Revenue')
    plt.legend(title='Region')
    plt.tight_layout()
    return plt.gcf()


def yellow_box_vip():
    """
    畫箱形圖：比較不同 VIP 等級 (vip_level) 的訂單金額分佈
    回傳 matplotlib Figure 物件
    提示：sns.boxplot(x='vip_level', y='amount', data=df)
    """
    df = _load_data()
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='vip_level', y='amount', data=df)
    plt.title('Order Amount Distribution by VIP Level')
    plt.xlabel('VIP Level')
    plt.ylabel('Order Amount')
    plt.tight_layout()
    return plt.gcf()



def yellow_scatter_price_amount():
    """
    畫散佈圖：X=商品單價 (unit_price)，Y=訂單金額 (amount)
    回傳 matplotlib Figure 物件
    提示：plt.scatter() 或 sns.scatterplot()
    """
    df = _load_data()
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x='unit_price', y='amount', data=df)
    plt.title('Scatter Plot of Unit Price vs Order Amount')
    plt.xlabel('Unit Price')
    plt.ylabel('Order Amount')
    plt.tight_layout()
    return plt.gcf()


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_category_dashboard(category="Electronics"):
    """
    針對指定類別，畫 2×2 的 subplot dashboard：
    1. 左上：該類別月營收趨勢 (折線圖)
    2. 右上：該類別各地區營收 (長條圖)
    3. 左下：該類別 Top 5 商品營收 (水平長條圖)
    4. 右下：該類別訂單金額分佈 (直方圖)

    回傳 matplotlib Figure 物件
    提示：fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    """
    df = _load_data()
    df['order_date'] = pd.to_datetime(df['order_date'])
    category_df = df[df['category'] == category]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 左上：月營收趨勢
    monthly_revenue = category_df.set_index('order_date').resample('M')['amount'].sum()
    sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, ax=axes[0, 0])
    axes[0, 0].set_title(f'Monthly Revenue Trend for {category}')
    axes[0, 0].set_xlabel('Month')
    axes[0, 0].set_ylabel('Total Revenue')

    # 右上：各地區營收
    region_revenue = category_df.groupby('region')['amount'].sum().reset_index()
    sns.barplot(x='region', y='amount', data=region_revenue, ax=axes[0, 1])
    axes[0, 1].set_title(f'Revenue by Region for {category}')
    axes[0, 1].set_xlabel('Region')
    axes[0, 1].set_ylabel('Total Revenue')

    # 左下：Top 5 商品營收
    top_products = category_df.groupby('product_name')['amount'].sum().nlargest(5).reset_index()
    sns.barplot(x='amount', y='product_name', data=top_products, ax=axes[1, 0], orient='h')
    axes[1, 0].set_title(f'Top 5 Products by Revenue for {category}')
    axes[1, 0].set_xlabel('Total Revenue')
    axes[1, 0].set_ylabel('Product Name')

    # 右下：訂單金額分佈
    sns.histplot(category_df['amount'], bins=20, kde=False, ax=axes[1, 1])
    axes[1, 1].set_title(f'Order Amount Distribution for {category}')
    axes[1, 1].set_xlabel('Order Amount')
    axes[1, 1].set_ylabel('Frequency')

    plt.tight_layout()
    return fig
