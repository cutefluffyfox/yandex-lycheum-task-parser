from json import load, dump
import pyautogui
import keyboard


def rewrite(key: str):
    with open('cords.json', 'r', encoding='UTF-8') as file:
        json_file = load(file)
    json_file[key] = (*pyautogui.position(),)
    with open('cords.json', 'w', encoding='UTF-8') as file:
        dump(json_file, file, indent=4)


print('День добрый, это помощник по скачиванию кода с Яндекса')
print('Перед тем, как приступить, надо будет дать программе понять где у вас что находится')
print('Откройте браузер и войдите в Яндекс.Лицей (!важно чтобы вы это делали в браузере, который стоит по умолчанию, и чтобы это была последняя вкладка!)')
print('Нажмите ctrl+shift+i и наведите на строчку html: <html lang="ru" data-rh="lang"> и нажмите клавишу 1')
print('Наведите теперь на вкладку эту в браузере на значёк "закрыть" и нажмите клавишу 2')
print('Закройте эту вкладку эту в браузере и наведите на значёк PyCharm, нажмите на клавишу 3')
print('Откройте в PyCharm файл yandex.html и нажмите наведите мышь по середине файла, нажмите клавишу 4 (эта 4 в файле ни на что не повлияет)')
print('После того, как вы всё это сделали, мы можете нажать shift+tab')
run = True
while run:
    if keyboard.is_pressed('shift+tab'):
        run = False
    if keyboard.is_pressed('1'):
        rewrite('HTML')
    if keyboard.is_pressed('2'):
        rewrite('TAB')
    if keyboard.is_pressed('3'):
        rewrite('PYCHARM')
    if keyboard.is_pressed('4'):
        rewrite('YANDEX')
print('Все координаты сохранены, можете запускать yandex_parser.py')
