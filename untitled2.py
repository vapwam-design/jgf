import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Файл для хранения избранных
FAVORITES_FILE = 'users.json'

# Загружаем избранных при старте
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

# Сохраняем избранных
def save_favorites(favorites):
    try:
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(favorites, f, indent=4)
    except IOError:
        messagebox.showerror("Ошибка", "Не удалось сохранить избранных.")

# Поиск пользователя
def search_user():
    username = entry.get().strip()
    if not username:
        messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым.")
        return
    url = f'https://api.github.com/users/{username}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            display_user(user_data)
        elif response.status_code == 404:
            messagebox.showinfo("Результат", "Пользователь не найден.")
        else:
            messagebox.showerror("Ошибка", f"Ошибка при запросе: {response.status_code}")
    except requests.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Произошла ошибка: {e}")

# Отображение информации пользователя
def display_user(user):
    info_text = f"Имя: {user.get('name', 'N/A')}\n" \
                f"Логин: {user.get('login')}\n" \
                f"URL: {user.get('html_url')}"
    label_result.config(text=info_text)
    btn_add_favorite.config(state='normal')
    btn_add_favorite.user_data = user

# Добавление в избранное
def add_to_favorites():
    user = btn_add_favorite.user_data
    if user['login'] not in [u['login'] for u in favorites]:
        favorites.append(user)
        save_favorites(favorites)
        update_favorites_list()
        messagebox.showinfo("Готово", "Пользователь добавлен в избранное")
    else:
        messagebox.showinfo("Информация", "Этот пользователь уже в избранных.")

# Обновление списка избранных
def update_favorites_list():
    favorites_list.delete(0, tk.END)
    for u in favorites:
        favorites_list.insert(tk.END, u['login'])

# Графический интерфейс
root = tk.Tk()
root.title("GitHub User Finder")

# Поле поиска
tk.Label(root, text="Введите имя пользователя GitHub").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Кнопка поиска
btn_search = tk.Button(root, text="Найти", command=search_user)
btn_search.pack(pady=5)

# Результат поиска
label_result = tk.Label(root, text="", justify='left')
label_result.pack(pady=5)

# Кнопка добавления в избранное
btn_add_favorite = tk.Button(root, text="Добавить в избранное", command=add_to_favorites, state='disabled')
btn_add_favorite.pack(pady=5)

# Список избранных
tk.Label(root, text="Избранные:").pack(pady=5)
favorites_list = tk.Listbox(root, width=50)
favorites_list.pack(pady=5)

# Загрузить избранных
favorites = load_favorites()
update_favorites_list()

root.mainloop()