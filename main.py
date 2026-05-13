import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ---------------------- Файл ---------------------- #

DATA_FILE = "trainings.json"

trainings = []

# ---------------------- Функции ---------------------- #

def add_training():
    date = date_entry.get().strip()
    training_type = type_entry.get().strip()
    duration = duration_entry.get().strip()

    # Проверка пустых полей
    if not date or not training_type or not duration:
        messagebox.showerror(
            "Ошибка",
            "Все поля должны быть заполнены!"
        )
        return

    # Проверка даты
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Ошибка",
            "Дата должна быть в формате YYYY-MM-DD!"
        )
        return

    # Проверка длительности
    try:
        duration_value = int(duration)

        if duration_value <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Ошибка",
            "Длительность должна быть положительным числом!"
        )
        return

    training = {
        "date": date,
        "type": training_type,
        "duration": duration_value
    }

    trainings.append(training)

    update_table(trainings)
    save_trainings()
    clear_fields()

    messagebox.showinfo(
        "Успех",
        "Тренировка добавлена!"
    )


def update_table(data):
    table.delete(*table.get_children())

    for training in data:
        table.insert(
            "",
            tk.END,
            values=(
                training["date"],
                training["type"],
                f'{training["duration"]} мин'
            )
        )


def filter_trainings():
    type_filter = type_filter_entry.get().strip().lower()
    date_filter = date_filter_entry.get().strip()

    filtered = trainings

    # Фильтр по типу
    if type_filter:
        filtered = [
            t for t in filtered
            if type_filter in t["type"].lower()
        ]

    # Фильтр по дате
    if date_filter:
        try:
            datetime.strptime(date_filter, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Дата фильтра должна быть в формате YYYY-MM-DD!"
            )
            return

        filtered = [
            t for t in filtered
            if t["date"] == date_filter
        ]

    update_table(filtered)


def clear_filters():
    type_filter_entry.delete(0, tk.END)
    date_filter_entry.delete(0, tk.END)

    update_table(trainings)


def clear_fields():
    date_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)


def save_trainings():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(trainings, file, ensure_ascii=False, indent=4)


def load_trainings():
    global trainings

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            trainings = json.load(file)

        update_table(trainings)

# ---------------------- GUI ---------------------- #

root = tk.Tk()
root.title("Training Planner")
root.geometry("800x600")
root.resizable(False, False)

# ---------------------- Заголовок ---------------------- #

title_label = tk.Label(
    root,
    text="План тренировок",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=10)

# ---------------------- Форма ---------------------- #

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Дата
tk.Label(form_frame, text="Дата (YYYY-MM-DD)").grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

date_entry = tk.Entry(form_frame, width=25)
date_entry.grid(row=0, column=1)

# Тип тренировки
tk.Label(form_frame, text="Тип тренировки").grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

type_entry = tk.Entry(form_frame, width=25)
type_entry.grid(row=1, column=1)

# Длительность
tk.Label(form_frame, text="Длительность (мин)").grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

duration_entry = tk.Entry(form_frame, width=25)
duration_entry.grid(row=2, column=1)

# Кнопка добавления
add_button = tk.Button(
    root,
    text="Добавить тренировку",
    font=("Arial", 12),
    command=add_training
)
add_button.pack(pady=10)

# ---------------------- Фильтрация ---------------------- #

filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Тип").grid(row=0, column=0)

type_filter_entry = tk.Entry(filter_frame)
type_filter_entry.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Дата").grid(row=0, column=2)

date_filter_entry = tk.Entry(filter_frame)
date_filter_entry.grid(row=0, column=3, padx=5)

filter_button = tk.Button(
    filter_frame,
    text="Фильтр",
    command=filter_trainings
)
filter_button.grid(row=0, column=4, padx=5)

clear_button = tk.Button(
    filter_frame,
    text="Сбросить",
    command=clear_filters
)
clear_button.grid(row=0, column=5)

# ---------------------- Таблица ---------------------- #

columns = ("Дата", "Тип тренировки", "Длительность")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=220)

table.pack(pady=10)

# ---------------------- Загрузка данных ---------------------- #

load_trainings()

# ---------------------- Запуск ---------------------- #

root.mainloop()
