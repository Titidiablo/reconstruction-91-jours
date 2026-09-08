from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = re.sub(r'\n<style id="v95-bilan-piliers">.*?</style>\s*<script id="v95-bilan-piliers">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v95-bilan-piliers">
.v95-pillars{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0}
.v95-pillar{padding:15px 16px;border:1px solid #ddd8cf;border-radius:14px;background:#fff}
.v95-pillar-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:6px}
.v95-pillar-title{font-weight:800;font-size:15px}
.v95-pillar-score{font-weight:800;font-size:18px;white-space:nowrap}
.v95-pillar-text{margin:0;color:#555;line-height:1.55;font-size:14px}
.v95-pillar-path{margin-top:7px;color:#777;font-size:12px;font-style:italic}
.v95-encouragement{margin-top:18px;padding:18px;border-radius:14px;background:linear-gradient(135deg,#f7f5f1,#fffdf8);border:1px solid #ddd8cf;text-align:center}
.v95-encouragement p{margin:0;color:#4e4a43;line-height:1.65}
.v95-encouragement .main{font-family:Georgia,serif;font-size:19px;font-weight:700}
.v95-encouragement .sub{margin-top:7px;font-size:14px}
@media(max-width:700px){.v95-pillars{grid-template-columns:1fr}}
</style>
<script id="v95-bilan-piliers">
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
  function phrase(label,cur,base){
    if(cur===null) return 'Pas encore assez de données pour tirer une conclusion. Les prochaines journées permettront de voir plus clairement ce qui évolue.';
    const delta=base!==null?cur-base:null;
    if(delta!==null && delta>=0.7) return 'Cette dimension évolue bien. Les efforts commencent à produire des repères concrets : continue à entretenir ce que tu es en train de construire.';
    if(delta!==null && delta>=0.2) return 'La progression est encourageante. Le changement est en train de s’installer, même s’il demande encore de la régularité.';
    if(delta!==null && delta<=-0.7) return 'Il reste encore du chemin sur cette dimension. Ce n’est pas un recul définitif : c’est une information qui peut t’aider à ajuster ta pratique et à persévérer.';
    if(delta!==null && delta<=-0.2) return 'Cette dimension demande encore de l’attention. Les variations font partie du parcours : accroche-toi et continue à observer ce qui t’aide réellement.';
    return 'Cette dimension est encore en construction. Rien n’est figé : la répétition des petits pas peut faire évoluer durablement les choses.';
  }
  function path(label,cur,base){
    if(cur===null)return 'À construire au fil des prochaines journées.';
    const delta=base!==null?cur-base:null;
    if(delta!==null&&delta>=0.2)return 'À poursuivre : consolider les habitudes qui fonctionnent déjà.';
    if(delta!==null&&delta<=-0.2)return 'À travailler : revenir aux exercices et observer les déclencheurs sans se juger.';
    return 'À approfondir : transformer progressivement l’intention en habitudes concrètes.';
  }
  function render(){
    const box=document.getElementById('v94Reflection');
    const rows=(typeof dailyScoreHistory!=='undefined'?dailyScoreHistory:[]).filter(r=>Number.isFinite(Number(r.day_number))).sort((a,b)=>Number(a.day_number)-Number(b.day_number));
    if(!box||!rows.length)return;
    const recent=rows.slice(-7);
    const first=rows[0];
    const key=rows.length+'|'+recent.map(r=>r.day_number+':'+D.map(d=>r[d[0]]??'').join(',')).join('|');
    if(box.dataset.v95Key===key)return;
    box.dataset.v95Key=key;
    const cards=D.map(d=>{
      const cur=avg(recent,d[0])??avg(rows,d[0]);
      const base=n(first[d[0]]);
      return `<div class="v95-pillar"><div class="v95-pillar-head"><div class="v95-pillar-title">${d[1]}</div><div class="v95-pillar-score">${cur===null?'—':cur.toFixed(1)}/10</div></div><p class="v95-pillar-text">${phrase(d[1],cur,base)}</p><div class="v95-pillar-path">${path(d[1],cur,base)}</div></div>`;
    }).join('');
    const total=recent.map(overall).filter(v=>v!==null);
    const recentAvg=total.length?total.reduce((a,b)=>a+b,0)/total.length:null;
    box.innerHTML=`<p><strong>Mon bilan, pilier par pilier</strong></p><p>Chaque pilier raconte une partie différente de ton chemin. Certains avancent plus vite que d’autres : l’objectif n’est pas d’être parfait, mais de continuer à devenir progressivement la personne que tu veux être.</p><div class="v95-pillars">${cards}</div><div class="v95-encouragement"><p class="main">🌿 Accroche-toi. Le chemin peut être long, mais chaque pas compte.</p><p class="sub">Le bonheur n’est pas une récompense qui attend à l’arrivée : il se construit aussi dans la manière dont tu avances. Continue, même lentement. Les petits changements répétés finissent par transformer une vie.</p>${recentAvg!==null?`<p class="sub"><strong>Repère actuel :</strong> ${recentAvg.toFixed(1)}/10 sur les 7 dernières journées. Ce n’est qu’une photographie d’aujourd’hui, pas une définition de qui tu es.</p>`:''}</div>`;
  }
  function init(){render();setInterval(render,700)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(init,250));else setTimeout(init,250);
  window.addEventListener('load',()=>setTimeout(render,900));
})();
</script>
'''
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V95 four-pillar bilan applied')
