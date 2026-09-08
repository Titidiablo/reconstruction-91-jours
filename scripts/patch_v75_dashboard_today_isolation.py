from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove previous V72/V74/V75 isolation patches so the generated page contains one clean V75 patch.
s = re.sub(r'\n<style id="v72-dashboard-no-today-duplicates">.*?</style>\s*<script id="v72-dashboard-no-today-duplicates">.*?</script>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<style id="v74-remove-today-cockpit-from-dashboard">.*?</style>\s*<script id="v74-remove-today-cockpit-from-dashboard">.*?</script>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<style id="v75-dashboard-today-isolation">.*?</style>\s*<script id="v75-dashboard-today-isolation">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v75-dashboard-today-isolation">
/* V75 — chaque écran est indépendant : le cockpit Aujourd'hui ne doit jamais apparaître dans Journal intime. */
#v61Dashboard.v75-dashboard-visible { display:block !important; }
#v64Dashboard.v75-today-visible { display:block !important; }
#v61Dashboard.v75-dashboard-hidden,
#v64Dashboard.v75-today-hidden { display:none !important; }
</style>
<script id="v75-dashboard-today-isolation">
(function(){
  function setActive(id){
    document.querySelectorAll('.nav-buttons button').forEach(b=>b.classList.remove('nav-active'));
    document.getElementById(id)?.classList.add('nav-active');
  }

  function hideCockpit(){
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    today?.classList.add('hidden','v75-today-hidden');
    today?.classList.remove('v75-today-visible');
    dashboard?.classList.add('hidden','v75-dashboard-hidden');
    dashboard?.classList.remove('v75-dashboard-visible');
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
    today.classList.remove('hidden','v75-today-hidden');
    today.classList.add('v75-today-visible');
    setActive('todayNavButton');
  }

  function showDashboardScreen(){
    const dashboard=document.getElementById('v61Dashboard');
    const today=document.getElementById('v64Dashboard');
    if(!dashboard) return;
    ['programSection','journalSection','evolutionSection'].forEach(id=>document.getElementById(id)?.classList.add('hidden'));
    today?.classList.add('hidden','v75-today-hidden');
    today?.classList.remove('v75-today-visible');
    dashboard.classList.remove('hidden','v75-dashboard-hidden');
    dashboard.classList.add('v75-dashboard-visible');
    setActive('dashboardNavButton');
  }

  function syncScreens(){
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');
    const journal=document.getElementById('journalSection');
    const program=document.getElementById('programSection');
    const evolution=document.getElementById('evolutionSection');
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    if(!today || !dashboard) return;

    if(todayBtn?.classList.contains('nav-active')){
      showTodayScreen();
      return;
    }
    if(dashboardBtn?.classList.contains('nav-active')){
      showDashboardScreen();
      return;
    }

    // Programme, Journal intime, Évolution des scores, Ressources, etc. :
    // aucun de ces écrans ne doit afficher le cockpit ni le tableau de bord.
    hideCockpit();
  }

  function install(){
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');

    // Ne remplace pas onclick : les boutons gardent leur logique native.
    if(todayBtn && !todayBtn.dataset.v75Bound){
      todayBtn.dataset.v75Bound='1';
      todayBtn.addEventListener('click',()=>setTimeout(syncScreens,0));
    }
    if(dashboardBtn && !dashboardBtn.dataset.v75Bound){
      dashboardBtn.dataset.v75Bound='1';
      dashboardBtn.addEventListener('click',()=>setTimeout(syncScreens,0));
    }

    syncScreens();
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
print('V75 Dashboard/Today isolation fixed: cockpit hidden from Journal intime and other screens')