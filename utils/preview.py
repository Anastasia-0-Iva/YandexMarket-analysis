import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\vatso\PycharmProjects\Yandex\utils\Yandex.xlsx') #Датафрейм

df_columns = df.columns.tolist() # ['price', 'purchases', 'rating', 'title']
df_cleaned = df[df['price'] > 100] # Очищенные цены

# Обработка 'title'
check_title = sorted(df_cleaned['title'].unique()) # Все производители
count_title = df_cleaned['title'].nunique() # Кол-во уникальных производителей 30
frequency = df_cleaned['title'].value_counts() # Периодичность появления в датафрейме товара конкретного производителя
total_title = df_cleaned['title'].count() # Всего позиций в колонке производителей 542
percent_frequency_title = round(frequency / total_title * 100, 2).sort_values() # Процентное соотношение производителей


# Обработка 'price'
check_price = sorted(df['price']) # Присутствуют цены в 1р и 2р (Перенесла строку с очищенными данными в начало скрипта)
sep_price = df_cleaned.groupby('title')['price'].agg(['min', 'max', 'sum', 'count', 'mean']) # Общая информация по всем производителям
sort_price = sep_price['mean'].sort_values() # Сортировка средней цены по всем производителям
total_price = df_cleaned['price'].sum() # Общая сумма по всему датафрейму 230959р.
mean_price = df_cleaned['price'].mean() # Средний показатель цены по всему датафрейму 426.12р.
sep_percent_price = round((sep_price['sum'] / total_price) * 100, 2).sort_values() # Процентное соотношение сумм


# Обработка 'purchases'
check_purchases = sorted(df_cleaned['purchases']) # Ok
sep_purchases = df_cleaned.groupby('title')['purchases'].agg(['min', 'max', 'sum', 'count', 'mean']) # Общая информация по всем производителям
sort_purchases = sep_purchases['mean'].sort_values() # Сортировка среднего кол-ва покупок по производителю
total_purchases = df_cleaned['purchases'].sum() # Общее кол-во покупок по всему датафрейму 48211
mean_purchases = df_cleaned['purchases'].mean() # Средний показатель покупок по всему датафрейму 88.95
sep_percent_purchases = round(sep_purchases['sum'] / total_purchases * 100, 2).sort_values() # Процент покупок каждой фирмы от общего кол-ва покупок


# Обработка 'rating'
check_rating = sorted(df_cleaned['rating']) # Ok
sep_rating = df_cleaned.groupby('title')['rating'].agg(['min', 'max', 'count', 'mean']) # Общая информация по всем производителям
sort_rating = sep_rating['mean'].sort_values() # Сортировка средних оценок по производителю
total_mean = df_cleaned['rating'].mean() # Средняя оценка по всему датафрейму 4.7
count_unique_rating = df_cleaned['rating'].value_counts() # Кол-во уникальных оценок
total_count_unique_rating = df_cleaned['rating'].count() # Кол-во всех оценок 542
percent_unique_rating = round(count_unique_rating / total_count_unique_rating * 100, 2) # Процентное соотношение всех уникальных оценок


# Корреляции
corr_price_rating = df_cleaned['price'].corr(df_cleaned['rating']) # 0.01 - низкая (цена/оценка)
corr_price_purchases = df_cleaned['price'].corr(df_cleaned['purchases']) # -0.1 - низкая отрицательная (цена/покупки)
corr_rating_purchases = df_cleaned['rating'].corr(df_cleaned['purchases']) # 0.01 - низкая (оценка/покупки)

worse = df_cleaned[df_cleaned['rating'] < 4.0]
corr_worse_price = worse['price'].corr(worse['purchases']) # -0.2 - низкая отрицательная (низкая оценка: цена/покупки)

perfect = df_cleaned[df_cleaned['rating'] == 5.0]
corr_perfect_price = perfect['price'].corr(perfect['purchases']) # -0.1 - низкая отрицательная (высокая оценка: цена/покупки)

# ТОП-10 брендов по продажам
top_10 = sep_purchases['sum'].sort_values(ascending=False).head(10)

#--------------------СОХРАНЯЕМ_АГРЕГИРОВАННЫЕ_ДАННЫЕ-----------------

# Таблица
final_table = pd.DataFrame({
    'Бренд': sep_price.index,
    'Средняя цена': sep_price['mean'],
    'Средняя оценка': sep_rating['mean'],
    'Среднее кол-во покупок': sep_purchases['mean']
})

