from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if '>V62</div>' in s:
    s = s.replace('>V62</div>', '>V63</div>', 1)

# V63 resources are already deployed; from now on this script also applies incremental V63 UI fixes.
if 'id="v63-resources-runtime"' not in s:
    raise SystemExit('V63 resources runtime not found in index.html')

# Score labels: clearer wording requested for the four daily dimensions.
replacements = {
    '🧘 Présence': '🧘 Pleine conscience',
    "🛑 Maîtrise de l'impulsion": '🔥 Maîtrise des impulsions',
    '🧭 Cohérence avec mes valeurs': '🧭 Cohérence avec mes valeurs',
    '❤️ Relation à moi-même': '❤️ Relation à moi-même',
}
for old, new in replacements.items():
    s = s.replace(old, new)

# Add an explicit evaluation question and anchors for 1/10 and 10/10.
score_guidance = {
    'presenceScore': (
        'Qu’ai-je réellement observé et vécu avec attention aujourd’hui ?',
        '1/10 : j’étais presque entièrement en pilote automatique.',
        '10/10 : j’ai été pleinement attentif à ce que je vivais, pensais et ressentais.'
    ),
    'impulseScore': (
        'Dans quelle mesure ai-je choisi ma réponse plutôt que de suivre une impulsion ?',
        '1/10 : j’ai presque toujours réagi sous le coup de l’impulsion.',
        '10/10 : j’ai laissé un espace entre l’impulsion et ma réponse, puis choisi consciemment.'
    ),
    'valuesScore': (
        'Dans quelle mesure mes actes d’aujourd’hui étaient-ils alignés avec mes valeurs ?',
        '1/10 : mes actes étaient largement en contradiction avec mes valeurs.',
        '10/10 : mes actes étaient pleinement cohérents avec les valeurs que je veux incarner.'
    ),
    'selfRelationScore': (
        'Comment ai-je traité, parlé et réagi envers moi-même aujourd’hui ?',
        '1/10 : je me suis jugé, dévalorisé ou maltraité intérieurement.',
        '10/10 : je me suis traité avec respect, lucidité, exigence juste et bienveillance.'
    ),
}

# Remove an earlier generated block before inserting the current version.
start_marker = '<style id="v63-score-guidance-style">'
end_marker = '</style>'
start = s.find(start_marker)
if start >= 0:
    end = s.find(end_marker, start)
    if end >= 0:
        s = s[:start] + s[end + len(end_marker):]

css = '''<style id="v63-score-guidance-style">
.score-guidance{font-size:12px;line-height:1.4;color:#666;margin:-2px 0 9px}
.score-guidance-question{font-weight:600;color:#333;margin-bottom:3px}
.score-guidance-anchors{display:flex;flex-direction:column;gap:2px}
.score-guidance-anchors span{display:block}
.score-guidance-anchors .low{color:#8a5a00}
.score-guidance-anchors .high{color:#26733d}
@media(max-width:700px){.score-guidance{font-size:11.5px}}
</style>'''
s = s.replace('</head>', css + '\n</head>', 1)

for field_id, (question, low, high) in score_guidance.items():
    marker = f'<select id="{field_id}">'
    if marker not in s:
        continue
    # Insert only when the guidance block for this field is not already present.
    if f'id="{field_id}-guidance"' not in s:
        block = (
            f'<div id="{field_id}-guidance" class="score-guidance">'
            f'<div class="score-guidance-question">{question}</div>'
            f'<div class="score-guidance-anchors">'
            f'<span class="low">{low}</span>'
            f'<span class="high">{high}</span>'
            f'</div></div>'
        )
        s = s.replace(marker, block + '\n' + marker, 1)

# Replace the English streak label wherever it appears in the V63 dashboard.
s = s.replace('>Streak<', '>Série<')
s = s.replace('>Streak en cours<', '>Série en cours<')
s = s.replace('Streak en cours', 'Série en cours')

p.write_text(s, encoding="utf-8")
print("V63 score UI updated")
