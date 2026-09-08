from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the V72 patch that deleted the whole first dashboard card.
s = re.sub(r'\s*<style id="v72-dashboard-no-today-duplicates">.*?</style>\s*<script id="v72-dashboard-no-today-duplicates">.*?</script>\s*', '\n', s, flags=re.S)

if 'id="v73-dashboard-restore-header"' not in s:
    patch = r'''
<style id="v73-dashboard-restore-header">
/* V73 — conserver l'identité du Tableau de bord sans recopier les indicateurs d'Aujourd'hui. */
#v61Dashboard .v73-dashboard-intro { margin-bottom:0; }
#v61Dashboard .v73-dashboard-intro p { margin:6px 0 0; color:#555; }
</style>
<script id="v73-dashboard-restore-header">
(function(){
  function clean(){
    const dashboard=document.getElementById('v61Dashboard');
    if(!dashboard) return;
    const firstCard=dashboard.querySelector('.card');
    if(!firstCard) return;

    // Rebuild only the dashboard identity/intro. The metrics belong exclusively to Aujourd'hui.
    if(firstCard.querySelector('#v61Progress, #v61Score, #v61Streak, #v61Last')){
      firstCard.innerHTML='<h2 class="section-title">🏠 Mon tableau de bord</h2><div class="v73-dashboard-intro"><p>Une vue d’analyse de ton parcours : tendances, points forts, points de vigilance et dernières journées.</p></div>';
      firstCard.classList.add('v73-dashboard-intro');
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',clean);
  else clean();
  window.addEventListener('load',()=>setTimeout(clean,1000));
  new MutationObserver(()=>setTimeout(clean,0)).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V73 dashboard header restored without Today metrics')
