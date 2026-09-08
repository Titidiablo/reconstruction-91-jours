from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the two previous patches that could delete the real dashboard card.
s = re.sub(r'\n<style id="v72-dashboard-no-today-duplicates">.*?</style>\s*<script id="v72-dashboard-no-today-duplicates">.*?</script>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<style id="v74-remove-today-cockpit-from-dashboard">.*?</style>\s*<script id="v74-remove-today-cockpit-from-dashboard">.*?</script>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<style id="v75-dashboard-today-isolation">.*?</style>\s*<script id="v75-dashboard-today-isolation">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v75-dashboard-today-isolation">
/* V75 — Aujourd'hui et Tableau de bord sont deux écrans indépendants. */
#v61Dashboard.v75-dashboard-visible { display:block !important; }
#v61Dashboard.v75-dashboard-visible ~ #v64Dashboard { display:none !important; }
#v64Dashboard.v75-today-visible { display:block !important; }
#v61Dashboard.v75-dashboard-hidden { display:none !important; }
</style>
<script id="v75-dashboard-today-isolation">
(function(){
  function setActive(id){
    document.querySelectorAll('.nav-buttons button').forEach(b=>b.classList.remove('nav-active'));
    document.getElementById(id)?.classList.add('nav-active');
  }

  function showTodayScreen(){
    const program=document.getElementById('programSection');
    const journal=document.getElementById('journalSection');
    const evolution=document.getElementById('evolutionSection');
    const dashboard=document.getElementById('v61Dashboard');
    const today=document.getElementById('v64Dashboard');
    if(!today) return;

    [program,journal,evolution,dashboard].forEach(el=>el?.classList.add('hidden'));
    dashboard?.classList.remove('v75-dashboard-visible');
    dashboard?.classList.add('v75-dashboard-hidden');
    today.classList.remove('hidden','v75-dashboard-hidden');
    today.classList.add('v75-today-visible');
    setActive('todayNavButton');
  }

  function showDashboardScreen(){
    const dashboard=document.getElementById('v61Dashboard');
    const today=document.getElementById('v64Dashboard');
    if(!dashboard) return;

    ['programSection','journalSection','evolutionSection'].forEach(id=>document.getElementById(id)?.classList.add('hidden'));
    today?.classList.add('hidden');
    today?.classList.remove('v75-today-visible');
    dashboard.classList.remove('hidden','v75-dashboard-hidden');
    dashboard.classList.add('v75-dashboard-visible');
    setActive('dashboardNavButton');
  }

  function install(){
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');
    if(todayBtn && !todayBtn.dataset.v75Bound){
      todayBtn.dataset.v75Bound='1';
      todayBtn.onclick=showTodayScreen;
    }
    if(dashboardBtn && !dashboardBtn.dataset.v75Bound){
      dashboardBtn.dataset.v75Bound='1';
      dashboardBtn.onclick=showDashboardScreen;
    }

    // Si l'utilisateur arrive sur Aujourd'hui après le chargement,
    // conserver l'écran courant sans laisser le Tableau de bord recouvrir le cockpit.
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    if(today && dashboard && document.getElementById('todayNavButton')?.classList.contains('nav-active')){
      showTodayScreen();
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,1200));
  new MutationObserver(()=>setTimeout(install,0)).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V75 Dashboard/Today isolation fixed')
