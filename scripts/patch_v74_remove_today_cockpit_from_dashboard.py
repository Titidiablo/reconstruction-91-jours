from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v74-remove-today-cockpit-from-dashboard"' not in s:
    patch = r'''
<style id="v74-remove-today-cockpit-from-dashboard">
/* V74 — Le cockpit « Aujourd’hui » ne doit jamais apparaître dans « Tableau de bord ». */
#v61Dashboard .v74-today-cockpit { display:none !important; }
</style>
<script id="v74-remove-today-cockpit-from-dashboard">
(function(){
  function clean(){
    const dashboard=document.getElementById('v61Dashboard');
    if(!dashboard) return;

    dashboard.querySelectorAll('.v74-today-cockpit').forEach(el=>el.remove());

    dashboard.querySelectorAll('.v64-hero, .v64-dashboard-grid').forEach(el=>{
      const text=String(el.textContent||'');
      if(text.includes('Aujourd’hui') || text.includes("Aujourd'hui") || text.includes('Ton parcours · 91 jours')) el.remove();
    });

    dashboard.querySelectorAll('*').forEach(el=>{
      if(el.children.length>0) return;
      const text=String(el.textContent||'').trim();
      if([
        'Ton parcours · 91 jours',
        'Aujourd’hui · Jour 1',
        'Aujourd’hui',
        'Continue là où tu t’es arrêté.',
        '▶ Continuer ma journée',
        'Jours réalisés',
        'Score du jour',
        'Série',
        'Dernier jour'
      ].includes(text)) {
        const card=el.closest('.card');
        if(card && (card.textContent.includes('Aujourd’hui') || card.textContent.includes('Ton parcours · 91 jours'))) card.remove();
        else el.remove();
      }
    });
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
print('V74 Today cockpit removed from Dashboard')
