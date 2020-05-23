from bs4 import BeautifulSoup
from os import mkdir, chdir, getcwd, listdir
from os.path import join
from webbrowser import open as web_open
from time import sleep
import pyautogui
import keyboard
from json import load


def make_dir(dir_name: str):
    if dir_name not in listdir(getcwd()):
        mkdir(dir_name.translate(translator))


def fill_html(link: str):
    """Заполняет html файл по ссылке"""
    if keyboard.is_pressed('ctrl'):
        exit()
    web_open(link)
    with open(cords_path, 'r', encoding='UTF-8') as file:
        json_file = load(file)
        assert json_file.get('HTML') is not None, 'Вначале запустите __init__.py'
        assert json_file.get('TAB') is not None, 'Вначале запустите __init__.py'
        assert json_file.get('PYCHARM') is not None, 'Вначале запустите __init__.py'
        assert json_file.get('YANDEX') is not None, 'Вначале запустите __init__.py'
        sleep(4)  # ждём загрузки страницы
        keyboard.press_and_release('ctrl+shift+i')
        sleep(1)  # ждём загрузки html
        pyautogui.moveTo(*json_file['HTML'])
        pyautogui.click(button='left')
        sleep(0.5)
        keyboard.press_and_release('ctrl+c')  # копируем html
        pyautogui.moveTo(*json_file['TAB'])
        pyautogui.click(button='left')  # закрываем вкладку
        pyautogui.moveTo(*json_file['PYCHARM'])
        pyautogui.click(button='left')  # открываем PyCharm
        sleep(0.5)
        pyautogui.moveTo(*json_file['YANDEX'])
        pyautogui.click(button='left')
        keyboard.press_and_release('ctrl+A')
        keyboard.press_and_release('backspace')
        keyboard.press_and_release('ctrl+v')
        sleep(0.5)
        keyboard.press_and_release('ctrl+s')  # записываем всё в файл и сохраняем
        sleep(2)


def parse_task(task_url: str) -> str:
    fill_html(task_url)
    with open('../../../yandex.html', 'r', encoding='UTF-8') as task_page:
        bs = BeautifulSoup(task_page.read(), features='lxml')
    code = '\n'.join([line_of_code.text for line_of_code in bs.find_all('pre', attrs={'class': 'CodeMirror-line'})])
    download_link = bs.find_all('a', attrs={'class': 'Link Link_behavior_external Link_theme_normal Link_view_lyceum source-code-viewer__download-link'})
    if download_link and not code:
        download_link = download_link[0]['href']
        print('Функционал не позволяет скачать архив, так что прийдётся лапками:', download_link)
        print('Путь для сохранения:', getcwd())
        return ''
    else:
        return code.replace('​', '')


def parse_lesson(lesson_url: str, lesson_title: str):
    fill_html(lesson_url)
    with open('../yandex.html', 'r', encoding='UTF-8') as lesson_page:
        bs = BeautifulSoup(lesson_page.read(), features='lxml')
    make_dir(lesson_title)
    chdir(lesson_title)
    for task_group in bs.find_all('ul', attrs={'class': 'Accordion-Group'}):
        group_type = task_group.find_all('h3', attrs={'class': 'heading heading_level_3 task-group-header__heading'})[0].text
        make_dir(group_type)
        chdir(group_type)
        for task in task_group.find_all('a', href=True):
            task_title = task.h4.text.rstrip('РУЧ').translate(translator)
            task_url = HOST + task['href']
            with open(task_title + '.py', 'w', encoding='UTF-8') as file:
                file.write(parse_task(task_url))
        chdir('..')
    chdir('..')


def parse_main():
    fill_html(YEAR_TO_DOWNLOAD)
    with open('../yandex.html', 'r', encoding='UTF-8') as main_page:
        bs = BeautifulSoup(main_page.read(), features='lxml')
    for lesson in bs.find_all('li', attrs={'class': 'link-list__item'}):
        lesson_url = HOST + lesson.find_all('a', href=True)[0]['href']
        lesson_title = lesson.h4.text
        parse_lesson(lesson_url, lesson_title)


# Заполнить данные тут
YEAR_TO_DOWNLOAD = '<LINK TO DOWNLOAD>'  # ссылка на главную страницу курса
# Заполнить данные тут


HOST = 'https://lyceum.yandex.ru'
cords_path = join(getcwd(), 'cords.json')
make_dir('yandex')
chdir('yandex')
translator = str.maketrans({elem: None for elem in '/\\|?*:<>«»'})  # запрещённые символы в создании файла
print('Откройте в PyCharm файл yandex.html и нажмите 1. Запустится скачивание файлов')
print('Чтобы прервать скачивание нажмите и держите ctrl')
print('Некоторые файлы могут не скачаться в связи с чем-то, что мне лень дебажить. Так что после прийдётся всё перепроверить')
wait = True
while wait:
    if keyboard.is_pressed('1'):
        wait = False
print('Началось скачивание')
parse_main()
