from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

for version in ('v72','v74','v75','v76','v78'):
    s = re.sub(rf'\n<style id="{version}-dashboard[^\"]*">.*?</style>\s*<script id="{version}-dashboard[^\"]*">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v78-dashboard-today-isolation">
/* V78 — Programme ne montre jamais le Tableau de bord ni le cockpit Aujourd'hui. */
#v61Dashboard.v78-dashboard-visible { display:block !important; }
#v64Dashboard.v78-today-visible { display:block !important; }
#v61Dashboard.v78-dashboard-hidden,
#v64Dashboard.v78-today-hidden { display:none !important; }
</style>
<script id="v78-dashboard-today-isolation">
(function(){
  function hide(el){
    el?.classList.add('hidden','v78-dashboard-hidden');
    el?.classList.remove('v78-dashboard-visible');
  }
  function show(el){
    el?.classList.remove('hidden','v78-dashboard-hidden');
    el?.classList.add('v78-dashboard-visible');
  }
  function sync(){
    const program=document.getElementById('programSection');
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');
    if(!today || !dashboard) return;

    // Programme visible = priorité absolue. Même si l'ancien bouton Tableau de bord
    // est encore marqué actif, son contenu doit rester caché.
    if(program && !program.classList.contains('hidden')){
      hide(today);
      hide(dashboard);
      return;
    }
    if(todayBtn?.classList.contains('nav-active')){
      hide(dashboard);
      show(today);
      return;
    }
    if(dashboardBtn?.classList.contains('nav-active')){
      hide(today);
      show(dashboard);
      return;
    }
    // Journal intime, Évolution des scores, Ressources, etc.
    hide(today);
    hide(dashboard);
  }
  function install(){
    sync();
    ['programSection','journalSection','evolutionSection','v61Dashboard','v64Dashboard'].forEach(id=>{
      const el=document.getElementById(id);
      if(el && !el.dataset.v78Observed){
        el.dataset.v78Observed='1';
        new MutationObserver(sync).observe(el,{attributes:true,attributeFilter:['class']});
      }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,700));
  new MutationObserver(()=>setTimeout(install,0)).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V78 Programme cleanup applied')
