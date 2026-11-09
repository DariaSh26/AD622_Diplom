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

print(f"Общая сумма заказов (включая отмены): {total_revenue:,.2f} руб.")
print(f"Реальная очищенная выручка компании: {clean_revenue:,.2f} руб.")
print(f"Отсеяно из-за отмен и возвратов: {lost_revenue:,.2f} руб.")

sns.set_theme(style="white")
fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), dpi=100)
fig.patch.set_facecolor('#f8f9fa')

kpis = [
    {"title": "ОБЩИЙ ОБЪЕМ ЗАКАЗОВ\n(Грязные данные)", "value": f"{total_revenue:,.0f} ₽", "color": "#1565c0", "bg": "#e3f2fd"},
    {"title": "РЕАЛЬНАЯ ВЫРУЧКА\n(Чистые деньги)", "value": f"{clean_revenue:,.0f} ₽", "color": "#2e7d32", "bg": "#e8f5e9"},
    {"title": "ОТСЕЯНО ПРИ ОЧИСТКЕ\n(Отмены и возвраты)", "value": f"{lost_revenue:,.0f} ₽", "color": "#c62828", "bg": "#ffebee"},
]

for i, kpi in enumerate(kpis):
    ax = axes[i]
    ax.set_facecolor(kpi["bg"])

    for spine in ax.spines.values():
        spine.set_color(kpi["color"])
        spine.set_linewidth(1.5)

    ax.text(0.5, 0.75, kpi["title"], ha="center", va="center", fontsize=11, fontweight="bold", color="#37474f")
    ax.text(0.5, 0.35, kpi["value"], ha="center", va="center", fontsize=24, fontweight="bold", color=kpi["color"])

    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.show()