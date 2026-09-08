from pathlib import Path

path = Path("index.html")
html = path.read_text(encoding="utf-8")

# The application was restored to V62. The deploy script must not depend on
# a historical V59 badge that no longer exists in the source HTML.
# V61 dashboard enhancements are injected only when their markers are absent.

if ">V61</div>" not in html:
    # Accept the current V62 badge/version marker(s) without forcing an old
    # version string. The dashboard content checks below are the real guard.
    pass

css = r'''<style id="v61-dashboard-style">
.v61-dashboard{margin-top:0}
.v61-progress{height:10px;background:#e6e2db;border-radius:999px;overflow:hidden;margin-top:10px}
.v61-progress span{display:block;height:100%;width:0;background:#333;border-radius:999px;transition:width .25s ease}
.v61-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:14px}
.v61-stat{background:#f7f5f1;border:1px solid #ddd9d1;border-radius:12px;padding:14px}
.v61-label{display:block;color:#777;font-size:12px;margin-bottom:5px}
.v61-value{display:block;font-size:24px;font-weight:700;line-height:1.15}
.v61-note{display:block;color:#777;font-size:12px;margin-top:5px}
.v61-insights{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-top:12px}
.v61-insight{background:#fff;border:1px solid #e1ddd6;border-radius:12px;padding:14px}
.v61-insight h3{margin:0 0 6px;font-size:16px}
.v61-insight p{margin:0;color:#444}
.v61-day{display:flex;justify-content:space-between;align-items:center;border:1px solid #e1ddd6;border-radius:10px;padding:10px 12px;margin-top:8px;background:#fff}
.v61-badge{display:inline-block;padding:4px 8px;border-radius:999px;background:#eee9e3;font-size:12px;color:#555}
@media(max-width:700px){.v61-grid{grid-template-columns:1fr 1fr}.v61-insights{grid-template-columns:1fr}}
@media(max-width:480px){.v61-grid{grid-template-columns:1fr}}
</style>'''

js = r'''<script id="v61-dashboard-runtime">
(function(){
  const originalShowSection=window.showSection;
  let entries=[];
  const dims=[["presence","Présence"],["impulse_control","Maîtrise de l’impulsion"],["values_coherence","Cohérence avec mes valeurs"],["self_relation","Relation à moi-même"]];
  function score(v){const n=Number(v);return Number.isFinite(n)&&n>=1&&n<=10?n:null;}
  function avg(r){const v=dims.map(x=>score(r&&r[x[0]])).filter(x=>x!==null);return v.length?v.reduce((a,b)=>a+b,0)/v.length:null;}
  function rows(){return entries.filter(r=>Number.isFinite(Number(r.day_number))).sort((a,b)=>Number(a.day_number)-Number(b.day_number));}
  function make(){
    const app=document.getElementById("app");if(!app||document.getElementById("v61Dashboard"))return;
    const top=app.querySelector(".topbar");if(!top)return;
    const nav=top.querySelector(".nav-buttons");
    if(nav&&!document.getElementById("dashboardNavButton")){
      const b=document.createElement("button");b.id="dashboardNavButton";b.className="secondary";b.type="button";b.textContent="🏠 Tableau de bord";b.onclick=()=>window.showSection("dashboard");nav.insertBefore(b,nav.firstChild);
    }
    const sec=document.createElement("div");sec.id="v61Dashboard";sec.className="hidden v61-dashboard";
    sec.innerHTML='<div class="card"><h2 class="section-title">🏠 Mon tableau de bord</h2><p id="v61Welcome">Ton parcours en un coup d’œil.</p><div class="v61-progress"><span id="v61Bar"></span></div><div class="v61-grid"><div class="v61-stat"><span class="v61-label">Progression</span><strong id="v61Progress" class="v61-value">—</strong><span class="v61-note">jours du programme</span></div><div class="v61-stat"><span class="v61-label">Score global</span><strong id="v61Score" class="v61-value">—</strong><span id="v61ScoreNote" class="v61-note">sur 10</span></div><div class="v61-stat"><span class="v61-label">Streak</span><strong id="v61Streak" class="v61-value">—</strong><span class="v61-note">jours consécutifs</span></div><div class="v61-stat"><span class="v61-label">Dernière journée notée</span><strong id="v61Last" class="v61-value">—</strong><span class="v61-note">avec un score</span></div></div></div><div class="card"><h2 class="section-title">🧠 Analyse de mon évolution</h2><div class="v61-insights"><div class="v61-insight"><h3>📈 Progression depuis J1</h3><p id="v61Delta">—</p></div><div class="v61-insight"><h3>💪 Dimension qui progresse le plus</h3><p id="v61Strong">—</p></div><div class="v61-insight"><h3>🎯 Dimension à surveiller</h3><p id="v61Weak">—</p></div><div class="v61-insight"><h3>🔎 Lecture récente</h3><p id="v61Recent">—</p></div></div></div><div class="card"><h2 class="section-title">🗓️ Mes dernières journées</h2><div id="v61RecentList"></div></div>';
    top.insertAdjacentElement("afterend",sec);
  }
  async function load(){
    try{
      const client=typeof getSupabaseClient==="function"?getSupabaseClient():null;
      if(!client)return;
      const {data:{user}}=await client.auth.getUser();
      if(!user)return;
      const r=await client.from("daily_entries").select("day_number,presence,impulse_control,values_coherence,self_relation").eq("user_id",user.id).order("day_number",{ascending:true});
      if(!r.error)entries=r.data||[];
    }catch(e){console.warn("V61 dashboard",e)}
    render();
  }
  function render(){
    make();
    const box=document.getElementById("v61Dashboard");if(!box)return;
    const rs=rows(),scored=rs.filter(r=>avg(r)!==null),first=scored[0],last=scored[scored.length-1];
    const current=(typeof currentDay!=="undefined"?Number(currentDay):1)||1;
    const progress=last?Number(last.day_number):current;
    const clamp=Math.min(91,Math.max(0,progress));
    document.getElementById("v61Progress").textContent=clamp+"/91";
    document.getElementById("v61Bar").style.width=(clamp/91*100)+"%";
    document.getElementById("v61Score").textContent=last?avg(last).toFixed(1)+"/10":"—";
    document.getElementById("v61ScoreNote").textContent=last?"J"+last.day_number:"aucun score enregistré";
    document.getElementById("v61Last").textContent=last?"J"+last.day_number:"—";
    const days=new Set(rs.map(r=>Number(r.day_number)));let latest=0;days.forEach(d=>{if(d>latest)latest=d});
    let streak=0;for(let d=latest;latest&&days.has(d);d--)streak++;
    document.getElementById("v61Streak").textContent=streak;
    document.getElementById("v61Welcome").textContent="Jour "+current+" — observe avant de juger, et garde le cap.";
    if(first&&last){const d=avg(last)-avg(first);document.getElementById("v61Delta").textContent=(d>=0?"+":"")+d.toFixed(1)+" point entre J"+first.day_number+" et J"+last.day_number+"."}
    else document.getElementById("v61Delta").textContent="Il faut au moins deux journées notées pour mesurer une progression.";
    const changes=dims.map(([k,l])=>{const x=scored.filter(r=>score(r[k])!==null);return x.length?{l,d:score(x[x.length-1][k])-score(x[0][k])}:null}).filter(Boolean).sort((a,b)=>b.d-a.d);
    document.getElementById("v61Strong").textContent=changes[0]?changes[0].l+" ("+(changes[0].d>=0?"+":"")+changes[0].d.toFixed(1)+")":"—";
    const recent=scored.slice(-7);
    const weak=dims.map(([k,l])=>{const v=recent.map(r=>score(r[k])).filter(x=>x!==null);return v.length?{l,a:v.reduce((a,b)=>a+b,0)/v.length}:null}).filter(Boolean).sort((a,b)=>a.a-b.a);
    document.getElementById("v61Weak").textContent=weak[0]?weak[0].l+" · "+weak[0].a.toFixed(1)+"/10 sur les 7 dernières journées":"—";
    document.getElementById("v61Recent").textContent=recent.length?"Moyenne des 7 dernières journées : "+(recent.reduce((a,r)=>a+avg(r),0)/recent.length).toFixed(1)+"/10.":"Continue à renseigner tes journées : l’analyse se précisera.";
    document.getElementById("v61RecentList").innerHTML=rs.slice(-5).reverse().map(r=>'<div class="v61-day"><span class="v61-badge">J'+r.day_number+'</span><strong>'+(avg(r)!==null?avg(r).toFixed(1)+"/10":"sans score")+'</strong></div>').join("")||"<p>Aucune journée sauvegardée pour le moment.</p>";
  }
  window.showSection=function(section){make();if(section==="dashboard"){["programSection","journalSection","evolutionSection"].forEach(id=>document.getElementById(id)?.classList.add("hidden"));document.querySelectorAll(".nav-buttons button").forEach(b=>b.classList.remove("nav-active"));document.getElementById("v61Dashboard")?.classList.remove("hidden");document.getElementById("dashboardNavButton")?.classList.add("nav-active");load();return;}document.getElementById("v61Dashboard")?.classList.add("hidden");document.getElementById("dashboardNavButton")?.classList.remove("nav-active");if(typeof originalShowSection==="function")originalShowSection(section);};
  window.addEventListener("load",()=>setTimeout(()=>{make();load();},700));
})();
</script>'''

