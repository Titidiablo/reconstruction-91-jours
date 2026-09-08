from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V65 : la grille « Mon parcours » est la seule grille de navigation des jours.
# Supprime le bouton global « 91 jours » ajouté par V64.
s, n1 = re.subn(
    r'\n\s*if\(!\$\(\'daysNavButton\'\)\)\{.*?\}\n',
    '\n',
    s,
    count=1,
    flags=re.S,
)

# Supprime les deux boutons redondants dans le tableau de bord V64.
s = s.replace(
    '<button class="secondary" type="button" id="v64OpenDays">🗓️ Voir les 91 jours</button>',
    ''
)
s = s.replace(
    '<button class="secondary" type="button" id="v64CompactDays">Ouvrir la grille</button>',
    ''
)
s = s.replace(
    ";$('v64OpenDays').onclick=openDays;$('v64CompactDays').onclick=openDays;",
    ";",
)

# Depuis « Mon parcours », un clic sur J1…J91 ouvre directement le bon jour.
s = s.replace(
    "b.onclick=()=>{closeDays();showSection('program');requestDayChange(d)};",
    "b.onclick=async()=>{closeDays();await requestDayChange(d);showSection('program')};",
)

# Marqueur de version pour éviter une réapplication inutile.
if 'id="v65-navigation-fix"' not in s:
    marker = '''\n<style id="v65-navigation-fix">\n/* V65 — Mon parcours est la navigation principale des 91 jours. */\n.v64-days-card .v64-days-head { justify-content: flex-start; }\n.v64-days-card .v64-days-head h3 { flex: 1; }\n.v64-day-btn { cursor: pointer; }\n.v64-day-btn:active { transform: translateY(1px); }\n</style>\n'''
    s = s.replace('</head>', marker + '</head>', 1)

p.write_text(s, encoding='utf-8')
print(f'V65 navigation applied (nav removed: {n1})')
