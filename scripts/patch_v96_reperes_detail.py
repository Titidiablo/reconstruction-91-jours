from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = re.sub(r'\n<style id="v96-reperes-detail">.*?</style>\s*<script id="v96-reperes-detail">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v96-reperes-detail">
.v96-record-details{margin-top:14px;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.v96-record-detail{padding:15px 16px;border:1px solid #ddd8cf;border-radius:14px;background:#fff}
.v96-record-detail h3{margin:0 0 7px;font-size:16px}
.v96-record-detail p{margin:0;color:#555;line-height:1.55;font-size:14px}
.v96-record-detail .number{font-size:23px;font-weight:800;color:#333}
.v96-record-detail .small{display:block;margin-top:3px;color:#777;font-size:12px}
.v96-record-detail .meaning{margin-top:8px;padding-top:8px;border-top:1px solid #eee9e3}
@media(max-width:700px){.v96-record-details{grid-template-columns:1fr}}
</style>
<script id="v96-reperes-detail">
(function(){
  const D=[
    ['presence','🧘 Pleine conscience'],
    ['impulse_control','🔥 Maîtrise des impulsions'],
    ['values_coherence','🧭 Cohérence avec mes valeurs'],
    ['self_relation','❤️ Relation à moi-même']
  ];
  const n=v=>{const x=Number(v);return Number.isFinite(x)?x:null};
  const avg=(rows,k)=>{const a=rows.map(r=>n(r[k])).filter(x=>x!==null);return a.length?a.reduce((x,y)=>x+y,0)/a.length:null};
  const overall=r=>{const a=D.map(d=>n(r[d[0]])).filter(x=>x!==null);return a.length?a.reduce((x,y)=>x+y,0)/a.length:null};
  function render(){
    const box=document.getElementById('v94Records');
    const rows=(typeof dailyScoreHistory!=='undefined'?dailyScoreHistory:[]).filter(r=>Number.isFinite(Number(r.day_number))).sort((a,b)=>Number(a.day_number)-Number(b.day_number));
    if(!box||!rows.length)return;
    const scored=rows.map(r=>({r,v:overall(r)})).filter(x=>x.v!==null);
    const best=scored.length?[...scored].sort((a,b)=>b.v-a.v)[0]:null;
    const first=rows[0],recent=rows.slice(-7),prev=rows.slice(-14,-7);
    const growth=D.map(d=>({d,delta:(avg(recent,d[0])??0)-(n(first[d[0]])??avg(recent,d[0])??0)})).sort((a,b)=>b.delta-a.delta);
    const fastest=growth[0];
    const bestPillar=D.map(d=>({d,v:avg(rows,d[0])})).filter(x=>x.v!==null).sort((a,b)=>b.v-a.v)[0];
    const recentAvg=recent.map(overall).filter(x=>x!==null);const ra=recentAvg.length?recentAvg.reduce((a,b)=>a+b,0)/recentAvg.length:null;
    const prevAvg=prev.map(overall).filter(x=>x!==null);const pa=prevAvg.length?prevAvg.reduce((a,b)=>a+b,0)/prevAvg.length:null;
    const existing=document.getElementById('v96RecordsDetails');
    if(existing){existing.innerHTML=build();return;}
    const wrap=document.createElement('div');wrap.id='v96RecordsDetails';wrap.className='v96-record-details';wrap.innerHTML=build();box.parentNode.insertBefore(wrap,box.nextSibling);
    function build(){return `
      <div class="v96-record-detail"><h3>🏆 Ton meilleur repère</h3><p>${best?`Ton meilleur score global est de <span class="number">${best.v.toFixed(1)}/10</span> au <strong>Jour ${best.r.day_number}</strong>.`:'Ton meilleur repère apparaîtra lorsque plusieurs journées auront été renseignées.'}<span class="small">Ce moment peut devenir un repère : qu’est-ce qui t’a aidé ce jour-là ?</span></p></div>
      <div class="v96-record-detail"><h3>📈 Ta plus belle progression</h3><p>${fastest?`<strong>${fastest.d[1]}</strong> est actuellement la dimension qui a le plus progressé depuis le début : <span class="number">${fastest.delta>=0?'+':''}${fastest.delta.toFixed(1)}</span>.`:'Les données se construisent progressivement.'}<span class="small">Ce que tu construis mérite d’être reconnu, même lorsque la progression est progressive.</span></p></div>
      <div class="v96-record-detail"><h3>🌟 Ton pilier le plus solide</h3><p>${bestPillar?`Sur l’ensemble des journées renseignées, <strong>${bestPillar.d[1]}</strong> présente actuellement la moyenne la plus élevée : <span class="number">${bestPillar.v.toFixed(1)}/10</span>.`:'Ce repère apparaîtra avec davantage de données.'}<span class="small">C’est une ressource sur laquelle tu peux t’appuyer pour continuer ton chemin.</span></p></div>
      <div class="v96-record-detail"><h3>🌱 Ton évolution récente</h3><p>${ra!==null&&pa!==null?`Ta moyenne des 7 dernières journées est de <span class="number">${ra.toFixed(1)}/10</span>, contre ${pa.toFixed(1)}/10 sur les 7 précédentes, soit <strong>${ra-pa>=0?'+':''}${(ra-pa).toFixed(1)}</strong>.`:'Les périodes se rempliront progressivement.'}<span class="small">Une période stable est elle aussi une étape : elle permet de consolider les changements.</span></p></div>`}
  }
  function init(){render();setInterval(render,900)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(init,300));else setTimeout(init,300);
})();
</script>
'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('V96 detailed repères applied')
