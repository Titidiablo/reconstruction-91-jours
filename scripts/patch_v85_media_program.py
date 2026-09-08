from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V85 — categories explicites à l'import + sélection des MP3 de méditation dans le Programme.

# 1) Ajoute les sélecteurs de catégorie dans les trois formulaires Média.
def add_after_once(source, needle, replacement):
    if replacement in source:
        return source
    if needle not in source:
        raise SystemExit(f'V85: élément introuvable: {needle}')
    return source.replace(needle, needle + replacement, 1)

s = add_after_once(
    s,
    '<input id="mediaAudioTitle" type="text" placeholder="Titre de la méditation">',
    '<label for="mediaAudioCategory">Catégorie</label><select id="mediaAudioCategory"><option value="Méditation">Méditation</option><option value="Développement personnel">Développement personnel</option><option value="Formation">Formation</option><option value="Coaching">Coaching</option><option value="YouTube">YouTube</option><option value="Autre">Autre</option></select>'
)
s = add_after_once(
    s,
    '<input id="mediaVideoTitle" type="text" placeholder="Titre de la vidéo">',
    '<label for="mediaVideoCategory">Catégorie</label><select id="mediaVideoCategory"><option value="Développement personnel">Développement personnel</option><option value="Méditation">Méditation</option><option value="Formation">Formation</option><option value="Coaching">Coaching</option><option value="YouTube">YouTube</option><option value="Autre">Autre</option></select>'
)
s = add_after_once(
    s,
    '<input id="mediaYoutubeTitle" type="text" placeholder="Titre">',
    '<label for="mediaYoutubeCategory">Catégorie</label><select id="mediaYoutubeCategory"><option value="Développement personnel">Développement personnel</option><option value="Méditation">Méditation</option><option value="Formation">Formation</option><option value="Coaching">Coaching</option><option value="YouTube">YouTube</option><option value="Autre">Autre</option></select>'
)

# 2) Remplace la catégorie automatique lors des insertions par la catégorie choisie.
s = s.replace(
    "category:type==='audio'?'Méditation':'Développement personnel',",
    "category:($(type==='audio'?'mediaAudioCategory':'mediaVideoCategory')?.value || (type==='audio'?'Méditation':'Développement personnel')) ,",
    1
)
s = s.replace(
    "category:'Développement personnel', media_type:'youtube'",
    "category:($('mediaYoutubeCategory')?.value || 'Développement personnel'), media_type:'youtube'",
    1
)

# 3) Styles du sélecteur Média + bloc Programme.
style = r'''
<style id="v85-media-program">
.media-form-card label { display:block; font-weight:bold; margin-top:4px; margin-bottom:4px; }
.meditation-media-picker { margin:12px 0 16px; padding:14px 16px; background:#f7f5f1; border:1px solid #ddd9d1; border-radius:10px; }
.meditation-media-picker label { display:block; font-weight:bold; margin-bottom:6px; }
.meditation-media-picker select { margin:0; }
.meditation-media-player { margin-top:10px; }
.meditation-media-player audio { width:100%; max-width:760px; }
.meditation-media-help { color:#777; font-size:13px; margin:6px 0 0; }
</style>
'''
s = re.sub(r'\n<style id="v85-media-program">.*?</style>\s*', '\n', s, flags=re.S)
s = s.replace('</body>', style + '\n</body>', 1)

