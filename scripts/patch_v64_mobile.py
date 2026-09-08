from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

patch = '''\n<style id="v64-mobile-save-fix">\n@media (max-width: 520px) {\n  /* Le bouton de sauvegarde ne doit jamais recouvrir la grille "Mon parcours". */\n  .v64-save-main {\n    position: static !important;\n    bottom: auto !important;\n    z-index: auto !important;\n    margin-bottom: 14px !important;\n  }\n}\n</style>\n'''

if 'id="v64-mobile-save-fix"' not in s:
    s = s.replace('</head>', patch + '</head>', 1)
    p.write_text(s, encoding='utf-8')
    print('Correctif mobile V64 ajouté')
else:
    print('Correctif mobile V64 déjà présent')
