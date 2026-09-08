from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v64-ux-style"' not in s:
    css = r'''
<style id="v64-ux-style">
/* V64 — DEVENIR SOI : refonte UX complète */
body{max-width:1180px;padding:18px;background:#f3f1ec}
.app-brand{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin:0 0 18px}
.app-brand h1{margin:0;font-size:30px;letter-spacing:.02em}.app-brand .subtitle{margin:4px 0 0}
.v64-dashboard{margin-bottom:18px}.v64-hero{background:#fff;border:1px solid #ddd8cf;border-radius:18px;padding:22px;box-shadow:0 4px 18px rgba(0,0,0,.06)}
.v64-kicker{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:#777;font-weight:700}.v64-hero h2{margin:5px 0 4px;font-size:28px}.v64-hero p{margin:0;color:#555}.v64-progress-row{display:flex;justify-content:space-between;gap:12px;margin-top:18px;font-size:13px;font-weight:700}.v64-progress{height:12px;background:#e5e1da;border-radius:999px;overflow:hidden;margin-top:7px}.v64-progress span{display:block;height:100%;background:#222;border-radius:999px;transition:width .25s ease}
.v64-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.v64-actions button{margin:0}
.v64-dashboard-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:12px}.v64-stat{background:#fff;border:1px solid #ddd8cf;border-radius:14px;padding:15px}.v64-stat small{display:block;color:#777;font-weight:600}.v64-stat strong{display:block;font-size:23px;margin-top:3px}.v64-stat span{display:block;color:#777;font-size:12px;margin-top:3px}
.v64-days-card{background:#fff;border:1px solid #ddd8cf;border-radius:18px;padding:20px;margin-top:12px}.v64-days-head{display:flex;justify-content:space-between;align-items:center;gap:10px}.v64-days-head h3{margin:0}.v64-days-grid{display:grid;grid-template-columns:repeat(13,minmax(34px,1fr));gap:6px;margin-top:14px}.v64-day-btn{margin:0!important;padding:8px 4px!important;background:#f0eee9;color:#333;border:1px solid #d8d3ca;font-size:12px;font-weight:700}.v64-day-btn.current{background:#222;color:#fff;border-color:#222}.v64-day-btn.done{box-shadow:inset 0 -3px 0 #26733d}.v64-day-btn.done::after{content:' ✓';color:#26733d}.v64-day-btn.current.done::after{color:#fff}.v64-day-modal{position:fixed;inset:0;z-index:99998;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;padding:16px}.v64-day-modal.hidden{display:none}.v64-day-dialog{background:#fff;border-radius:18px;width:min(900px,100%);max-height:90vh;overflow:auto;padding:20px}.v64-stepper{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;margin:16px 0}.v64-step{padding:9px 7px;border-radius:10px;background:#eeeae3;text-align:center;font-size:12px;font-weight:700;color:#666}.v64-step.active{background:#222;color:#fff}.v64-step.done{background:#dfeee3;color:#26733d}
.v64-section-head{display:flex;align-items:center;justify-content:space-between;gap:10px}.v64-section-head h2{margin-bottom:4px}.v64-completion{font-weight:700;font-size:13px;color:#555}.v64-save-main{display:flex;align-items:center;justify-content:space-between;gap:14px;background:#fff;border:2px solid #222;border-radius:14px;padding:13px 15px;margin-top:14px;position:sticky;bottom:78px;z-index:50;box-shadow:0 8px 22px rgba(0,0,0,.12)}.v64-save-main button{margin:0;font-size:16px;font-weight:800;padding:13px 20px}.v64-save-main.dirty{border-color:#8a5a00;background:#fffaf0}.v64-save-hint{font-size:12px;color:#666}.v64-score-card{min-height:100%}.v64-score-question{font-size:12px;line-height:1.4;color:#555;margin:2px 0 8px}.v64-score-anchor{font-size:11px;color:#777;line-height:1.35;margin-bottom:8px}.v64-score-anchor strong{color:#333}.score-item select{font-size:16px;font-weight:700;min-height:46px}.score-item{padding:14px!important}
.control-table{min-width:760px}.control-table th{font-size:13px}.control-table th:nth-child(1){background:#e7f2e9}.control-table th:nth-child(2){background:#f6f0dc}.control-table th:nth-child(3){background:#f3e4e2}.control-table td{background:#fff}.control-table textarea{min-height:72px}.v64-control-help{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0 4px}.v64-control-help div{padding:9px;border-radius:9px;font-size:12px;color:#555}.v64-control-help .c1{background:#eaf4ec}.v64-control-help .c2{background:#faf4df}.v64-control-help .c3{background:#f8e9e7}
.v64-evolution-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}.v64-evo-stat{padding:12px;border:1px solid #ddd8cf;border-radius:12px;background:#faf9f6}.v64-evo-stat small{display:block;color:#777}.v64-evo-stat strong{font-size:20px}.v64-empty{padding:18px;text-align:center;color:#777}
@media(max-width:800px){.v64-dashboard-grid{grid-template-columns:1fr 1fr}.v64-days-grid{grid-template-columns:repeat(7,minmax(34px,1fr))}.v64-evolution-summary{grid-template-columns:1fr 1fr}.v64-control-help{grid-template-columns:1fr}.v64-save-main{bottom:64px}}
@media(max-width:520px){body{padding:10px}.app-brand h1{font-size:24px}.v64-dashboard-grid{grid-template-columns:1fr 1fr}.v64-days-grid{grid-template-columns:repeat(7,1fr);gap:4px}.v64-day-btn{font-size:11px;padding:7px 2px!important}.v64-stepper{grid-template-columns:1fr 1fr}.v64-step:last-child{grid-column:1/-1}.v64-save-main{flex-direction:column;align-items:stretch}.v64-save-main button{width:100%}.score-grid{grid-template-columns:1fr!important}.day-navigation{position:sticky;bottom:0;background:#f3f1ec;padding:8px 0;z-index:40}}
</style>
'''
    s = s.replace('</head>', css + '</head>', 1)

