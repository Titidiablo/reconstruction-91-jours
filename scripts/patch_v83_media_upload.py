from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V83: TUS resumable uploads + direct Supabase Storage hostname.
if 'tus-js-client@4' not in s:
    s = s.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/tus-js-client@4/dist/tus.min.js"></script>\n</head>', 1)

new_fn = r'''  async function uploadFileResource(type){
    const titleEl=$(type==='audio'?'mediaAudioTitle':'mediaVideoTitle');
    const descEl=$(type==='audio'?'mediaAudioDescription':'mediaVideoDescription');
    const fileEl=$(type==='audio'?'mediaAudioFile':'mediaVideoFile');
    const file=fileEl?.files?.[0];
    const title=titleEl?.value.trim();
    if(!title || !file){ setStatus('Titre et fichier obligatoires.',false); return; }
    const mime=type==='audio'?'audio/mpeg':'video/mp4';
    const max=type==='audio'?200*1024*1024:500*1024*1024;
    const name=file.name.toLowerCase();
    const validExt=type==='audio'?name.endsWith('.mp3'):name.endsWith('.mp4');
    if(!validExt){ setStatus(type==='audio'?'Choisis un fichier MP3 (.mp3).':'Choisis un fichier MP4 (.mp4).',false); return; }
    if(file.size>max){ setStatus(type==='audio'?'MP3 trop volumineux (200 Mo max).':'MP4 trop volumineux (500 Mo max).',false); return; }
    try{
      setStatus('Téléversement en cours… 0 %',true);
      const {client,user}=await currentUser();
      if(!window.tus || typeof window.tus.Upload!=='function') throw new Error('Le module de téléversement n’est pas chargé. Recharge la page.');
      const {data:{session}}=await client.auth.getSession();
      if(!session?.access_token) throw new Error('Session Supabase absente ou expirée. Reconnecte-toi puis réessaie.');
      const projectRef=new URL(SUPABASE_URL).hostname.split('.')[0];
      const endpoint=`https://${projectRef}.storage.supabase.co/storage/v1/upload/resumable`;
      const safeName=name.replace(/[^a-z0-9._-]+/g,'-');
      const path=`${user.id}/${type}/${Date.now()}-${safeName}`;
      await new Promise((resolve,reject)=>{
        const upload=new window.tus.Upload(file,{
          endpoint,
          retryDelays:[0,1000,3000,5000,10000],
          chunkSize:6*1024*1024,
          headers:{authorization:`Bearer ${session.access_token}`,apikey:SUPABASE_KEY},
          metadata:{bucketName:BUCKET,objectName:path,contentType:mime,cacheControl:'3600'},
          onProgress:(bytesUploaded,bytesTotal)=>setStatus(`Téléversement en cours… ${Math.round(bytesUploaded/bytesTotal*100)} %`,true),
          onError:error=>reject(error),
          onSuccess:()=>resolve()
        });
        upload.start();
      });
      const {error:dbError}=await client.from('personal_resources').insert({user_id:user.id,title,description:descEl?.value.trim()||null,category:type==='audio'?'Méditation':'Développement personnel',media_type:type,storage_path:path});
      if(dbError) throw dbError;
      titleEl.value=''; descEl.value=''; fileEl.value='';
      setStatus('Média ajouté avec succès.',true);
      await loadMediaResources();
    }catch(e){ console.error('V83 media upload',e); setStatus('Impossible d’ajouter le média : '+(e.message||e),false); }
  }
'''

pattern = r'  async function uploadFileResource\(type\)\{.*?\n  \}\n\n  async function addYoutubeResource'
if not re.search(pattern, s, flags=re.S):
    raise SystemExit('V83: uploadFileResource function not found')
s = re.sub(pattern, new_fn + '\n  async function addYoutubeResource', s, count=1, flags=re.S)
p.write_text(s, encoding='utf-8')
print('V83 media upload patch applied')
