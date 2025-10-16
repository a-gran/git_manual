# -*- coding: utf-8 -*-
import re

# Читаем файл
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Удаляем эмодзи из заголовков
# Шаблон: ## ЧИСЛО. ЭМОДЗИ git КОМАНДА -> ## ЧИСЛО. git КОМАНДА
pattern = r'(## \d+\.)\s+[^\s\w]+\s+(git [^\n]+)'
replacement = r'\1 \2'

content = re.sub(pattern, replacement, content)

# Записываем обратно
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Headers fixed!")
