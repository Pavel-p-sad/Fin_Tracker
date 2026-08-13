import json  # Вызвал модуль Json
import os # Проверю , есть ли файл
from datetime import datetime
# sp[0] - цель
# sp[1] - всего накоплений
# sp[2] - история
def save_data(per):
    with open("data.json", "w", encoding="utf-8") as file: 
     json.dump(per, file, ensure_ascii=False, indent=4)

def iron(): 
    print(f" Твоя цель {sp[0]['цель']} руб. \n")
    print(f" Накоплено уже : {sp[1]['всего']} руб. \n")
    ost = int(sp[0]['цель'] - sp[1]['всего'])
    print(f' Осталось накопить: {ost} \n')
    prog = sp[1]['всего'] / sp[0]['цель'] * 100
    print(f" Прогресс {prog} % \n\n")
    show_menu()

def get_yes_no (qwes):                                                            # Обрабатываю ответы 
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

def reset():
    while True:
        try:
            sp[0]["цель"] = int(input(" Ваша цель:  (руб.)\n\n\n"))
            while True:
                if sp[0]["цель"] == 0:
                    print( f" Пожалуйста укажи цель , отличную от '0' , сейчас твоя цель равна {sp[0]["цель"]}.руб")
                    sp[0]["цель"] = int(input(" Ваша цель:  (руб.)"))
                    save_data(sp)
                else:
                    break
            break
        except ValueError:
            print("Пожалуйста введите числовое значение")
    save_data(sp)


sp = [{"цель": "0", },
      {"всего": "0",},
      {"история": "[]"}]
if os.path.exists("data.json"):                                                # data - название файла с данными (проверили что файл существует)   
    with open ("data.json", "r", encoding="utf-8" ) as file:                   # открыли файл так как он существует
        sp = json.load(file)                                                   # загрузили данные из файла в список словарей sp (теперь он не 0 )
else:
    while True:
        try:
            sp[0]["цель"] = int(input("Ваша цель:  (руб.)"))                   # так как файла не существовало, меняю список н азначение цели
            break
        except ValueError:
            print("Пожалуйста введите числовое значение")
    with open("data.json", "w", encoding="utf-8") as file:                     # создаю файл так как его еще не существовало
     json.dump(sp, file, ensure_ascii=False, indent=4)                         # загружаю измененный список с целью в файл, только что созданный

print('                       ДОБРО ПОЖАЛОВАТЬ !!!             \n')
print(f"  Ваша цель: {sp[0]['цель']} руб.",end="                           "),  print(f'DATE:  ')
print(f"  Всего накоплений: {sp[1]['всего']} руб.  " '\n')
print('                             МЕНЮ !!!             \n')
show_menu()

while True:
    try:
        w = int(input(" "))
        if w == 1:
            while True:
                try:
                    qq = int(input('Введите сумму: (руб.)'))
                    popolnenie = qq + 0
                    break
                except ValueError:
                    print('Введите числовое значение!')
            qq = int(sp[1]['всего']) + qq
            sp[1]['всего'] = qq 
            save_data(sp)
            print('Изменения сохранены!')

            now = datetime.now().strftime("%d-%m-%Y %H:%M")
            sp[2]["история"].append({
                  "дата": now,
                  "сумма": popolnenie }) 

        elif w == 4:
            print(" ДО ВСТРЕЧИ!")
            input("                                    PRESS (Enter) , FOR OUT! ")
            save_data(sp)
            break

        elif w == 2:
            if int(sp[0]['цель']) == 0:
                print(" Цель еще не указана")
                reset()                
                while True:
                    if sp[0]["цель"] == 0:
                        print( f" Пожалуйста укажи цель , отличную от '0' , сейчас твоя цель равна {sp[0]["цель"]}.руб")
                        sp[0]["цель"] = int(input(" Ваша цель:  (руб.)"))
                        save_data(sp)
                    else:
                        iron()
                        break
            else:
                iron()

        elif w == 3:            
            if get_yes_no(" ВЫ УВЕРЕНЫ , ЧТО ХОТИТЕ СБРОСИТЬ ПРОГРЕСС?  (Y/N)"):                
                sp[0]['цель'] = 0
                sp[1]['всего'] = 0
                sp[2]["история"] = []
                save_data(sp)
                print(' данные сброшены ! \n\n\n')
                print(f"  Ваша цель: {sp[0]['цель']} руб.",end="                           "),  print(f'DATE: ')
                print(f"  Всего накоплений: {sp[1]['всего']} руб.  " '\n\n')
                print(f"  История пополнений пуста.")
                show_menu()                    
            else:
                print(' ok ')
                show_menu()
    
        elif w == 5:
            if int(sp[0]['цель']) > 0:
                while True:
                    if get_yes_no (" Вы уверены , что хотите перезаписать цель? Y/N"):
                        reset()
                        iron()
                        break
                    else:
                        print(" OK ")
                        show_menu()
                        break
            else:
                while True:
                    try:
                        sp[0]["цель"] = int(input(" Ваша цель:  (руб.)"))
                        break
                    except ValueError:
                        print("Пожалуйста введите числовое значение")
                save_data(sp)
        elif w == 6:
            if not sp[2]["история"]:
                print("История пополнений пуста.\n")
            else:
                print("\n--- История пополнений ---")
                for entry in sp[2]["история"]:
                    print(f"{entry['дата']}  |  {entry['сумма']} руб.")
                print(f" И ТОГО:          |  {sp[1]['всего']} руб. \n")
                print("----------------------------\n")
            show_menu()
        else:
            print('Пожалуйста введите числом из списка')
    except ValueError:
        print('Пожалуйста введите числом')

        