import json                   # Вызвал модуль Json
import os                     # Проверю , есть ли файл
from datetime import datetime # Вызвал модуль дата время
import sqlite3                # Вызвал модуль базы данных
conn = sqlite3.connect("tracker.db") #  Подключиться к базе (если файла нет — он создастся)
cursor = conn.cursor()        # Создать курсор
# sp[0] - цель
# sp[1] - всего накоплений
# sp[2] - история
def save_data(per):
    with open("data.json", "w", encoding="utf-8") as file: 
     json.dump(per, file, ensure_ascii=False, indent=4)

def show_progress(): 
    print(f" Твоя цель {data['goal']} руб. \n")
    print(f" Накоплено уже : {data['total']} руб. \n")
    ost = int(data['goal'] - data['total'])
    print(f' Осталось накопить: {ost} \n')
    prog = data['total'] / data['goal'] * 100
    print(f" Прогресс {round(prog,2)} % \n\n")
    show_menu()

def get_yes_no (qwes):  # Обрабатываю ответы 
    while True:
        q1 = input(qwes)
        if q1 == 'Y' or q1 == 'y' or q1 == 'н' or q1 == 'Н' :
            return True
        elif q1 == 'N' or q1 == 'n' or q1 == 'т' or q1 == 'Т' :
            return False
        else:
            print(' Пожалуйста введите  Y/N ')

def show_menu():
    print("1.Внести сумму     2.Показать прогресс    3.Сброс    4.Выйти    5.Обновить цель  6.История " '\n\n\n\n')

def reset_goal():
    while True:
        try:
            data["goal"] = int(input(" Ваша цель:  (руб.)\n\n\n"))
            while True:
                if data["goal"] == 0:
                    print( f" Пожалуйста укажи цель , отличную от '0' , сейчас твоя цель равна {data["goal"]}.руб")
                    data["goal"] = int(input(" Ваша цель:  (руб.)"))
                    save_data(data)
                else:
                    break
            break
        except ValueError:
            print("Пожалуйста введите числовое значение")
    save_data(data)


cursor.execute("""CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER,
    date TEXT,
    comment TEXT                                 )""")      
conn.commit()

data ={"goal": 0,
       "total": 0,
       "history": [] ,}
if os.path.exists("data.json"):                                                 # data - название файла с данными (проверили что файл существует)   
    with open ("data.json", "r", encoding="utf-8" ) as file:                    # открыли файл так как он существует
        data = json.load(file)                                                    # загрузили данные из файла в список словарей sp (теперь он не 0 )
else:
    while True:
        try:
            data["goal"] = int(input("Ваша цель:  (руб.)"))                    # так как файла не существовало, меняю список н азначение цели
            break
        except ValueError:
            print("Пожалуйста введите числовое значение")
    with open("data.json", "w", encoding="utf-8") as file:                      # создаю файл так как его еще не существовало
     json.dump(data, file, ensure_ascii=False, indent=4)                          # загружаю измененный список с целью в файл, только что созданный

print('                       ДОБРО ПОЖАЛОВАТЬ !!!             \n')
print(f"  Ваша цель: {data['goal']} руб.",end="                           "),  print(f'DATE:  ')
print(f"  Всего накоплений: {data['total']} руб.  " '\n')
print('                             МЕНЮ !!!             \n')
show_menu()

