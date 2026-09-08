from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v67-program-active-fix"' not in s:
    patch = r'''
<script id="v67-program-active-fix">
(function(){
  function syncProgramActive(section){
    const today=document.getElementById('todayNavButton');
    if(!today) return;
    if(section==='program') today.classList.remove('nav-active');
  }
  function install(){
    if(typeof window.showSection!=='function' || window.showSection.__v67Wrapped) return;
    const previous=window.showSection;
    function wrapped(section){
      const result=previous.apply(this,arguments);
      setTimeout(()=>syncProgramActive(section),0);
      return result;
    }
    wrapped.__v67Wrapped=true;
    window.showSection=wrapped;
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,800));
})();
</script>
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V67 program active navigation fix applied')