# 4) Runtime : détecte une section de programme contenant une méditation et propose les MP3
#    dont category = Méditation et media_type = audio.
script = r'''
<script id="v85-media-program">
(function(){
  const MARKER_RE=/\[\[MEDIA_MEDITATION_ID:([^\]]+)\]\]/;
  let pickerTimer=null;

  function $(id){ return document.getElementById(id); }
  function esc(v){ return String(v ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function getClient(){ return typeof getSupabaseClient==='function' ? getSupabaseClient() : null; }

  function programmeHasMeditation(){
    const roots=[$('exerciseContent'),$('interactiveExercise')].filter(Boolean);
    const text=roots.map(r=>r.innerText||r.textContent||'').join(' ').toLowerCase();
    return text.includes('méditation') || text.includes('meditation');
  }

  function removePicker(){
    document.querySelectorAll('.meditation-media-picker').forEach(el=>el.remove());
  }

  function insertPicker(){
    removePicker();
    if(!programmeHasMeditation()) return;
    const targets=[$('exerciseContent'),$('interactiveExercise')].filter(Boolean);
    if(!targets.length) return;
    const host=targets[0];
    const picker=document.createElement('div');
    picker.className='meditation-media-picker';
    picker.id='meditationMediaPicker';
    picker.innerHTML=`<label for="meditationMediaSelect">🎧 Choisir l’audio de méditation</label><select id="meditationMediaSelect"><option value="">— Aucun audio sélectionné —</option></select><p class="meditation-media-help">Les MP3 classés « Méditation » dans 🎧 Média apparaissent ici.</p><div id="meditationMediaPlayer" class="meditation-media-player"></div>`;
    host.parentNode.insertBefore(picker,host);
    $('meditationMediaSelect').addEventListener('change',()=>applySelection());
    loadMeditationChoices();
  }

  async function loadMeditationChoices(){
    const select=$('meditationMediaSelect');
    if(!select) return;
    try{
      const client=getClient();
      if(!client) return;
      const {data:{user}}=await client.auth.getUser();
      if(!user) return;
      const {data,error}=await client.from('personal_resources').select('id,title,description,storage_path,category,media_type,created_at').eq('category','Méditation').eq('media_type','audio').order('created_at',{ascending:false});
      if(error) throw error;
      const saved=findSavedMediaId();
      select.innerHTML='<option value="">— Aucun audio sélectionné —</option>' + (data||[]).map(r=>`<option value="${esc(r.id)}">${esc(r.title)}</option>`).join('');
      if(saved && (data||[]).some(r=>String(r.id)===String(saved))) select.value=saved;
      await applySelection(false);
    }catch(e){
      console.error('V85 meditation media',e);
      select.innerHTML='<option value="">Impossible de charger les méditations</option>';
    }
  }

  function findSavedMediaId(){
    try{
      const entry=window.__v85CurrentEntry;
      const raw=entry?.exercise_response || '';
      const m=String(raw).match(MARKER_RE);
      return m ? m[1] : '';
    }catch(e){ return ''; }
  }

  async function applySelection(markDirty=true){
    const select=$('meditationMediaSelect');
    const player=$('meditationMediaPlayer');
    if(!select || !player) return;
    const id=select.value;
    player.innerHTML='';
    if(!id) return;
    try{
      const client=getClient();
      const {data,error}=await client.from('personal_resources').select('id,title,storage_path,category,media_type').eq('id',id).single();
      if(error) throw error;
      if(data?.storage_path){
        const out=await client.storage.from('personal-resources').createSignedUrl(data.storage_path,3600);
        if(out.error) throw out.error;
        player.innerHTML=`<audio controls preload="metadata" src="${esc(out.data.signedUrl)}"></audio>`;
      }
      if(markDirty && typeof markDirty==='function') markDirty();
    }catch(e){
      console.error('V85 meditation player',e);
      player.textContent='Impossible de charger cet audio.';
    }
  }

  function wrapSave(){
    if(typeof window.buildExerciseResponse==='function' && !window.buildExerciseResponse.__v85){
      const original=window.buildExerciseResponse;
      function wrapped(){
        let value=original.apply(this,arguments);
        const id=$('meditationMediaSelect')?.value || '';
        value=String(value||'').replace(/\[\[MEDIA_MEDITATION_ID:[^\]]+\]\]/g,'').trim();
        if(id) value += `\n[[MEDIA_MEDITATION_ID:${id}]]`;
        return value;
      }
      wrapped.__v85=true;
      window.buildExerciseResponse=wrapped;
    }
  }

  function wrapLoad(){
    if(typeof window.loadExistingEntry==='function' && !window.loadExistingEntry.__v85){
      const original=window.loadExistingEntry;
      async function wrapped(entry){
        window.__v85CurrentEntry=entry||null;
        const result=await original.apply(this,arguments);
        window.setTimeout(insertPicker,50);
        return result;
      }
      wrapped.__v85=true;
      window.loadExistingEntry=wrapped;
    }
  }

  function watch(){
    wrapSave();
    wrapLoad();
    clearTimeout(pickerTimer);
    pickerTimer=setTimeout(()=>{
      if($('programSection') && !$('programSection').classList.contains('hidden')) insertPicker();
    },80);
  }

  function init(){
    wrapSave();
    wrapLoad();
    watch();
    new MutationObserver(watch).observe(document.body,{childList:true,subtree:true});
    window.addEventListener('load',()=>setTimeout(watch,500));
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>
'''

s = re.sub(r'\n<script id="v85-media-program">.*?</script>\s*', '\n', s, flags=re.S)
s = s.replace('</body>', script + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
print('V85 media categories + meditation picker applied')
