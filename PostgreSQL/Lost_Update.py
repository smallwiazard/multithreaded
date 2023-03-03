import psycopg2 as ps2   # для взаємодії з базою даних
from psycopg2 import Error

import threading as t
import time

# функція-каунтер
def increment():
    cursor_in_thread = klient_connection.cursor()
    for i in range(0, 10000):
        cursor_in_thread.execute("SELECT counter FROM user_counter WHERE id =1")
        counter = cursor_in_thread.fetchone()
        counter = counter[0] + 1
        cursor_in_thread.execute("UPDATE user_counter set counter = %s WHERE id = %s", (counter, 1))
        klient_connection.commit()


START_time = time.time()
START_values = (1,0,0)
try:
    # з'єднання з базою даних
    klient_connection = ps2.connect(database="Olga_database", user="postgres", password="0000", host="127.0.0.1", port="5432")
    cursor = klient_connection.cursor()
    print("Connected")
    # створюється табличка та додаються значення за замовчуванням
    cursor.execute("CREATE TABLE IF NOT EXISTS user_counter (id INT, counter  INT  , version  INT ); ")
    cursor.execute("INSERT INTO user_counter (id, counter,version) Values(%s,%s,%s)",(START_values))
    klient_connection.commit()

    threads = []
    for i in range(0, 10):                      # запуск функції у 10 потоках
        thread = t.Thread(target=increment)
        threads.append(thread)
        thread.start()
    for i in threads:
        i.join()
    # вивід результату
    cursor.execute("SELECT counter FROM User_Counter WHERE id = 1")
    print(cursor.fetchone())
except(Exception, Error ) as error:
    print("Error", error)
finally:
    if klient_connection:
        cursor.close()
        klient_connection.close()
execution_time = str((time.time() - START_time))
print("Execution time:" + execution_time)
