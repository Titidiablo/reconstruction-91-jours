from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

# V64 : applique directement les corrections visibles à partir de l'index V63.
if 'id="v63-resources-runtime"' not in s:
    raise SystemExit('V63 resources runtime not found in index.html')

# Version visible.
s = s.replace('<div class="app-version-v18">V63</div>', '<div class="app-version-v18">V64</div>', 1)

# Libellés des 4 scores.
s = s.replace('🧘 Présence', '🧘 Pleine conscience')
s = s.replace("🛑 Maîtrise de l'impulsion", '🔥 Maîtrise des impulsions')
s = s.replace('Maîtrise de l’impulsion', 'Maîtrise des impulsions')
s = s.replace('Maîtrise de l\'impulsion', 'Maîtrise des impulsions')

# Libellés du graphique pour rester cohérents avec les scores du jour.
s = s.replace('["presence", "Présence", "#3b82f6"]', '["presence", "Pleine conscience", "#3b82f6"]')
s = s.replace('["impulse_control", "Maîtrise de l\'impulsion", "#ef4444"]', '["impulse_control", "Maîtrise des impulsions", "#ef4444"]')
s = s.replace('["impulse_control", "Maîtrise de l’impulsion"]', '["impulse_control", "Maîtrise des impulsions"]')

# Guidance : conserve les questions et les repères 1/10 - 10/10 de V63.
# Si le bloc est absent, on l'insère à partir des sélecteurs existants.
if 'id="v63-score-guidance-style"' not in s:
    css = '''<style id="v64-score-guidance-style">\n.score-guidance{font-size:12px;line-height:1.4;color:#666;margin:-2px 0 9px}.score-guidance-question{font-weight:600;color:#333;margin-bottom:3px}.score-guidance-anchors{display:flex;flex-direction:column;gap:2px}.score-guidance-anchors span{display:block}.score-guidance-anchors .low{color:#8a5a00}.score-guidance-anchors .high{color:#26733d}@media(max-width:700px){.score-guidance{font-size:11.5px}}\n</style>'''
    s = s.replace('</head>', css + '\n</head>', 1)

# Le bouton de sauvegarde dans le journal du programme était vide dans l'index actuel.
# On lui donne un libellé explicite ; le bouton flottant reste disponible.
s = s.replace('''<button\n          class="primary"\n          onclick="saveEntry()">\n        </button>''', '''<button\n          class="primary"\n          onclick="saveEntry()">\n          💾 Sauvegarder la journée\n        </button>''', 1)

# Le terme anglais Streak ne doit plus apparaître.
s = s.replace('>Streak<', '>Série<')
s = s.replace('>Streak en cours<', '>Série en cours<')
s = s.replace('Streak en cours', 'Série en cours')

p.write_text(s, encoding="utf-8")
print("V64 visible UI updated")
