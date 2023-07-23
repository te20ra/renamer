import os
from tkinter import Tk, Button, filedialog, Label
from natsort import os_sorted
from tkinter import messagebox as mb
import pyperclip

FOLDER_PATH = ''
OLD_FILE_NAMES = []
NEW_FILE_NAMES = []
FILE_EXTENSION = []

#функция для проверки наличия недпосутимых символов в имени файла
def check_character_in_string(string):
    characters = '\/:*?"<>|'
    for character in characters:
        if character in string:
            return character
    return 'True'

#функция для вывода имени файла
def shortcut_name(name):
    shortname = name[name.rfind('/')+1:]
    if len(shortname) < 30:
        return shortname
    else:
        shortname = shortname[:13] + '...' + shortname[-13:]
        return shortname


#функция для выбора папки и копирования имен файолов в буфер обмена
def open_files_path():
    global FOLDER_PATH, OLD_FILE_NAMES, FILE_EXTENSION
    FOLDER_PATH = filedialog.askdirectory()
    label_folder_path.configure(text=f'Выбран путь: {FOLDER_PATH}')
    label_txt.configure(text='')
    label_status.configure(text='')
    OLD_FILE_NAMES.clear()
    OLD_FILE_NAMES += os_sorted(os.listdir(FOLDER_PATH))
    str_names = ''
    for i in range(len(OLD_FILE_NAMES)):
        name = OLD_FILE_NAMES[i]
        FILE_EXTENSION.append(name[name.rfind('.'):])
        name = name[:name.rfind('.')]
        str_names += name + '\n'
    str_names = str_names[:-1]
    pyperclip.copy(str_names)
    mb.showinfo(title="Информация", message="Имена файлов скопированы в буфер обмена")

#функция для выбора txt файла и проверки его на правильность
def open_file_txt():
    global FOLDER_PATH, NEW_FILE_NAMES
    if FOLDER_PATH == '':
        mb.showerror(title="Ошибка", message=f'Сначала необходимо выбрать папку')
        return
    txt_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    short_txt = shortcut_name(txt_path)
    label_txt.configure(text=f'Выбран txt файл: {short_txt}')
    try:
        with open(txt_path, 'r') as f:
            NEW_FILE_NAMES = f.read().splitlines()
    except FileNotFoundError:
        mb.showerror(title="Ошибка", message=f'Файл не найден')
        label_txt.configure(text="Файл не выбран")
        return
    if len(NEW_FILE_NAMES) != len(os.listdir(FOLDER_PATH)):
        mb.showerror(title="Ошибка", message=f'Количество файлов в папке и количество строк в текстовом файле не совпадают')
        label_txt.configure(text="Файл не выбран")
        return
    for name in NEW_FILE_NAMES:
        check = check_character_in_string(name)
        if check != "True":
            mb.showerror(title="Ошибка", message=f'В имени файла {name} содержиться запрещенный символ "{check}"\nИсправте и выберите файл заново')
            return

#функция для непосредственного переименовывания файлов
def start():
    global OLD_FILE_NAMES, FOLDER_PATH, FILE_EXTENSION, NEW_FILE_NAMES
    if FOLDER_PATH == '' or len(NEW_FILE_NAMES) == 0:
        mb.showerror(title="Ошибка", message=f'Необходимо выбрать папку и файл txt')
        return
    for old_name, new_name, extension in zip((OLD_FILE_NAMES), NEW_FILE_NAMES, FILE_EXTENSION):
        old_file_path = os.path.join(FOLDER_PATH, old_name)
        new_name += extension
        new_file_path = os.path.join(FOLDER_PATH, new_name)
        os.rename(old_file_path, new_file_path)
    label_status.configure(text=f'Выполнено')
    OLD_FILE_NAMES.clear()
    FILE_EXTENSION.clear()
    NEW_FILE_NAMES.clear()
    FOLDER_PATH = ''

root = Tk()
root.title("Renamer")
root.geometry("600x150")
for c in range(10): root.columnconfigure(index=c, weight=10)
for r in range(10): root.rowconfigure(index=r, weight=5)

label_folder_path = Label(root, text=f'Путь не выбран')
label_folder_path.grid(column=1, row=0)

label_txt = Label(root, text=f'Файл txt не выбран')
label_txt.grid(column=1, row=1)

label_status = Label(root, text="")
label_status.grid(column=1, row=2)

button_select_folder = Button(root, text="Выбрать папку", command=open_files_path)
button_select_folder.grid(column=0, row=0)

button_select_file = Button(root, text="Выбрать txt файл", command=open_file_txt)
button_select_file.grid(column=0, row=1)

button_start = Button(root, text='Выполнить', command=start)
button_start.grid(column=0, row=2)

root.mainloop()