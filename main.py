import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os

# 📁 نام فایل ذخیره‌سازی
TASKS_FILE = "tasks.json"

# 📝 لیست سراسری برای ذخیره‌ی تسک‌ها
tasks = []


def load_tasks():
    """بارگذاری تسک‌ها از فایل JSON (در صورت وجود)"""
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                tasks = []


def save_tasks():
    """ذخیره‌ی تسک‌ها در فایل JSON"""
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def add_task():
    """افزودن تسک جدید با Date Picker"""
    add_window = tk.Toplevel(root)
    add_window.title("Add Task")
    add_window.geometry("300x250")

    tk.Label(add_window, text="Title:").pack(pady=5)
    title_entry = tk.Entry(add_window, width=30)
    title_entry.pack()

    tk.Label(add_window, text="Due Date:").pack(pady=5)
    date_entry = DateEntry(add_window, width=27, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
    date_entry.pack()

    tk.Label(add_window, text="Done? (yes/no):").pack(pady=5)
    status_entry = ttk.Combobox(add_window, values=["yes", "no"], state="readonly", width=27)
    status_entry.set("no")
    status_entry.pack()

    def save_new_task():
        title = title_entry.get().strip()
        due_date = date_entry.get_date().strftime("%Y-%m-%d")
        status = status_entry.get().strip().lower()

        if title:
            is_done = True if status == "yes" else False
            tasks.append({"title": title, "done": is_done, "due_date": due_date})
            save_tasks()  # 📥 ذخیره در فایل
            messagebox.showinfo("Success", "Task added successfully!")
            add_window.destroy()
        else:
            messagebox.showwarning("Error", "Please fill all fields!")

    tk.Button(add_window, text="Save", command=save_new_task, bg="green", fg="white").pack(pady=10)


def edit_task():
    """ویرایش تسک با Date Picker"""
    if not tasks:
        messagebox.showwarning("Error", "No tasks to edit!")
        return

    try:
        task_number = simpledialog.askinteger("Edit Task", "Enter task number to edit:", minvalue=1, maxvalue=len(tasks))
        if task_number is None:
            return

        task_index = task_number - 1
        task = tasks[task_index]

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Task")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="New Title:").pack(pady=5)
        title_entry = tk.Entry(edit_window, width=30)
        title_entry.insert(0, task["title"])
        title_entry.pack()

        tk.Label(edit_window, text="New Due Date:").pack(pady=5)
        date_entry = DateEntry(edit_window, width=27, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        date_entry.set_date(task["due_date"])
        date_entry.pack()

        tk.Label(edit_window, text="Done? (yes/no):").pack(pady=5)
        status_entry = ttk.Combobox(edit_window, values=["yes", "no"], state="readonly", width=27)
        status_entry.set("yes" if task["done"] else "no")
        status_entry.pack()

        def save_changes():
            new_title = title_entry.get().strip()
            new_due_date = date_entry.get_date().strftime("%Y-%m-%d")
            new_status = status_entry.get().strip().lower()

            if new_title:
                task["title"] = new_title
                task["due_date"] = new_due_date
                task["done"] = True if new_status == "yes" else False
                save_tasks()  # 📥 ذخیره تغییرات
                messagebox.showinfo("Success", "Task updated successfully!")
                edit_window.destroy()
            else:
                messagebox.showwarning("Error", "Please fill all fields!")

        tk.Button(edit_window, text="Save", command=save_changes, bg="blue", fg="white").pack(pady=10)

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter a number.")


def show_tasks():
    """نمایش لیست تسک‌ها"""
    task_window = tk.Toplevel(root)
    task_window.title("Task List")
    task_window.geometry("400x300")

    if not tasks:
        tk.Label(task_window, text="⚠️ No tasks available!", fg="red").pack(pady=10)
    else:
        for idx, task in enumerate(tasks, start=1):
            status_icon = "✅" if task["done"] else "⏳"
            tk.Label(task_window, text=f"{idx}. {status_icon} {task['title']} (Due: {task['due_date']})").pack()


def delete_task():
    """حذف تسک"""
    if not tasks:
        messagebox.showwarning("Error", "No tasks to delete!")
        return

    try:
        task_number = simpledialog.askinteger("Delete Task", "Enter task number to delete:", minvalue=1, maxvalue=len(tasks))
        if task_number is None:
            return

        task_index = task_number - 1
        deleted_task = tasks.pop(task_index)
        save_tasks()  # 📥 ذخیره تغییرات
        messagebox.showinfo("Success", f"Deleted task: {deleted_task['title']}")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter a number.")


def exit_app():
    """خروج از برنامه"""
    root.quit()


# 🖼️ تنظیمات اصلی پنجره
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x400")

# 📥 **بارگذاری تسک‌های ذخیره‌شده هنگام اجرا**
load_tasks()

# 📌 منوی اصلی
menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

# 🔘 دکمه‌های منو
tk.Button(menu_frame, text="➕ Add Task", command=add_task, width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(menu_frame, text="📋 Show Tasks", command=show_tasks, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(menu_frame, text="✏️ Edit Task", command=edit_task, width=20).grid(row=2, column=0, padx=5, pady=5)
tk.Button(menu_frame, text="🗑 Delete Task", command=delete_task, width=20).grid(row=3, column=0, padx=5, pady=5)
tk.Button(menu_frame, text="🚪 Exit", command=exit_app, width=20, bg="red", fg="white").grid(row=4, column=0, padx=5, pady=5)

# 🚀 اجرای GUI
root.mainloop()
