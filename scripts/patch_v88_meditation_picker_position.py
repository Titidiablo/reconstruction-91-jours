from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V88 — place le sélecteur audio juste sous le texte explicatif du bloc Méditation.
old = "if(host === $('programSection')) host.prepend(picker); else host.parentNode.insertBefore(picker,host);"
new = r'''const sections=Array.from(host.querySelectorAll('.exercise-section'));
    const meditationSection=sections.find(section=>{
      const text=(section.innerText||section.textContent||'').toLowerCase();
      return text.includes('méditation') || text.includes('meditation');
    });
    if(meditationSection){
      const explanatoryText=meditationSection.querySelector('.exercise-text');
      if(explanatoryText){
        explanatoryText.insertAdjacentElement('afterend',picker);
      } else {
        meditationSection.appendChild(picker);
      }
    } else if(host === $('programSection')) {
      host.prepend(picker);
    } else {
      host.parentNode.insertBefore(picker,host);
    }'''

if old not in s:
    raise SystemExit('V88: insertion point not found')
s = s.replace(old, new, 1)

# Replace any previous V88 patch cleanly if the workflow is re-run.
s = re.sub(r'\n<style id="v88-meditation-picker-position">.*?</style>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v88-meditation-picker-position">
/* Le sélecteur audio reste visuellement dans le bloc Méditation, sous son texte explicatif. */
.meditation-media-picker { margin-top:12px; margin-bottom:16px; }
</style>
'''
s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V88 meditation picker position applied')
