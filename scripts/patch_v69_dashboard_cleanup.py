from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v69-dashboard-cleanup"' not in s:
    patch = r'''
<style id="v69-dashboard-cleanup">
/* V69 — Tableau de bord = grille du parcours uniquement */
#v64Dashboard .v64-hero,
#v64Dashboard .v64-dashboard-grid { display:none !important; }
#v64Dashboard .v64-days-card { display:block !important; margin-top:0; }
</style>
<script id="v69-dashboard-cleanup">
(function(){
  function clean(){
    const dashboard=document.getElementById('v64Dashboard');
    if(!dashboard) return;
    dashboard.querySelector('.v64-hero')?.remove();
    dashboard.querySelector('.v64-dashboard-grid')?.remove();
    const grid=document.getElementById('v64MiniDays');
    if(!grid) return;
    grid.querySelectorAll('.v64-day-btn').forEach(btn=>{
      if(btn.dataset.v69Bound) return;
      btn.dataset.v69Bound='1';
      btn.onclick=function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        const match=String(btn.textContent||'').match(/J(\d+)/i);
        const day=match ? Number(match[1]) : NaN;
        if(!Number.isInteger(day) || day < 1 || day > 91) return;
        if(typeof closeDays==='function') closeDays();
        if(typeof showSection==='function') showSection('program');
        if(typeof requestDayChange==='function') requestDayChange(day);
      };
    });
  }
  function install(){ clean(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,500));
  new MutationObserver(install).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V69 dashboard cleanup applied')