if 'id="v64-ux-runtime"' not in s:
    js = r'''
<script id="v64-ux-runtime">
(function(){
  const V='V64';
  const $=id=>document.getElementById(id);
  const client=()=>typeof getSupabaseClient==='function'?getSupabaseClient():null;
  let entries=[];
  function addTopBrand(){
    const h=document.querySelector('body > h1');
    if(h && !h.parentElement.classList.contains('app-brand')){
      const wrap=document.createElement('div');wrap.className='app-brand';
      const sub=document.querySelector('body > .subtitle');
      h.parentNode.insertBefore(wrap,h);wrap.appendChild(h);if(sub)wrap.appendChild(sub);
    }
    if(h)h.textContent='DEVENIR SOI';
    document.title='DEVENIR SOI — 91 jours';
  }
  function navButton(){
    const nav=document.querySelector('#app .nav-buttons');if(!nav)return;
    if(!$('todayNavButton')){const b=document.createElement('button');b.id='todayNavButton';b.className='secondary';b.type='button';b.textContent="🏠 Aujourd’hui";b.onclick=()=>showToday();nav.insertBefore(b,nav.firstChild)}
    if(!$('daysNavButton')){const b=document.createElement('button');b.id='daysNavButton';b.className='secondary';b.type='button';b.textContent='🗓️ 91 jours';b.onclick=()=>openDays();nav.insertBefore(b,nav.children[1]||null)}
  }
  function dashboard(){
    if($('v64Dashboard'))return;
    const app=$('app'),top=app?.querySelector('.topbar');if(!top)return;
    const sec=document.createElement('section');sec.id='v64Dashboard';sec.className='hidden v64-dashboard';
    sec.innerHTML=`<div class="v64-hero"><div class="v64-kicker">Ton parcours · 91 jours</div><h2 id="v64TodayTitle">Aujourd’hui</h2><p id="v64TodayText">Un pas concret, puis un autre.</p><div class="v64-progress-row"><span id="v64ProgressLabel">Progression du parcours</span><span id="v64ProgressValue">0 %</span></div><div class="v64-progress"><span id="v64ProgressBar"></span></div><div class="v64-actions"><button class="primary" type="button" id="v64Continue">▶ Continuer ma journée</button><button class="secondary" type="button" id="v64OpenDays">🗓️ Voir les 91 jours</button></div></div><div class="v64-dashboard-grid"><div class="v64-stat"><small>Jours réalisés</small><strong id="v64Done">0/91</strong><span>journées sauvegardées</span></div><div class="v64-stat"><small>Score du jour</small><strong id="v64TodayScore">—</strong><span id="v64TodayScoreNote">pas encore évalué</span></div><div class="v64-stat"><small>Série</small><strong id="v64Streak">0</strong><span>jours consécutifs</span></div><div class="v64-stat"><small>Dernier jour</small><strong id="v64LastDay">—</strong><span>du parcours</span></div></div><div class="v64-days-card"><div class="v64-days-head"><h3>🗓️ Mon parcours</h3><button class="secondary" type="button" id="v64CompactDays">Ouvrir la grille</button></div><div id="v64MiniDays" class="v64-days-grid"></div></div>`;
    top.insertAdjacentElement('afterend',sec);
    $('v64Continue').onclick=()=>{showSection('program');loadDay(currentDay)};$('v64OpenDays').onclick=openDays;$('v64CompactDays').onclick=openDays;
  }
  function daySet(){return new Set(entries.map(r=>Number(r.day_number)).filter(n=>n>=1&&n<=91))}
  function scoreAvg(r){const vals=[r?.presence,r?.impulse_control,r?.values_coherence,r?.self_relation].map(Number).filter(n=>n>=1&&n<=10);return vals.length?vals.reduce((a,b)=>a+b,0)/vals.length:null}
  function renderDays(container,mini){
    if(!container)return;const done=daySet();container.innerHTML='';
    for(let d=1;d<=91;d++){const b=document.createElement('button');b.type='button';b.className='v64-day-btn'+(d===Number(currentDay)?' current':'')+(done.has(d)?' done':'');b.textContent='J'+d;b.title=done.has(d)?'Jour réalisé':'Jour non réalisé';b.onclick=()=>{closeDays();showSection('program');requestDayChange(d)};container.appendChild(b)}
  }
  function openDays(){
    let m=$('v64DayModal');if(!m){m=document.createElement('div');m.id='v64DayModal';m.className='v64-day-modal hidden';m.innerHTML='<div class="v64-day-dialog"><div class="v64-days-head"><h2>🗓️ Les 91 jours</h2><button type="button" class="secondary" id="v64CloseDays">✕ Fermer</button></div><p>✓ = journée déjà sauvegardée. Le jour courant est encadré.</p><div id="v64AllDays" class="v64-days-grid"></div></div>';document.body.appendChild(m);$('v64CloseDays').onclick=closeDays;m.addEventListener('click',e=>{if(e.target===m)closeDays()})}renderDays($('v64AllDays'));m.classList.remove('hidden')}
  function closeDays(){$('v64DayModal')?.classList.add('hidden')}
  function loadEntries(){const c=client();if(!c)return Promise.resolve();return c.auth.getUser().then(({data:{user}})=>{if(!user)return;return c.from('daily_entries').select('day_number,presence,impulse_control,values_coherence,self_relation').eq('user_id',user.id).order('day_number',{ascending:true}).then(r=>{if(!r.error)entries=r.data||[]})}).then(()=>{renderDashboard();renderDays($('v64MiniDays'),true)}).catch(e=>console.warn('V64 dashboard',e))}
  function renderDashboard(){
    dashboard();const done=daySet(),sorted=[...entries].sort((a,b)=>Number(a.day_number)-Number(b.day_number));const last=sorted[sorted.length-1];const today=sorted.find(r=>Number(r.day_number)===Number(currentDay));const avg=scoreAvg(today);const n=done.size;
    $('v64TodayTitle').textContent='Aujourd’hui · Jour '+currentDay;
    $('v64TodayText').textContent=last?'Continue là où tu t’es arrêté.':'Commence par le Jour 1 : observer, pratiquer, écrire, évaluer.';
    $('v64Done').textContent=n+'/91';$('v64LastDay').textContent=last?'J'+last.day_number:'—';$('v64TodayScore').textContent=avg!==null?avg.toFixed(1)+'/10':'—';$('v64TodayScoreNote').textContent=avg!==null?'moyenne des 4 scores':'pas encore évalué';
    $('v64ProgressValue').textContent=Math.round(n/91*100)+' %';$('v64ProgressBar').style.width=(n/91*100)+'%';
    let streak=0;for(let d=last?Number(last.day_number):0;d>0&&done.has(d);d--)streak++;$('v64Streak').textContent=streak;
  }
  function showToday(){closeDays();['programSection','journalSection','evolutionSection','v61Dashboard','v63Resources'].forEach(id=>$(id)?.classList.add('hidden'));dashboard();$('v64Dashboard').classList.remove('hidden');document.querySelectorAll('.nav-buttons button').forEach(b=>b.classList.remove('nav-active'));$('todayNavButton')?.classList.add('nav-active');loadEntries()}
  function steps(){
    const card=document.querySelector('.exercise-card');if(!card||$('v64Stepper'))return;const s=document.createElement('div');s.id='v64Stepper';s.className='v64-stepper';s.innerHTML='<div class="v64-step">1 · Comprendre</div><div class="v64-step">2 · Pratiquer</div><div class="v64-step">3 · Méditer</div><div class="v64-step">4 · Écrire</div><div class="v64-step">5 · Évaluer</div>';card.insertBefore(s,card.firstChild)
  }
  function completion(){
    const fields=['meditationNotes','learning','reaction','presenceScore','impulseScore','valuesScore','selfRelationScore'];let done=0;fields.forEach(id=>{const e=$(id);if(e&&(String(e.value||'').trim()))done++});if($('controlTableBody')&&[...$('controlTableBody').querySelectorAll('textarea')].some(x=>x.value.trim()))done++;const pct=Math.round(done/fields.length*100);let box=$('v64Completion');if(!box){const host=document.querySelector('.journal-header');if(!host)return;box=document.createElement('div');box.id='v64Completion';box.className='v64-completion';host.appendChild(box)}box.textContent='Journée : '+Math.min(100,pct)+'% complétée';
    const st=[...document.querySelectorAll('.v64-step')];const n=pct<20?0:pct<40?1:pct<60?2:pct<85?3:4;st.forEach((x,i)=>x.classList.toggle('active',i===n));
  }
  function enhanceSave(){
    const btn=document.querySelector('button[onclick="saveEntry()"]');const host=btn?.parentElement;if(!btn||!host||$('v64SaveMain'))return;const wrap=document.createElement('div');wrap.id='v64SaveMain';wrap.className='v64-save-main';wrap.innerHTML='<div><strong>💾 Sauvegarder ma journée</strong><div class="v64-save-hint">Tes réponses et tes scores sont enregistrés dans ton espace personnel.</div></div><button type="button" class="primary">💾 Sauvegarder maintenant</button>';const newBtn=wrap.querySelector('button');newBtn.onclick=()=>window.saveEntry();btn.remove();host.appendChild(wrap);['input','change'].forEach(ev=>document.addEventListener(ev,()=>{completion();wrap.classList.toggle('dirty',true)},true));const oldSave=window.saveEntry;window.saveEntry=async function(){const r=await oldSave.apply(this,arguments);if(r){wrap.classList.remove('dirty');loadEntries()}return r}}
  function enhanceControl(){
    const table=document.querySelector('.control-table');if(!table||$('v64ControlHelp'))return;const h=document.createElement('div');h.id='v64ControlHelp';h.className='v64-control-help';h.innerHTML='<div class="c1"><strong>🟢 Sous mon contrôle</strong><br>Ce que je peux décider ou faire moi-même.</div><div class="c2"><strong>🟡 Influence partielle</strong><br>Ce que je peux influencer sans garantir le résultat.</div><div class="c3"><strong>🔴 Hors de mon contrôle</strong><br>Ce qui dépend des autres, du passé ou des circonstances.</div>';table.parentElement.insertBefore(h,table)
  }
  function enhanceScores(){
    const data={presenceScore:['Qu’ai-je réellement observé et vécu avec attention aujourd’hui ?','1/10 : pilote automatique.','10/10 : attention pleinement présente.'],impulseScore:['Ai-je choisi ma réponse plutôt que de suivre une impulsion ?','1/10 : réaction presque automatique.','10/10 : réponse choisie consciemment.'],valuesScore:['Mes actes étaient-ils alignés avec mes valeurs ?','1/10 : forte contradiction avec mes valeurs.','10/10 : cohérence pleine avec mes valeurs.'],selfRelationScore:['Comment me suis-je traité aujourd’hui ?','1/10 : jugement ou dévalorisation.','10/10 : respect, lucidité et bienveillance.']};Object.entries(data).forEach(([id,a])=>{const e=$(id),item=e?.closest('.score-item');if(!item||item.querySelector('.v64-score-question'))return;const p=document.createElement('div');p.className='v64-score-question';p.textContent=a[0];const x=document.createElement('div');x.className='v64-score-anchor';x.innerHTML='<strong>'+a[1]+'</strong><br>'+a[2];item.insertBefore(p,e);item.insertBefore(x,e)})
  }
  function persistControlExtras(){
    const oldBuild=window.buildExerciseResponse;if(typeof oldBuild!=='function')return;if(window.v64BuildWrapped)return;window.v64BuildWrapped=true;window.buildExerciseResponse=function(){let raw=oldBuild.apply(this,arguments);const a=$('controlActionResponse')?.value?.trim()||'',o=$('controlObservationResponse')?.value?.trim()||'';if(a)raw+='\nACTIONS CONCRÈTES\n'+a;if(o)raw+='\nTRACE DU TABLEAU\n'+o;return raw};const oldRestore=window.restoreInlineResponses;if(typeof oldRestore==='function'){window.restoreInlineResponses=function(data){oldRestore.apply(this,arguments);const raw=String(data?.exercise_response||'');const get=n=>{const m=raw.match(new RegExp('(?:^|\\n)'+n+'\\n([\\s\\S]*?)(?=\\n(?:ACTIONS CONCRÈTES|TRACE DU TABLEAU|DÉCISION SANS VALIDATION|BILAN DE SEMAINE — SCORES)\\n|$)','i'));return m?m[1].trim():''};if($('controlActionResponse'))$('controlActionResponse').value=get('ACTIONS CONCRÈTES');if($('controlObservationResponse'))$('controlObservationResponse').value=get('TRACE DU TABLEAU')}}}
  function init(){addTopBrand();navButton();dashboard();steps();enhanceSave();enhanceControl();enhanceScores();persistControlExtras();completion();loadEntries()}
  window.addEventListener('load',()=>setTimeout(init,900));
  document.addEventListener('input',()=>setTimeout(completion,20),true);document.addEventListener('change',()=>setTimeout(completion,20),true);
})();
</script>
'''
    s = s.replace('</body>', js + '</body>', 1)

# Normalize version marker and remove duplicate legacy cleanup markers.
s = s.replace('<div class="app-version-v18">V64</div>', '<div class="app-version-v18">V64</div>')
while s.count('<script id="v62-save-button-cleanup">') > 1:
    pos=s.rfind('<script id="v62-save-button-cleanup">')
    end=s.find('</script>',pos)
    if end>=0:s=s[:pos]+s[end+9:]

p.write_text(s,encoding='utf-8')
print('V64 UX applied')
