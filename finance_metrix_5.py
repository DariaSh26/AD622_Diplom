import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_users = pd.read_csv("users.csv")
df_orders = pd.read_csv("orders.csv")
df_events = pd.read_csv("events.csv")

df_users['reg_date'] = pd.to_datetime(df_users['reg_date'])
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
df_events['timestamp'] = pd.to_datetime(df_events['timestamp'])

df_orders_clean = df_orders[df_orders['status'] == 'Delivered'].copy()

total_revenue = df_orders['amount'].sum()
clean_revenue = df_orders_clean['amount'].sum()
lost_revenue = total_revenue - clean_revenue

def get_period(date):
    if date < pd.Timestamp('2026-10-01'):
        return '1. До акции (сентябрь)'
    elif date <= pd.Timestamp('2026-10-07 23:59:59'):
        return '2. Во время акции (1-7 окт)'
    else:
        return '3. После акции (8-25 окт)'

df_orders_clean['period'] = df_orders_clean['order_date'].apply(get_period)

eda_finance = df_orders_clean.groupby('period').agg(
    clean_revenue = ('amount', 'sum'),       # Чистая прибыль (сумма)
    orders_count = ('order_id', 'count'),    # Общее количество заказов
    aov = ('amount', 'mean'),                # Средний чек
    unique_buyers = ('user_id', 'nunique')    # Количество уникальных покупателей
).reset_index()

print("--- Финансовые метрики по периодам (Очищенные данные) ---")
print(eda_finance.to_string(index=False))

df_events['period'] = df_events['timestamp'].apply(get_period)

funnel = df_events.groupby(['period', 'event_type'])['user_id'].nunique().unstack().reset_index()
funnel['CR_to_cart'] = funnel['cart'] / funnel['view'] * 100
funnel['CR_cart_to_buy'] = funnel['purchase'] / funnel['cart'] * 100
funnel['CR_total'] = funnel['purchase'] / funnel['view'] + 100

print("\n---Конверсия воронки (CR) по периодам ---")
print(funnel[['period', 'view', 'cart', 'purchase']].to_string(index=False))


# Построение комбинированного графика
sns.set_theme(style="white")
fig, ax1 = plt.subplots(figsize=(10, 6.5), dpi=100)
fig.patch.set_facecolor('#f8f9fa')

sns.barplot(data=eda_finance, x='period', y='clean_revenue', ax=ax1, color='#1e88e5', alpha=0.8,
            width=0.45, edgecolor='#0d47a1')
ax1.set_ylabel("Чистая выручка, руб.", color='#0d47a1', fontsize=12, weight='bold', labelpad=15)
ax1.tick_params(axis='y', labelcolor='#0d47a1', labelsize=11)
ax1.set_xlabel('')
ax1.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

for p in ax1.patches:
    h = p.get_height()
    if h > 0:
        ax1.annotate(f"{h:,.0f} ₽", (p.get_x() + p.get_width() / 2., h), ha='center', va='bottom',
                     fontsize=11, weight='bold', color='#0d47a1', xytext=(0, 6), textcoords='offset points')

plt.show()