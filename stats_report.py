import sqlite3
import pandas as pd

# Соединение с БД
conn = sqlite3.connect('messages.db')
c = conn.cursor()

def get_statistics():
    # Извлечение данных из БД
    df = pd.read_sql_query('SELECT * FROM messages', conn)

    # Конвертация timestamp в datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Статистика по дням
    daily_stats = df.groupby(df['timestamp'].dt.date).size().reset_index(name='count')

    # Статистика по юзерам
    user_stats = df['user'].value_counts().reset_index(name='count')

    # Статистика по командам бота
    command_stats = df['command'].value_counts().reset_index(name='count')

    return daily_stats, user_stats, command_stats

daily_stats, user_stats, command_stats = get_statistics()

# Сохранение статистики в Excel-файл
with pd.ExcelWriter('statistics.xlsx') as writer:
    daily_stats.to_excel(writer, sheet_name='Daily Statistics', index=False)
    user_stats.to_excel(writer, sheet_name='User Statistics', index=False)
    command_stats.to_excel(writer, sheet_name='Command Statistics', index=False)

print("Статистика успешно сохранена в файл statistics.xlsx.")
