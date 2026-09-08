from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the two previous patches that could delete the real dashboard card.
s = re.sub(r'\n<style id="v72-dashboard-no-today-duplicates">.*?</style>\s*<script id="v72-dashboard-no-today-duplicates">.*?</script>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<style id="v74-remove-today-cockpit-from-dashboard">.*?</style>\s*<script id="v74-remove-today-cockpit-from-dashboard">.*?</script>\s*', '\n', s, flags=re.S)

if 'id="v75-dashboard-today-isolation"' not in s:
    patch = r'''
<style id="v75-dashboard-today-isolation">
/* V75 — Aujourd'hui et Tableau de bord sont deux écrans indépendants. */
#v61Dashboard.v75-dashboard-visible + #v64Dashboard,
#v64Dashboard.v75-dashboard-hidden { display:none !important; }
</style>
<script id="v75-dashboard-today-isolation">
(function(){
  function sync(){
    const dashboard=document.getElementById('v61Dashboard');
    const today=document.getElementById('v64Dashboard');
    if(!dashboard || !today) return;

    const dashboardBtn=document.getElementById('dashboardNavButton');
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardActive=!!dashboardBtn?.classList.contains('nav-active');
    const todayActive=!!todayBtn?.classList.contains('nav-active');

    if(dashboardActive){
      dashboard.classList.add('v75-dashboard-visible');
      dashboard.classList.remove('hidden');
      today.classList.add('hidden','v75-dashboard-hidden');
      return;
    }
    if(todayActive){
      dashboard.classList.add('hidden');
      dashboard.classList.remove('v75-dashboard-visible');
      today.classList.remove('hidden','v75-dashboard-hidden');
      return;
    }
  }

  function install(){
    const oldShowSection=window.showSection;
    if(typeof oldShowSection==='function' && !oldShowSection.__v75Wrapped){
      const wrapped=function(){
        const result=oldShowSection.apply(this,arguments);
        setTimeout(sync,0);
        return result;
      };
      wrapped.__v75Wrapped=true;
      window.showSection=wrapped;
    }

    const oldShowToday=window.showToday;
    if(typeof oldShowToday==='function' && !oldShowToday.__v75Wrapped){
      const wrapped=function(){
        const result=oldShowToday.apply(this,arguments);
        setTimeout(sync,0);
        return result;
      };
      wrapped.__v75Wrapped=true;
      window.showToday=wrapped;
    }
    sync();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,1000));
})();
</script>
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V75 Dashboard/Today isolation applied')
