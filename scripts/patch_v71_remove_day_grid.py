from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v71-remove-day-grid"' not in s:
    patch = r'''
<style id="v71-remove-day-grid">
/* V71 — aucune grille des 91 jours dans l'interface */
#v64Dashboard .v64-days-card,
#v61Dashboard .v70-days-card,
#v64DayModal,
#v64OpenDays,
#v64CompactDays,
#daysNavButton { display:none !important; }
</style>
<script id="v71-remove-day-grid">
(function(){
  function removeDayGrid(){
    document.querySelectorAll('.v64-days-card, .v70-days-card, #v64DayModal, #v64OpenDays, #v64CompactDays, #daysNavButton, .v64-day-modal').forEach(el=>el.remove());
    document.querySelectorAll('.v64-day-btn').forEach(el=>el.remove());
  }
  function install(){ removeDayGrid(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',install);
  else install();
  window.addEventListener('load',()=>setTimeout(install,500));
  new MutationObserver(install).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
    s = s.replace('</body>', patch + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V71 day grid removed everywhere')