final_table.to_excel('final_table.xlsx', index=False)

#--------------------ВИЗУАЛИЗАЦИЯ-------------------------

# Доля производителей в датафрейме
#categories = percent_frequency_title.index
#value = percent_frequency_title.values
#colors = ['#1F4E79']
#plt.barh(categories, value, color=colors)
#plt.xlabel('Доля')
#plt.title('Доля производителей на датафрейм')
#plt.tight_layout()
#plt.tick_params(labelsize=8)
#plt.show()

# Доля "живых" производителей в датафрейме
#cleared_df = percent_frequency_title[percent_frequency_title.index != 'Бренд не указан']
#categories = cleared_df.index
#value = cleared_df.values
#colors = ['#1F4E79']
#plt.barh(categories, value, color=colors)
#plt.xlabel('Доля')
#plt.title('Доля "живых" производителей на датафрейм')
#plt.tight_layout()
#plt.tick_params(labelsize=8)
#plt.show()

# Процент средней стоимости товара каждого производителя
#categories = sep_percent_price.index
#value = sep_percent_price.values
#colors = ['#1F4E79']
#plt.barh(categories, value, color=colors)
#plt.xlabel('Доля')
#plt.title('Процент средней стоимости товара каждого производителя')
#plt.tight_layout()
#plt.tick_params(labelsize=8)
#plt.show()

# Процент средней стоимости товара каждого производителя ("живые")
#cleared_df = sep_percent_price[sep_percent_price.index != 'Бренд не указан']
#categories = cleared_df.index
#value = cleared_df.values
#colors = ['#1F4E79']
#plt.barh(categories, value, color=colors)
#plt.xlabel('Доля')
#plt.title('Процент средней стоимости товара каждого производителя ("живые")')
#plt.tight_layout()
#plt.tick_params(labelsize=8)
#plt.show()

# Среднее кол-во покупок по производителю
#categories = sep_percent_purchases.index
#value = sep_percent_purchases.values
#colors = ['#1F4E79']
#plt.barh(categories, value, color=colors)
#plt.xlabel('Доля')
#plt.title('Среднее кол-во покупок по каждому производителю')
#plt.tight_layout()
#plt.tick_params(labelsize=8)
#plt.show()

# Среднее кол-во покупок по каждому "живому" производителю
#cleared_df = sep_percent_purchases[sep_percent_purchases.index != 'Бренд не указан']
#categories = cleared_df.index
#value = cleared_df.values
#colors = ['#1F4E79']
#plt.barh(categories, value, color=colors)
#plt.xlabel('Доля')
#plt.title('Среднее кол-во покупок по каждому "живому" производителю')
#plt.tight_layout()
#plt.tick_params(labelsize=8)
#plt.show()

# Корреляция цены и оценок
#plt.scatter(df_cleaned['price'], df_cleaned['rating'], alpha=0.2, color='#1F4E79')
#plt.xlabel('Цена')
#plt.ylabel('Оценка')
#plt.title('Корреляция цена/оценка')
#plt.show()

# Корреляция цены и покупок
#plt.scatter(df_cleaned['price'], df_cleaned['purchases'], alpha=0.2, color='#1F4E79')
#plt.xlabel('Цена')
#plt.ylabel('Покупки')
#plt.title('Корреляция цена/покупки')
#plt.show()

# Корреляция оценок и покупок
#plt.scatter(df_cleaned['rating'], df_cleaned['purchases'], alpha=0.2, color='#1F4E79')
#plt.xlabel('Оценка')
#plt.ylabel('Покупки')
#plt.title('Корреляция оценки/покупки')
#plt.show()

# Корреляция (низкий рейтинг) - цена и покупки
#cleared_df = df_cleaned[df_cleaned['rating'] < 4.0]
#plt.scatter(cleared_df['price'], cleared_df['purchases'], alpha=0.5, color='#1F4E79')
#plt.xlabel('Цена')
#plt.ylabel('Покупки')
#plt.title('Корреляция цена/покупки (низкий рейтинг)')
#plt.show()

# Корреляция (высокий рейтинг) - цена и покупки
#cleared_df = df_cleaned[df_cleaned['rating'] == 5.0]
#plt.scatter(cleared_df['price'], cleared_df['purchases'], alpha=0.5, color='#1F4E79')
#plt.xlabel('Цена')
#plt.ylabel('Покупки')
#plt.title('Корреляция цена/покупки (высокий рейтинг)')
#plt.show()