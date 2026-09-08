from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = re.sub(r'\n<style id="v93-zen-images">.*?</style>\s*<script id="v93-zen-images">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v93-zen-images">
/* V93 — touches visuelles zen discrètes, sans modifier la structure fonctionnelle. */
.zen-image-banner{
  position:relative;
  min-height:170px;
  margin:0 0 20px;
  border-radius:20px;
  overflow:hidden;
  background-image:linear-gradient(90deg,rgba(53,48,39,.38),rgba(53,48,39,.08)),url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1600&q=82');
  background-size:cover;
  background-position:center 58%;
  display:flex;
  align-items:flex-end;
  padding:24px 28px;
  box-shadow:0 7px 24px rgba(75,64,52,.10);
  color:#fffdf8;
}
.zen-image-banner h2{margin:0;color:#fffdf8 !important;font-family:Georgia,'Times New Roman',serif;font-size:27px;line-height:1.2;text-shadow:0 1px 8px rgba(0,0,0,.25)}
.zen-image-banner p{margin:5px 0 0;color:#fffdf8;font-style:italic;opacity:.96}

#meditation{position:relative;overflow:hidden}
#meditation::after{
  content:"";
  position:absolute;
  right:-20px;
  bottom:-35px;
  width:190px;
  height:150px;
  border-radius:50%;
  background-image:linear-gradient(135deg,rgba(244,240,229,.15),rgba(244,240,229,.82)),url('https://images.unsplash.com/photo-1545389336-cf090694435e?auto=format&fit=crop&w=700&q=80');
  background-size:cover;
  background-position:center;
  opacity:.20;
  pointer-events:none;
}

.zen-motivation-image{
  min-height:125px;
  margin:18px 0 4px;
  border-radius:16px;
  background-image:linear-gradient(90deg,rgba(54,48,40,.25),rgba(54,48,40,.03)),url('https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=80');
  background-size:cover;
  background-position:center 62%;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:22px;
  color:#fffdf8;
  text-align:center;
  box-shadow:0 4px 18px rgba(75,64,52,.08);
}
.zen-motivation-image span{
  font-family:Georgia,'Times New Roman',serif;
  font-size:20px;
  font-style:italic;
  text-shadow:0 1px 7px rgba(0,0,0,.30);
}

.zen-journal-image{
  float:right;
  width:210px;
  height:82px;
  margin:0 0 10px 18px;
  border-radius:14px;
  background-image:url('https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=700&q=80');
  background-size:cover;
  background-position:center;
  opacity:.82;
}

@media(max-width:700px){
  .zen-image-banner{min-height:145px;padding:20px;border-radius:16px}
  .zen-image-banner h2{font-size:23px}
  .zen-journal-image{float:none;width:100%;height:105px;margin:12px 0}
  .zen-motivation-image{min-height:110px}
}
</style>
<script id="v93-zen-images">
(function(){
  function addImageTouches(){
    const program=document.getElementById('programSection');
    if(!program || program.classList.contains('hidden')) return;
    if(!document.getElementById('zenImageBanner')){
      const banner=document.createElement('div');
      banner.id='zenImageBanner';
      banner.className='zen-image-banner';
      banner.innerHTML='<div><h2>Un moment pour soi</h2><p>Respire. Recentre-toi. Avance.</p></div>';
      const first=program.querySelector('.card');
      if(first) first.parentNode.insertBefore(banner,first);
    }
    const journal=program.querySelector('.journal-entry');
    if(journal && !journal.querySelector('.zen-journal-image')){
      const img=document.createElement('div');
      img.className='zen-journal-image';
      journal.prepend(img);
    }
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',addImageTouches); else addImageTouches();
  setInterval(addImageTouches,1000);
})();
</script>
'''
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V93 zen images applied')