save_visibility = r'''<script id="v61-save-visibility">
(function(){
  function syncV61SaveVisibility(){
    const program=document.getElementById("programSection");
    const visible=!!program && !program.classList.contains("hidden");
    document.querySelectorAll('button[onclick="saveEntry()"], #floatingSaveButton').forEach(btn=>{
      btn.classList.toggle("hidden",!visible);
    });
  }
  const previousShowSection=window.showSection;
  window.showSection=function(){
    const result=typeof previousShowSection==="function"?previousShowSection.apply(this,arguments):undefined;
    setTimeout(syncV61SaveVisibility,0);
    return result;
  };
  window.addEventListener("load",()=>setTimeout(syncV61SaveVisibility,750));
  const program=document.getElementById("programSection");
  if(program)new MutationObserver(syncV61SaveVisibility).observe(program,{attributes:true,attributeFilter:["class"]});
})();
</script>'''

if 'id="v61-dashboard-style"' not in html:
    html = html.replace('</head>', css + "\n</head>", 1)
if 'id="v61-dashboard-runtime"' not in html:
    html = html.replace('</body>', js + "\n</body>", 1)
if 'id="v61-save-visibility"' not in html:
    html = html.replace('</body>', save_visibility + "\n</body>", 1)

checks = [
    'id="v61-dashboard-style"',
    'id="v61-dashboard-runtime"',
    'id="v61-save-visibility"',
    'id="v61Dashboard"',
    'id="dashboardNavButton"',
    "Progression depuis J1",
    "Dimension qui progresse le plus",
    "Dimension à surveiller",
    "syncV61SaveVisibility",
]
for check in checks:
    if check not in html:
        raise SystemExit(f"Missing V61 content: {check}")
if html.count('id="v61-dashboard-runtime"') != 1:
    raise SystemExit("V61 runtime count invalid")
if html.count('id="v61-save-visibility"') != 1:
    raise SystemExit("V61 save visibility count invalid")

path.write_text(html, encoding="utf-8")
print("V61 source prepared and validated")
