#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для исправления ссылок в содержании README.md
"""

import re
import sys

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_anchor(text):
    """
    Создает якорь из текста заголовка по правилам GitHub
    - Убирает эмодзи
    - Преобразует в нижний регистр
    - Заменяет пробелы на дефисы
    - Убирает специальные символы
    """
    # Убираем эмодзи и невидимые символы
    # Оставляем только буквы, цифры, пробелы, точки и дефисы
    text = re.sub(r'[^\w\s\.\-а-яё]', '', text, flags=re.UNICODE)

    # Приводим к нижнему регистру
    text = text.lower()

    # Убираем лишние пробелы
    text = text.strip()

    # Заменяем пробелы на дефисы
    text = re.sub(r'\s+', '-', text)

    # Заменяем точки на пустую строку или дефис
    text = text.replace('.', '')

    # Убираем множественные дефисы
    text = re.sub(r'-+', '-', text)

    # Убираем дефисы в начале и конце
    text = text.strip('-')

    return text

# Читаем файл
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим все заголовки команд (## ЧИСЛО. ...)
headers = re.findall(r'^## (\d+)\.\s+(.+)$', content, re.MULTILINE)

print("Найденные заголовки и их якоря:\n")
print("-" * 60)

# Создаем список правильных ссылок
links_list = []
for num, header_text in headers:
    # Создаем якорь из полного заголовка (с номером)
    full_text = f"{num}. {header_text}"
    anchor = create_anchor(full_text)

    # Извлекаем название команды (убираем эмодзи в начале)
    cmd_name = re.sub(r'^[^\w\s]+\s*', '', header_text, flags=re.UNICODE).strip()
    # Берем всё до первого пробела или всё, если пробелов нет
    # Для команд типа "git cherry-pick" берем полное название
    if cmd_name.startswith('git'):
        # Берем "git КОМАНДА" (первые два слова)
        parts = cmd_name.split(None, 2)  # Разделяем на максимум 3 части
        cmd_name = ' '.join(parts[:2]) if len(parts) >= 2 else cmd_name

    print(f"{num}. Заголовок: {header_text}")
    print(f"   Команда: {cmd_name}")
    print(f"   Якорь: #{anchor}")
    print()

    links_list.append(f"{num}. [{cmd_name}](#{anchor})")

print("-" * 60)
print("\nНовое содержание:\n")
print('\n'.join(links_list))

# Находим секцию содержания и заменяем её
toc_pattern = r'(## 📋 Содержание\n\n)(.*?)(\n---)'

new_toc = f"## 📋 Содержание\n\n" + '\n'.join(links_list) + "\n\n---"

# Заменяем старое содержание на новое
new_content = re.sub(toc_pattern, lambda m: new_toc, content, flags=re.DOTALL)

# Сохраняем
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n" + "=" * 60)
print("✅ Файл README.md успешно обновлен!")
print("=" * 60)
