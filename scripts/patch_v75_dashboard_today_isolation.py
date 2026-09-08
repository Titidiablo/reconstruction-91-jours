from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

for version in ('v72','v74','v75','v76','v78','v79','v80'):
    s = re.sub(rf'\n<style id="{version}-dashboard[^\"]*">.*?</style>\s*<script id="{version}-dashboard[^\"]*">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v80-dashboard-navigation-fix">
/* V80 — séparation stricte sans observer de classes : évite toute boucle qui bloque les clics. */
#v61Dashboard.v80-dashboard-visible { display:block !important; }
#v64Dashboard.v80-today-visible { display:block !important; }
#v61Dashboard.v80-dashboard-hidden,
#v64Dashboard.v80-today-hidden { display:none !important; }
</style>
<script id="v80-dashboard-navigation-fix">
(function(){
  function hide(el){
    if(!el) return;
    el.classList.add('hidden','v80-dashboard-hidden');
    el.classList.remove('v80-dashboard-visible','v80-today-visible');
  }
  function show(el, today){
    if(!el) return;
    el.classList.remove('hidden','v80-dashboard-hidden','v80-today-hidden');
    el.classList.add(today ? 'v80-today-visible' : 'v80-dashboard-visible');
  }
  function sync(){
    const program=document.getElementById('programSection');
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');
    if(!today || !dashboard) return;

    if(program && !program.classList.contains('hidden')){
      hide(today);
      hide(dashboard);
      return;
    }
    if(todayBtn?.classList.contains('nav-active')){
      hide(dashboard);
      show(today, true);
      return;
    }
    if(dashboardBtn?.classList.contains('nav-active')){
      hide(today);
      show(dashboard, false);
      return;
    }
    hide(today);
    hide(dashboard);
  }
  function install(){
    sync();
    document.querySelectorAll('.nav-buttons button').forEach(btn=>{
      if(btn.dataset.v80Bound) return;
      btn.dataset.v80Bound='1';
      btn.addEventListener('click',()=>setTimeout(sync,0));
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
print('V80 navigation fix applied')
