from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove any previous V81 patch before rebuilding it.
import re
s = re.sub(r'\n<style id="v81-media-menu">.*?</style>\s*<script id="v81-media-menu">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v81-media-menu">
.media-library { margin-top: 10px; }
.media-intro { color:#666; margin-top:-8px; }
.media-upload-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.media-form-card { background:#f7f5f1; border:1px solid #ddd9d1; border-radius:12px; padding:18px; }
.media-form-card h3 { margin-top:0; }
.media-resource-list { display:grid; gap:14px; margin-top:18px; }
.media-resource { border:1px solid #ddd9d1; border-radius:12px; padding:16px; background:#fff; }
.media-resource-head { display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }
.media-resource-title { font-size:18px; font-weight:bold; margin:0; }
.media-resource-meta { color:#777; font-size:13px; margin:3px 0 10px; }
.media-resource audio, .media-resource video { width:100%; max-width:760px; margin-top:8px; border-radius:8px; }
.media-resource iframe { width:100%; min-height:315px; border:0; border-radius:8px; margin-top:8px; }
.media-resource-description { white-space:pre-wrap; margin:8px 0; }
.media-resource-actions { margin-top:10px; }
.media-empty { color:#777; text-align:center; padding:28px 10px; }
.media-status { min-height:22px; margin-top:8px; }
.media-status.success { color:#26733d; }
.media-status.error { color:#a00; }
.media-delete { background:#eee; color:#a00; }
@media (max-width:700px) { .media-upload-grid { grid-template-columns:1fr; } }
</style>
<script id="v81-media-menu">
(function(){
  const BUCKET = 'personal-resources';
  const MAX_AUDIO = 200 * 1024 * 1024;
  const MAX_VIDEO = 500 * 1024 * 1024;

  function $(id){ return document.getElementById(id); }
  function esc(value){
    return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function youtubeId(url){
    try {
      const u = new URL(url);
      if (u.hostname === 'youtu.be') return u.pathname.slice(1).split('/')[0];
      if (u.hostname === 'youtube.com' || u.hostname === 'www.youtube.com' || u.hostname.endsWith('.youtube.com')) {
        if (u.pathname === '/watch') return u.searchParams.get('v');
        const m = u.pathname.match(/^\/(embed|shorts)\/([^/?]+)/);
        return m ? m[2] : null;
      }
    } catch(e) {}
    return null;
  }
  function isYoutube(url){ return !!youtubeId(url); }
  function setStatus(text, ok){
    const el=$('mediaStatus');
    if(!el) return;
    el.textContent=text || '';
    el.className='media-status ' + (text ? (ok ? 'success' : 'error') : '');
  }
  function getClient(){ return typeof getSupabaseClient === 'function' ? getSupabaseClient() : null; }

  function buildSection(){
    if ($('mediaSection')) return;
    const sec=document.createElement('section');
    sec.id='mediaSection';
    sec.className='card hidden media-library';
    sec.innerHTML=`
      <h2 class="section-title">🎧 Média</h2>
      <p class="media-intro">Tes supports personnels pour la méditation et le développement personnel.</p>
      <div class="media-upload-grid">
        <div class="media-form-card">
          <h3>🧘 Ajouter une méditation audio</h3>
          <input id="mediaAudioTitle" type="text" placeholder="Titre de la méditation">
          <textarea id="mediaAudioDescription" placeholder="Description (facultative)"></textarea>
          <input id="mediaAudioFile" type="file" accept="audio/mpeg,.mp3">
          <button class="primary" type="button" id="mediaAudioUpload">⬆️ Ajouter le MP3</button>
        </div>
        <div class="media-form-card">
          <h3>🧠 Ajouter une vidéo</h3>
          <input id="mediaVideoTitle" type="text" placeholder="Titre de la vidéo">
          <textarea id="mediaVideoDescription" placeholder="Description (facultative)"></textarea>
          <input id="mediaVideoFile" type="file" accept="video/mp4,.mp4">
          <button class="primary" type="button" id="mediaVideoUpload">⬆️ Ajouter le MP4</button>
        </div>
      </div>
      <div class="media-form-card" style="margin-top:16px;">
        <h3>▶️ Ajouter une ressource YouTube</h3>
        <input id="mediaYoutubeTitle" type="text" placeholder="Titre">
        <textarea id="mediaYoutubeDescription" placeholder="Description (facultative)"></textarea>
        <input id="mediaYoutubeUrl" type="url" placeholder="https://www.youtube.com/watch?v=..."><br>
        <button class="primary" type="button" id="mediaYoutubeAdd">＋ Ajouter le lien YouTube</button>
      </div>
      <div id="mediaStatus" class="media-status" aria-live="polite"></div>
      <h3 style="margin-top:26px;">📚 Mes médias</h3>
      <div id="mediaResourceList" class="media-resource-list"><div class="media-empty">Chargement…</div></div>
    `;
    document.body.appendChild(sec);
    $('mediaAudioUpload').addEventListener('click',()=>uploadFileResource('audio'));
    $('mediaVideoUpload').addEventListener('click',()=>uploadFileResource('video'));
    $('mediaYoutubeAdd').addEventListener('click',addYoutubeResource);
  }

  function installNav(){
    const nav=document.querySelector('.nav-buttons');
    if(!nav || $('mediaNavButton')) return false;
    const btn=document.createElement('button');
    btn.id='mediaNavButton';
    btn.type='button';
    btn.textContent='🎧 Média';
    nav.appendChild(btn);
    btn.addEventListener('click', showMedia);
    return true;
  }

  function hideMainSections(){
    ['programSection','journalSection','evolutionSection','v61Dashboard','v64Dashboard','v63Resources','mediaSection'].forEach(id=>{
      const el=$(id); if(el) el.classList.add('hidden');
    });
    document.querySelectorAll('.nav-buttons button').forEach(b=>b.classList.remove('nav-active'));
  }

  function showMedia(){
    buildSection();
    hideMainSections();
    const sec=$('mediaSection');
    if(sec) sec.classList.remove('hidden');
    $('mediaNavButton')?.classList.add('nav-active');
    loadMediaResources();
  }

  function bindExistingNav(){
    document.querySelectorAll('.nav-buttons button').forEach(btn=>{
      if(btn.dataset.v81MediaBound || btn.id==='mediaNavButton') return;
      btn.dataset.v81MediaBound='1';
      btn.addEventListener('click',()=>{
        if(btn.id!=='mediaNavButton') setTimeout(()=>{ $('mediaSection')?.classList.add('hidden'); },0);
      });
    });
  }

  async function currentUser(){
    const client=getClient();
    if(!client) throw new Error('Supabase n\'est pas disponible.');
    const {data,error}=await client.auth.getUser();
    if(error) throw error;
    if(!data?.user) throw new Error('Tu dois être connecté pour gérer tes médias.');
    return {client,user:data.user};
  }

  async function uploadFileResource(type){
    const titleEl=$(type==='audio'?'mediaAudioTitle':'mediaVideoTitle');
    const descEl=$(type==='audio'?'mediaAudioDescription':'mediaVideoDescription');
    const fileEl=$(type==='audio'?'mediaAudioFile':'mediaVideoFile');
    const file=fileEl?.files?.[0];
    const title=titleEl?.value.trim();
    if(!title || !file){ setStatus('Titre et fichier obligatoires.',false); return; }
    const mime=type==='audio'?'audio/mpeg':'video/mp4';
    const max=type==='audio'?MAX_AUDIO:MAX_VIDEO;
    if(file.type && file.type!==mime){ setStatus(type==='audio'?'Choisis un fichier MP3.':'Choisis un fichier MP4.',false); return; }
    if(file.size>max){ setStatus(type==='audio'?'MP3 trop volumineux (200 Mo max).':'MP4 trop volumineux (500 Mo max).',false); return; }
    try{
      setStatus('Téléversement en cours…',true);
      const {client,user}=await currentUser();
      const safeName=file.name.toLowerCase().replace(/[^a-z0-9._-]+/g,'-');
      const path=`${user.id}/${type}/${Date.now()}-${safeName}`;
      const {error:uploadError}=await client.storage.from(BUCKET).upload(path,file,{contentType:mime,upsert:false});
      if(uploadError) throw uploadError;
      const {error:dbError}=await client.from('personal_resources').insert({
        user_id:user.id,
        title,
        description:descEl?.value.trim() || null,
        category:type==='audio'?'Méditation':'Développement personnel',
        media_type:type,
        storage_path:path
      });
      if(dbError) throw dbError;
      titleEl.value=''; descEl.value=''; fileEl.value='';
      setStatus('Média ajouté.',true);
      await loadMediaResources();
    }catch(e){ console.error(e); setStatus('Impossible d’ajouter le média : '+(e.message||e),false); }
  }

  async function addYoutubeResource(){
    const title=$('mediaYoutubeTitle')?.value.trim();
    const description=$('mediaYoutubeDescription')?.value.trim();
    const url=$('mediaYoutubeUrl')?.value.trim();
    if(!title || !url){ setStatus('Titre et lien YouTube obligatoires.',false); return; }
    if(!isYoutube(url)){ setStatus('Le lien doit être un lien YouTube valide.',false); return; }
    try{
      const {client,user}=await currentUser();
      const {error}=await client.from('personal_resources').insert({user_id:user.id,title,description:description||null,category:'Développement personnel',media_type:'youtube',url});
      if(error) throw error;
      $('mediaYoutubeTitle').value=''; $('mediaYoutubeDescription').value=''; $('mediaYoutubeUrl').value='';
      setStatus('Lien YouTube ajouté.',true);
      await loadMediaResources();
    }catch(e){ console.error(e); setStatus('Impossible d’ajouter le lien : '+(e.message||e),false); }
  }

  async function loadMediaResources(){
    const list=$('mediaResourceList');
    if(!list) return;
    try{
      const {client}=await currentUser();
      const {data,error}=await client.from('personal_resources').select('*').order('created_at',{ascending:false});
      if(error) throw error;
      if(!data?.length){ list.innerHTML='<div class="media-empty">Aucun média pour le moment.</div>'; return; }
      const signed={};
      for(const r of data){
        if(r.storage_path){
          const out=await client.storage.from(BUCKET).createSignedUrl(r.storage_path,3600);
          if(!out.error && out.data?.signedUrl) signed[r.id]=out.data.signedUrl;
        }
      }
      list.innerHTML=data.map(r=>renderResource(r,signed[r.id]||'')).join('');
      list.querySelectorAll('[data-media-delete]').forEach(btn=>btn.addEventListener('click',()=>deleteResource(btn.dataset.mediaDelete)));
    }catch(e){ console.error(e); list.innerHTML='<div class="media-empty">Impossible de charger les médias. Vérifie la connexion et la session.</div>'; }
  }

  function renderResource(r,signedUrl){
    const desc=r.description?`<div class="media-resource-description">${esc(r.description)}</div>`:'';
    let body='';
    if(r.media_type==='audio' && signedUrl) body=`<audio controls preload="metadata" src="${esc(signedUrl)}"></audio>`;
    else if(r.media_type==='video' && signedUrl) body=`<video controls preload="metadata" src="${esc(signedUrl)}"></video>`;
    else if(r.media_type==='youtube'){
      const id=youtubeId(r.url||'');
      body=id?`<iframe src="https://www.youtube.com/embed/${encodeURIComponent(id)}" title="${esc(r.title)}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`:`<a href="${esc(r.url||'#')}" target="_blank" rel="noopener noreferrer">Ouvrir sur YouTube</a>`;
    } else if(r.url) body=`<a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">Ouvrir la ressource</a>`;
    return `<article class="media-resource"><div class="media-resource-head"><div><h4 class="media-resource-title">${esc(r.title)}</h4><div class="media-resource-meta">${esc(r.category)} · ${esc(r.media_type)}</div></div><button type="button" class="media-delete" data-media-delete="${esc(r.id)}">🗑️ Supprimer</button></div>${desc}${body}<div class="media-resource-actions"></div></article>`;
  }

  async function deleteResource(id){
    if(!id || !confirm('Supprimer cette ressource ?')) return;
    try{
      const {client}=await currentUser();
      const {data,error}=await client.from('personal_resources').select('id,storage_path').eq('id',id).single();
      if(error) throw error;
      if(data?.storage_path) await client.storage.from(BUCKET).remove([data.storage_path]);
      const {error:deleteError}=await client.from('personal_resources').delete().eq('id',id);
      if(deleteError) throw deleteError;
      setStatus('Ressource supprimée.',true);
      await loadMediaResources();
    }catch(e){ console.error(e); setStatus('Impossible de supprimer la ressource : '+(e.message||e),false); }
  }

  function init(){
    buildSection();
    installNav();
    bindExistingNav();
    window.setTimeout(()=>{ installNav(); bindExistingNav(); },500);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
'''

s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V81 media menu applied')
