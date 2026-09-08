from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V89 — le sélecteur audio est placé directement sous le texte du bloc Méditation (#meditation).
patch = r'''
<style id="v89-meditation-picker-exact-position">
#meditation + .meditation-media-picker { margin-top:12px; margin-bottom:16px; }
</style>
<script id="v89-meditation-picker-exact-position">
(function(){
  function movePicker(){
    const picker=document.getElementById('meditationMediaPicker');
    const meditation=document.getElementById('meditation');
    if(!picker || !meditation) return;
    if(meditation.nextElementSibling !== picker){
      meditation.insertAdjacentElement('afterend', picker);
    }
  }
  function init(){
    movePicker();
    setInterval(movePicker,700);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>
'''
s = re.sub(r'\n<style id="v89-meditation-picker-exact-position">.*?</style>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<script id="v89-meditation-picker-exact-position">.*?</script>\s*', '\n', s, flags=re.S)
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V89 exact meditation picker position applied')