while True:
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        w = int(input(" "))
        if w == 1:
            while True:
                try:
                    amount = int(input('Введите сумму: (руб.)'))
                    deposit = amount + 0
                    break
                except ValueError:
                    print('Введите числовое значение!')
            amount = int(data['total']) + amount
            data['total'] = amount 
            save_data(data)                                                                  # занесли данные в Json
            print('Изменения сохранены!')
            data["history"].append({                                                      # Занесли данные в список
                  "дата": now,
                  "сумма": deposit }) 
            cursor.execute("INSERT INTO history (amount, date, comment) VALUES (?, ?, ?)", # Занесли данные в базу SQLite
               (deposit, now, "пополнение"))
            conn.commit()
        elif w == 4:
            print(" ДО ВСТРЕЧИ!")
            input("                                    PRESS (Enter) , FOR OUT! ")
            conn.close()
            save_data(data)
            break

        elif w == 2:
            if int(data['goal']) == 0:
                print(" Цель еще не указана")
                reset_goal()                
                while True:
                    if data["goal"] == 0:
                        print( f" Пожалуйста укажи цель , отличную от '0' , сейчас твоя цель равна {data["goal"]}.руб")
                        data["goal"] = int(input(" Ваша цель:  (руб.)"))
                        save_data(data)
                    else:
                        show_progress()
                        break
            else:
                show_progress()

        elif w == 3:            
            if get_yes_no(" ВЫ УВЕРЕНЫ , ЧТО ХОТИТЕ СБРОСИТЬ ПРОГРЕСС?  (Y/N)"):                
                data['goal'] = 0
                data['total'] = 0
                data["history"] = []
                cursor.execute("DELETE FROM history")
                conn.commit()
                save_data(data)
                print(' данные сброшены ! \n\n\n')
                print(f"  Ваша цель: {data['goal']} руб.",end="                           "),  print(f'DATE:{datetime.now().strftime("%Y-%m-%d %H:%M")}')
                print(f"  Всего накоплений: {data['total']} руб.  " '\n\n')
                print(f"  История пополнений пуста.")
                show_menu()                    
            else:
                print(' ok ')
                show_menu()
    
        elif w == 5:
            if int(data['goal']) > 0:
                while True:
                    if get_yes_no (" Вы уверены , что хотите перезаписать цель? Y/N"):
                        reset_goal()
                        show_progress()
                        break
                    else:
                        print(" OK ")
                        show_menu()
                        break
            else:
                while True:
                    try:
                        data["goal"] = int(input(" Ваша цель:  (руб.)"))
                        break
                    except ValueError:
                        print("Пожалуйста введите числовое значение")
                save_data(data)
        elif w == 6:
            while True:
                try:
                    choise = int(input(" 1.Показать историю   2.сумма за месяц   3.Общая сумма   4. очистить историю   5.Вернуться в главное меню   6.История '.Json' \n"))
                except ValueError:
                    print("Пожалуйста введите числом")
                if choise == 1:
                    cursor.execute("SELECT * FROM history ORDER BY date DESC LIMIT 100")
                    back = cursor.fetchall()
                    if not back:
                        print(" История пуста.\n")
                    else:
                        print("\n--- История пополнений (SQLite) ---")
                        for row in back:
                            print(f"{row[2]}  |  {row[1]} руб. | {row[3]}")
                        print("------------------------------------\n")
                elif choise == 2:
                    while True:
                        try:
                            month_choise = input("За какой месяц вы хотите посмотреть историю? '0000-00\n")
                            if len(month_choise) != 7 or month_choise[4] != "-":
                                print("Не верный формат, укажите формат '0000-00' \n")
                            else:
                                cursor.execute("SELECT * FROM history WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC", (month_choise,))
                                month_choise_con = cursor.fetchall()
                                if not month_choise_con:
                                    print(f" История за {month_choise} пуста.\n")
                                    break
                                else:
                                    month_summ = sum(row[1] for row in month_choise_con)
                                    print(f"-------- История за {month_choise} 'SQLite' ---------")
                                    for row in month_choise_con:
                                        print(f"дата :{row[2]} сумма :{row[1]}руб. {row[3]}")
                                        print(f"Общая сумма за месяц {month_summ} руб.")
                                    print(f"------------------------------------------------------")

                                    break
                        except Exception as e:
                            print("Ошибка при выполнении запроса:", e + "\n")
                elif choise == 3:
                    cursor.execute("SELECT SUM(amount) FROM history")
                    total = cursor.fetchone()[0]
                    if total is None:
                        print(" Сумма пополнений '0' руб.\n")
                    else:
                        print(f" Сумма пополнений = {total} руб.\n")

                elif choise == 4:
                    if get_yes_no(" ВЫ УВЕРЕНЫ , ЧТО ХОТИТЕ СБРОСИТЬ ИСТОРИЮ?  (Y/N)"):
                        cursor.execute("DELETE FROM history")
                        conn.commit()
                        data["history"] = []
                        print("История очищена.\n")
                    else:
                        print("OK")
                elif choise == 5:
                    print("OK")
                    show_menu()
                    break                 
                elif choise == 6:
                    if not data["history"]:
                        print("История пополнений пуста.\n")
                    else:
                        print("\n--- История пополнений ---")
                        for entry in data["history"]:
                            print(f"{entry['дата']}  |  {entry['сумма']} руб.")
                        print(f" И ТОГО:          |  {data['total']} руб. \n")
                        print("----------------------------\n")
                else:
                    print("Пожалуйста введите числом из списка")
        else:
            print('Пожалуйста введите числом из списка')
    except ValueError:
        print('Пожалуйста введите числом')

        