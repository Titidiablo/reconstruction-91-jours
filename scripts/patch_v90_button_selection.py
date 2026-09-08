from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = re.sub(r'\n<style id="v90-button-selection-fix">.*?</style>\s*<script id="v90-button-selection-fix">.*?</script>\s*', '\n', s, flags=re.S)
patch = r'''
<style id="v90-button-selection-fix">
.nav-buttons button.nav-active { background:#222 !important; color:white !important; }
</style>
<script id="v90-button-selection-fix">
(function(){
  function clear(){ document.querySelectorAll('.nav-buttons button.nav-active').forEach(b=>b.classList.remove('nav-active')); }
  function select(btn){
    if(!btn || !btn.closest('.nav-buttons')) return;
    document.querySelectorAll('.nav-buttons button.nav-active').forEach(b=>{if(b!==btn)b.classList.remove('nav-active');});
    btn.classList.add('nav-active');
  }
  function install(){
    document.querySelectorAll('.nav-buttons button').forEach(btn=>{
      if(btn.dataset.v90Bound)return;
      btn.dataset.v90Bound='1';
      btn.addEventListener('click',function(){select(this);},true);
      btn.addEventListener('click',()=>setTimeout(sync,0));
    });
  }
  function sync(){
    install();
    const program=document.getElementById('programSection');
    const today=document.getElementById('todayNavButton');
    const dash=document.getElementById('dashboardNavButton');
    if(program && !program.classList.contains('hidden')){
      clear();
      const b=[...document.querySelectorAll('.nav-buttons button')].find(x=>/Programme/i.test(x.textContent||''));
      if(b)b.classList.add('nav-active');
    } else if(today && today.classList.contains('nav-active')){
      clear(); today.classList.add('nav-active');
    } else if(dash && dash.classList.contains('nav-active')){
      clear(); dash.classList.add('nav-active');
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',sync);else sync();
  window.addEventListener('load',()=>setTimeout(sync,500));
  setInterval(install,1000);
})();
</script>
'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('V90 button selection fix applied')
