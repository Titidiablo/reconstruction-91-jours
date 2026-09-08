from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# V84: status is displayed directly below each file upload button.
s = s.replace(
    '<button class="primary" type="button" id="mediaAudioUpload">⬆️ Ajouter le MP3</button>',
    '<button class="primary" type="button" id="mediaAudioUpload">⬆️ Ajouter le MP3</button><div id="mediaAudioStatus" class="media-status" aria-live="polite"></div>'
)
s = s.replace(
    '<button class="primary" type="button" id="mediaVideoUpload">⬆️ Ajouter le MP4</button>',
    '<button class="primary" type="button" id="mediaVideoUpload">⬆️ Ajouter le MP4</button><div id="mediaVideoStatus" class="media-status" aria-live="polite"></div>'
)

helper = r'''  function setFileStatus(type, text, ok){
    const el=$(type==='audio'?'mediaAudioStatus':'mediaVideoStatus');
    if(!el) return;
    el.textContent=text||'';
    el.className='media-status '+(text?(ok?'success':'error'):'');
  }
'''
if 'function setFileStatus(type, text, ok)' not in s:
    s=s.replace('  async function uploadFileResource(type){', helper+'\n  async function uploadFileResource(type){', 1)

new_fn = r'''  async function uploadFileResource(type){
    const titleEl=$(type==='audio'?'mediaAudioTitle':'mediaVideoTitle');
    const descEl=$(type==='audio'?'mediaAudioDescription':'mediaVideoDescription');
    const fileEl=$(type==='audio'?'mediaAudioFile':'mediaVideoFile');
    const file=fileEl?.files?.[0];
    const title=titleEl?.value.trim();
    if(!title || !file){ setFileStatus(type,'Titre et fichier obligatoires.',false); return; }
    const mime=type==='audio'?'audio/mpeg':'video/mp4';
    const max=type==='audio'?200*1024*1024:500*1024*1024;
    const name=file.name.toLowerCase();
    const validExt=type==='audio'?name.endsWith('.mp3'):name.endsWith('.mp4');
    if(!validExt){ setFileStatus(type,type==='audio'?'Choisis un fichier MP3 (.mp3).':'Choisis un fichier MP4 (.mp4).',false); return; }
    if(file.size>max){ setFileStatus(type,type==='audio'?'MP3 trop volumineux (200 Mo max).':'MP4 trop volumineux (500 Mo max).',false); return; }
    try{
      setFileStatus(type,'Importation en cours… 0 %',true);
      const {client,user}=await currentUser();
      const safeName=name.replace(/[^a-z0-9._-]+/g,'-');
      const path=`${user.id}/${type}/${Date.now()}-${safeName}`;

      if(file.size <= 6*1024*1024){
        setFileStatus(type,'Importation en cours…',true);
        const {error}=await client.storage.from(BUCKET).upload(path,file,{contentType:mime,cacheControl:'3600',upsert:false});
        if(error) throw error;
      } else {
        if(!window.tus || typeof window.tus.Upload!=='function') throw new Error('Le module de téléversement n’est pas chargé. Recharge la page.');
        const {data:{session}}=await client.auth.getSession();
        if(!session?.access_token) throw new Error('Session Supabase absente ou expirée. Reconnecte-toi puis réessaie.');
        const projectRef=new URL(SUPABASE_URL).hostname.split('.')[0];
        const endpoint=`https://${projectRef}.storage.supabase.co/storage/v1/upload/resumable`;
        await new Promise((resolve,reject)=>{
          const upload=new window.tus.Upload(file,{
            endpoint,
            retryDelays:[0,3000,5000,10000,20000],
            chunkSize:6*1024*1024,
            headers:{authorization:`Bearer ${session.access_token}`},
            uploadDataDuringCreation:true,
            removeFingerprintOnSuccess:true,
            metadata:{bucketName:BUCKET,objectName:path,contentType:mime,cacheControl:'3600'},
            onProgress:(uploaded,total)=>setFileStatus(type,`Importation en cours… ${Math.round(uploaded/total*100)} %`,true),
            onError:error=>reject(error),
            onSuccess:()=>resolve()
          });
          upload.start();
        });
      }

      const {error:dbError}=await client.from('personal_resources').insert({user_id:user.id,title,description:descEl?.value.trim()||null,category:type==='audio'?'Méditation':'Développement personnel',media_type:type,storage_path:path});
      if(dbError){
        await client.storage.from(BUCKET).remove([path]);
        throw dbError;
      }
      titleEl.value=''; descEl.value=''; fileEl.value='';
      setFileStatus(type,'Média ajouté avec succès.',true);
      await loadMediaResources();
    }catch(e){
      console.error('V84 media upload',e);
      const detail=e?.message||e?.statusCode||String(e);
      setFileStatus(type,'Échec de l’importation : '+detail,false);
    }
  }
'''

pattern = r'  async function uploadFileResource\(type\)\{.*?\n  \}\n\n  async function addYoutubeResource'
if not re.search(pattern, s, flags=re.S):
    raise SystemExit('V84: uploadFileResource function not found')
s = re.sub(pattern, new_fn + '\n  async function addYoutubeResource', s, count=1, flags=re.S)

p.write_text(s, encoding='utf-8')
print('V84 media upload UI/fallback applied')
