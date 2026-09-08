from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V87 — préremplit le titre des imports MP3/MP4 avec le nom du fichier sélectionné.
patch = r'''
<style id="v87-media-filename-title">
</style>
<script id="v87-media-filename-title">
(function(){
  function $(id){ return document.getElementById(id); }
  function filenameWithoutExtension(name){
    return String(name || '').replace(/\\.(mp3|mp4)$/i,'');
  }
  function bind(){
    const audioFile=$('mediaAudioFile');
    const audioTitle=$('mediaAudioTitle');
    const videoFile=$('mediaVideoFile');
    const videoTitle=$('mediaVideoTitle');
    if(audioFile && audioTitle && !audioFile.dataset.v87Bound){
      audioFile.dataset.v87Bound='1';
      audioFile.addEventListener('change',()=>{
        const file=audioFile.files?.[0];
        if(file) audioTitle.value=filenameWithoutExtension(file.name);
      });
    }
    if(videoFile && videoTitle && !videoFile.dataset.v87Bound){
      videoFile.dataset.v87Bound='1';
      videoFile.addEventListener('change',()=>{
        const file=videoFile.files?.[0];
        if(file) videoTitle.value=filenameWithoutExtension(file.name);
      });
    }
  }
  function init(){
    bind();
    setInterval(bind,700);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>
'''
s = re.sub(r'\n<style id="v87-media-filename-title">.*?</style>\s*', '\n', s, flags=re.S)
s = re.sub(r'\n<script id="v87-media-filename-title">.*?</script>\s*', '\n', s, flags=re.S)
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V87 media filename title applied')
