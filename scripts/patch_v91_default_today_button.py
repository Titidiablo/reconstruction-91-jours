from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

patch = r'''
<style id="v91-default-today-button">
/* V91 — à l'arrivée sur l'application, Aujourd'hui est le bouton sélectionné par défaut. */
</style>
<script id="v91-default-today-button">
(function(){
  function setOnly(btn){
    if(!btn) return;
    document.querySelectorAll('.nav-buttons button.nav-active').forEach(b=>b.classList.remove('nav-active'));
    btn.classList.add('nav-active');
  }
  function initDefault(){
    const today=document.getElementById('todayNavButton');
    const program=document.getElementById('programSection');
    const dashboard=document.getElementById('v61Dashboard');
    if(!today) return;
    /* Ne force Aujourd'hui que lors de l'arrivée initiale, quand aucune autre section n'est active. */
    const active=document.querySelector('.nav-buttons button.nav-active');
    const programVisible=program && !program.classList.contains('hidden');
    const dashboardVisible=dashboard && !dashboard.classList.contains('hidden');
    if(!active && !programVisible && !dashboardVisible) setOnly(today);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>setTimeout(initDefault,50));
  else setTimeout(initDefault,50);
  window.addEventListener('load',()=>setTimeout(initDefault,300));
  setTimeout(initDefault,1000);
})();
</script>
'''

s = re.sub(r'\n<style id="v91-default-today-button">.*?</style>\s*<script id="v91-default-today-button">.*?</script>\s*', '\n', s, flags=re.S)
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V91 default Today button applied')
