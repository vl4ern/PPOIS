#!/usr/bin/env python3
"""
Скрипт для создания пустых __init__.py файлов
Запуск: python create_init_files.py
"""

import os

# Папки, в которых нужно создать __init__.py
folders = [
    'Auto_master/classes',
    'Auto_master/classes/Exceptions',
    'Auto_master/classes/Inventory_classes',
    'Auto_master/classes/Person',
    'Auto_master/classes/Order_classes',
    'Auto_master/classes/Vehicle_classes',
    'Auto_master/classes/Service_classes',
    'Auto_master/classes/Room_classes',
    'tests'
]

for folder in folders:
    init_file = os.path.join(folder, '__init__.py')
    
    # Создаем папку, если она не существует
    os.makedirs(folder, exist_ok=True)
    
    # Создаем пустой __init__.py файл
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# This file makes this directory a Python package\n')
        print(f"✅ Создан: {init_file}")
    else:
        print(f"📁 Уже существует: {init_file}")

print("\n🎉 Все необходимые __init__.py файлы созданы!")