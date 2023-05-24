from customtkinter import CTk, CTkButton, CTkTextbox, CTkProgressBar, CTkLabel
from tkinter.filedialog import askdirectory
from utils import compress_to_osz
import threading


class AppWindow:
    def __init__(self, master):
        # Название программы
        self.master = master
        master.title("BeatmapsToOsz")

        # Размер приложения
        width = 590
        height = 300
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # width x height  x+y размещение по центру экрана
        master.geometry(
            "{}x{}+{}+{}".format(width, height, screen_width // 2 - width // 2, screen_height // 2 - height // 2))
        master.resizable(False, False)

        # Виджеты
        label1 = CTkLabel(master, text="Choose osu folder")
        label1.grid(padx=2, pady=4, column=0, row=0)

        self.text1 = CTkTextbox(master, height=12, width=400)
        self.text1.grid(row=1, column=0, padx=10)

        self.button1 = CTkButton(master, text="Choose")
        self.button1.bind("<Button-1>", lambda event: self.open_folder_dialog(event))
        self.button1.grid(row=1, column=1, padx=10)

        label2 = CTkLabel(master, text="Choose osu output folder")
        label2.grid(padx=2, pady=4, column=0, row=2)

        self.text2 = CTkTextbox(master, height=12, width=400)
        self.text2.grid(row=4, column=0, padx=10)

        self.button2 = CTkButton(master, text="Choose")
        self.button2.bind("<Button-1>", lambda event: self.open_folder_dialog(event))
        self.button2.grid(row=4, column=1, padx=10)

        # Todo: Сделать рабочий прогресс бар
        # self.progress_bar = CTkProgressBar(master, height=10, width=400)
        # self.progress_bar.grid(pady=25)

        # Todo:
        #  1. Центрировать кнопку, а то выглядит не очень
        #  2. Обработка ошибок, такие как "Неверный путь до папки songs", "Существование конечной папки"
        #  и другие если появятся
        self.button3 = CTkButton(master, text="Start", command=self.start_process)
        self.button3.grid(pady=40)

        # Todo: Переключение тем(почему бы и нет)

    def open_folder_dialog(self, event):
        widget = "." + str(event.widget).split(".")[1]
        folder_path = askdirectory()

        if widget == str(self.button1):
            self.text1.delete(1.0, "end")
            self.text1.insert(0.0, folder_path)
        elif widget == str(self.button2):
            self.text2.delete(1.0, "end")
            self.text2.insert(0.0, folder_path)
        else:
            print("Что это?")

    def start_process(self):
        self.button3.configure(state="disabled")

        songs_path = self.text1.get(0.0, "end").strip().replace('\n', '')
        output_path = self.text2.get(0.0, "end").strip().replace('\n', '')

        # Запустить функцию compress_to_osz в отдельном потоке
        threading.Thread(target=self.compress_to_osz_thread, args=(songs_path, output_path)).start()

    def compress_to_osz_thread(self, songs_path, output_path):
        compress_to_osz(songs_path, output_path)

        # Вернуться в главный поток для обновления интерфейса
        self.master.after(0, self.enable_button)

    def enable_button(self):
        self.button3.configure(state="normal")


def main():
    app = CTk()
    converter = AppWindow(app)
    app.mainloop()


if __name__ == "__main__":
    main()
