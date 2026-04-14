"""Script para corrigir incompatibilidades com Flet 0.84."""
import re
import glob
import logging

logger = logging.getLogger("FixFlet84")

files = glob.glob('views/*.py') + ['main.py']
total = 0

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. ft.alignment.center -> ft.Alignment.CENTER
    content = content.replace('ft.alignment.center', 'ft.Alignment.CENTER')
    # 2. ft.alignment.top_center -> ft.Alignment.TOP_CENTER
    content = content.replace(
        'ft.alignment.top_center', 'ft.Alignment.TOP_CENTER')

    # 3. ft.ElevatedButton(text="X", ... ) -> ft.Button(content=ft.Text("X"), ...)
    content = re.sub(
        r'ft\.ElevatedButton\(text=(".*?")',
        r'ft.Button(content=ft.Text(\1)',
        content,
    )

    # 4. ft.TextButton(text="X", ...) -> ft.TextButton(content=ft.Text("X"), ...)
    content = re.sub(
        r'ft\.TextButton\(text=(".*?")',
        r'ft.TextButton(content=ft.Text(\1))',
        content,
    )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        total += 1
        logger.info('Fixed: %s', fpath)
    else:
        logger.debug('OK: %s', fpath)

logger.info('Total files modified: %d', total)
