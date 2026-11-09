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

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(13, 7), dpi=100)

for i in range(len(steps)):
    if i == 0 or i == len(steps) - 1:
        color = "#1565c0" if i == 0 else "#2e7d32"
        ax.bar(steps[i], cumulative[i], color=color, width=0.5, edgecolor="black", linewidth=0.8)
        display_text = f"{cumulative[i]:,.0f} ₽"
        y_pos = cumulative[i] + total_revenue * 0.02
        text_color = "black"
    else:
        color = "#c62828"
        start_val = cumulative[i - 1]
        ax.bar(steps[i], amounts[i], bottom=start_val, color=color, width=0.5, edgecolor="black", linewidth=0.8)
        display_text = f"{amounts[i]:+,.0f} ₽"
        y_pos = start_val + amounts[i] / 2
        text_color = "white"

    ax.annotate(display_text, (i, y_pos), ha="center", va="center", fontsize=11, color=text_color, fontweight="bold")

for i in range(len(steps) -1):
    line_y = cumulative[i] if i == 0 else cumulative[i - 1] + amounts[i]
    ax.plot([i + 0.25, i + 0.75], [line_y, line_y], color="#37474f", linewidth=1.2, linestyle="--")

ax.set_title("Процесс очистки финансовых данных: от общего оборота к чистой выручке", fontsize=14, fontweight="bold", pad=25,
             color="#212121")

ax.set_ylabel('Сумма в рублях', fontsize=12)
ax.set_ylim(0, total_revenue * 1.15)

ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

sns.despine(left=True)

plt.tight_layout()
plt.show()
