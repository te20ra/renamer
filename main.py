import os
from tkinter import Tk, Button, filedialog

def sort_list(lst):
    return sorted(lst, key=lambda x: ''.join(sorted(x)))
def rename_files():
    folder_path = filedialog.askdirectory()
    txt_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    try:
        with open(txt_path, 'r') as f:
            file_names = f.read().splitlines()
    except FileNotFoundError:
        print("Файл не найден")
        return

    if len(file_names) != len(os.listdir(folder_path)):
        print("Количество файлов в папке и количество строк в текстовом файле не совпадают")
        return

    for filename, new_name in zip(os.listdir(folder_path), file_names):
        file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_name)
        os.rename(file_path, new_file_path)

    spisok_name = os.listdir(folder_path)
    print(spisok_name)
    print("________________")
    spisok_name.sort(key=len)
    spisok_len = []
    for i in range(len(spisok_name)):
        spisok_len.append(len(spisok_name[i]))
    spisok_dict = {'name': spisok_name,
                   'lenght': spisok_len}
    print("________________")
    print(spisok_dict)




root = Tk()
root.title("Переименование файлов")
button_select_folder = Button(root, text="Выберите папку", command=rename_files)
button_select_folder.pack()
root.mainloop()
