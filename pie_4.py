import pandas as pd
import numpy as np
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

print(f"Общая сумма заказов (включая отмены): {total_revenue:,.2f} руб.")
print(f"Реальная очищенная выручка компании: {clean_revenue:,.2f} руб.")
print(f"Отсеяно из-за отмен и возвратов: {lost_revenue:,.2f} руб.")

canceled_revenue = df_orders[df_orders['status'] == 'Canceled']['amount'].sum()
refunded_revenue = df_orders[df_orders['status'] == 'Refunded']['amount'].sum()

steps = [
    'Все заказы\n(Грязные данные)',
    'Отмена\n(Canceled)',
    'Возвраты\n(Refunded)',
    'Реальная выручка\n(Чистые деньги)'
]

amounts = [total_revenue, -canceled_revenue, -refunded_revenue, clean_revenue]

cumulative = np.zeros(len(amounts))
cumulative[0] = amounts[0]
for i in range(1, len(amounts)):
    if i == len(amounts) - 1:
        cumulative[i] = clean_revenue
    else:
        cumulative[i] = cumulative[i - 1] + amounts[i]

labels = ['Чистая выручка\n(Доставленно)', 'Упущенная выручка\n(Отмены и возвраты)']
sizes = [clean_revenue, lost_revenue]
colors = ['#2e7d32', '#d32f2f']

sns.set_theme(style="white")

fig, ax = plt.subplots(figsize=(10,7), dpi=100)
fig.patch.set_facecolor('#f8f9fa')

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=140,
    pctdistance=0.7,
    textprops=dict(color='#212121', fontsize=11, fontweight='bold'),
    wedgeprops=dict(width=0.4, edgecolor="white", linewidth=3)
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_size(12)

center_text = f"Всего создано\nзаказов на: \n\n{total_revenue:,.0f}₽"
ax.text(0, 0, center_text, fontsize=12, fontweight='bold', color='#37474f', ha='center', va='center')

ax.set_title("Структура выручки интернет-магазина после очистки данных", fontsize=14, fontweight='bold', pad=25, color='#212121')

plt.tight_layout()
plt.show()
