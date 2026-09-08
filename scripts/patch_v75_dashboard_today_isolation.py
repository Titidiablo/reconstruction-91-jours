from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove previous isolation patches so the generated page contains one clean V76 patch.
for version in ('v72','v74','v75','v76'):
    s = re.sub(
        rf'\n<style id="{version}-dashboard[^\"]*">.*?</style>\s*<script id="{version}-dashboard[^\"]*">.*?</script>\s*',
        '\n', s, flags=re.S
    )

patch = r'''
<style id="v76-dashboard-today-isolation">
/* V76 — séparation stricte : le bloc Tableau de bord n'apparaît pas dans Programme. */
#v61Dashboard.v76-dashboard-visible { display:block !important; }
#v64Dashboard.v76-today-visible { display:block !important; }
#v61Dashboard.v76-dashboard-hidden,
#v64Dashboard.v76-today-hidden { display:none !important; }
</style>
<script id="v76-dashboard-today-isolation">
(function(){
  function setActive(id){
    document.querySelectorAll('.nav-buttons button').forEach(b=>b.classList.remove('nav-active'));
    document.getElementById(id)?.classList.add('nav-active');
  }

  function hideCockpit(){
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    today?.classList.add('hidden','v76-today-hidden');
    today?.classList.remove('v76-today-visible');
    dashboard?.classList.add('hidden','v76-dashboard-hidden');
    dashboard?.classList.remove('v76-dashboard-visible');
  }

  function removeDashboardBlockFromProgram(){
    const program=document.getElementById('programSection');
    if(!program) return;
    const markers=[
      '🏠 Mon tableau de bord',
      '🧠 Analyse de mon évolution',
      '📈 Progression depuis J1',
      '💪 Dimension qui progresse le plus',
      '🎯 Dimension à surveiller',
      '🔎 Lecture récente',
      '🗓️ Mes dernières journées'
    ];
    const normalize=s=>String(s||'').replace(/\\s+/g,' ').trim();
    const candidates=Array.from(program.querySelectorAll('.card, section, article, div'))
      .filter(el=>el!==program)
      .filter(el=>markers.every(m=>normalize(el.textContent).includes(m)))
      .sort((a,b)=>normalize(a.textContent).length-normalize(b.textContent).length);
    const block=candidates[0];
    if(block){
      block.remove();
    }
  }

  function showTodayScreen(){
    const program=document.getElementById('programSection');
    const journal=document.getElementById('journalSection');
    const evolution=document.getElementById('evolutionSection');
    const dashboard=document.getElementById('v61Dashboard');
    const today=document.getElementById('v64Dashboard');
    if(!today) return;
    [program,journal,evolution,dashboard].forEach(el=>el?.classList.add('hidden'));
    dashboard?.classList.remove('v76-dashboard-visible');
    dashboard?.classList.add('v76-dashboard-hidden');
    today.classList.remove('hidden','v76-today-hidden');
    today.classList.add('v76-today-visible');
    setActive('todayNavButton');
  }

  function showDashboardScreen(){
    const dashboard=document.getElementById('v61Dashboard');
    const today=document.getElementById('v64Dashboard');
    if(!dashboard) return;
    ['programSection','journalSection','evolutionSection'].forEach(id=>document.getElementById(id)?.classList.add('hidden'));
    today?.classList.add('hidden','v76-today-hidden');
    today?.classList.remove('v76-today-visible');
    dashboard.classList.remove('hidden','v76-dashboard-hidden');
    dashboard.classList.add('v76-dashboard-visible');
    setActive('dashboardNavButton');
  }

  function syncScreens(){
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');
    const today=document.getElementById('v64Dashboard');
    const dashboard=document.getElementById('v61Dashboard');
    if(!today || !dashboard) return;
    removeDashboardBlockFromProgram();
    if(todayBtn?.classList.contains('nav-active')){
      showTodayScreen();
      return;
    }
    if(dashboardBtn?.classList.contains('nav-active')){
      showDashboardScreen();
      return;
    }
    // Programme, Journal intime, Évolution des scores, Ressources, etc.
    // aucun de ces écrans ne doit afficher le cockpit ni le tableau de bord.
    hideCockpit();
  }

  function install(){
    const todayBtn=document.getElementById('todayNavButton');
    const dashboardBtn=document.getElementById('dashboardNavButton');
    if(todayBtn && !todayBtn.dataset.v76Bound){
      todayBtn.dataset.v76Bound='1';
      todayBtn.addEventListener('click',()=>setTimeout(syncScreens,0));
    }
    if(dashboardBtn && !dashboardBtn.dataset.v76Bound){
      dashboardBtn.dataset.v76Bound='1';
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
print('V76 Dashboard block removed from Programme; Today/Dashboard isolation preserved')
