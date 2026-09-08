from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v72-dashboard-no-today-duplicates"' not in s:
    patch = r'''
<style id="v72-dashboard-no-today-duplicates">
/* V72 — Tableau de bord ne répète aucun élément du cockpit Aujourd'hui. */
#v61Dashboard .v72-today-duplicate { display:none !important; }
</style>
<script id="v72-dashboard-no-today-duplicates">
(function(){
  function clean(){
    const dashboard=document.getElementById('v61Dashboard');
    if(!dashboard) return;
    const firstCard=dashboard.querySelector('.card');
    if(firstCard && firstCard.querySelector('#v61Progress, #v61Score, #v61Streak, #v61Last')){
      firstCard.classList.add('v72-today-duplicate');
      firstCard.remove();
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
print('V72 dashboard duplicate Today content removed')
