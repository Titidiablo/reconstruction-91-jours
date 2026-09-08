from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the mistaken V69 runtime patch from the generated page.
s = re.sub(r'\s*<style id="v69-dashboard-cleanup">.*?</style>\s*<script id="v69-dashboard-cleanup">.*?</script>\s*', '\n', s, flags=re.S)

if 'id="v70-restore-structure"' not in s:
    patch = r'''
<style id="v70-restore-structure">
/* V70 — Aujourd'hui = cockpit ; Tableau de bord = suivi + grille ; Programme = programme. */
#v64Dashboard .v64-days-card { display:none !important; }
#v61Dashboard .v70-days-card { display:block !important; margin-top:20px; }
#v61Dashboard .v70-days-grid { display:grid; grid-template-columns:repeat(13,minmax(34px,1fr)); gap:6px; margin-top:14px; }
.v70-days-card h3 { margin:0; }
@media(max-width:800px){#v61Dashboard .v70-days-grid{grid-template-columns:repeat(7,minmax(34px,1fr));}}
</style>
<script id="v70-restore-structure">
(function(){
  function buildDashboardGrid(){
    const dashboard=document.getElementById('v61Dashboard');
    const source=document.querySelector('#v64Dashboard .v64-days-card');
    if(!dashboard || !source) return;
    let card=dashboard.querySelector('.v70-days-card');
    if(!card){
      card=document.createElement('div');
      card.className='card v70-days-card';
      card.innerHTML='<div class="v64-days-head"><h3>🗓️ Les 91 jours</h3></div><div id="v70DaysGrid" class="v70-days-grid"></div>';
      dashboard.appendChild(card);
    }
    const target=document.getElementById('v70DaysGrid');
    if(!target) return;
    target.innerHTML='';
    source.querySelectorAll('.v64-day-btn').forEach(original=>{
      const btn=original.cloneNode(true);
      btn.onclick=function(e){
        e.preventDefault();
        e.stopPropagation();
        const match=String(btn.textContent||'').match(/J(\d+)/i);
        const day=match ? Number(match[1]) : NaN;
        if(!Number.isInteger(day) || day<1 || day>91) return;
        const go=typeof requestDayChange==='function' ? requestDayChange(day) : Promise.resolve();
        Promise.resolve(go).then(()=>{ if(typeof showSection==='function') showSection('program'); });
      };
      target.appendChild(btn);
    });
    source.remove();
  }

  function cleanProgram(){
    document.querySelectorAll('#programSection .v64-stepper').forEach(el=>el.remove());
    document.querySelectorAll('#programSection .v64-days-card, #programSection .v70-days-card').forEach(el=>el.remove());
  }

  function install(){
    buildDashboardGrid();
    cleanProgram();
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
print('V70 structure restored')
