from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v68-dashboard-program-fix"' not in s:
    patch = r'''
<style id="v68-dashboard-program-fix">
/* V68 — Aujourd'hui = cockpit ; Programme = travail du jour */
#v64Dashboard .v64-days-card { display:block !important; }
#v64Dashboard .v64-actions #v64OpenDays,
#v64Dashboard .v64-days-head #v64CompactDays { display:none !important; }
#v64Dashboard .v64-days-card { margin-top:18px; }
</style>
<script id="v68-dashboard-program-fix">
(function(){
  function bind(){
    const grid=document.getElementById('v64MiniDays');
    if(!grid || grid.dataset.v68Bound) return;
    grid.dataset.v68Bound='1';
    grid.addEventListener('click',function(e){
      const btn=e.target.closest('.v64-day-btn');
      if(!btn) return;
      e.preventDefault();
      const match=String(btn.textContent||'').match(/J(\d+)/i);
      if(!match) return;
      const day=Number(match[1]);
      if(!Number.isInteger(day)) return;
      if(typeof closeDays==='function') closeDays();
      if(typeof showSection==='function') showSection('program');
      if(typeof requestDayChange==='function') requestDayChange(day);
    });
  }
  function install(){ bind(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,500));
  new MutationObserver(install).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V68 dashboard/program separation applied')
