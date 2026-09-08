from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

new_subtitle = 'Ne subissez plus votre vie. Reprenez le contrôle !'

# V82 — remplace le sous-titre de la marque sans toucher au contenu du programme.
patterns = [
    r'(<[^>]*class=["\'][^"\']*\bsubtitle\b[^"\']*["\'][^>]*>)(.*?)(</[^>]+>)',
]

for pattern in patterns:
    s, count = re.subn(pattern, lambda m: m.group(1) + new_subtitle + m.group(3), s, count=1, flags=re.S)
    if count:
        break
else:
    raise SystemExit('V82: élément .subtitle introuvable')

p.write_text(s, encoding='utf-8')
print('V82 subtitle applied:', new_subtitle)
