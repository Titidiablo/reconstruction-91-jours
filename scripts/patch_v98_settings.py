from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove a previous V98 patch if the workflow is re-run.
s = re.sub(r'\n<style id="v98-settings">.*?</style>\s*<script id="v98-settings">.*?</script>\s*', '\n', s, flags=re.S)

patch = r'''
<style id="v98-settings">
.v98-settings-panel{max-width:900px;margin:0 auto}
.v98-settings-intro{margin:0 0 18px;color:#666}
.v98-settings-group{background:#fff;border:1px solid #ddd8cf;border-radius:16px;padding:18px;margin-bottom:16px;box-shadow:0 2px 10px rgba(0,0,0,.04)}
.v98-settings-group h3{margin:0 0 5px;font-size:18px}
.v98-settings-group>p{margin:0 0 14px;color:#666;font-size:14px}
.v98-setting-row{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:13px 0;border-top:1px solid #eee9e1}
.v98-setting-row:first-of-type{border-top:0}
.v98-setting-label{display:flex;align-items:center;gap:10px;font-weight:700}
.v98-setting-help{display:block;font-size:12px;font-weight:400;color:#777;margin-top:2px}
.v98-switch{position:relative;width:48px;height:28px;flex:0 0 48px}
.v98-switch input{opacity:0;width:0;height:0;position:absolute}
.v98-slider{position:absolute;inset:0;background:#d8d4cc;border-radius:30px;cursor:pointer;transition:.18s}
.v98-slider:before{content:"";position:absolute;width:22px;height:22px;left:3px;top:3px;background:#fff;border-radius:50%;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:.18s}
.v98-switch input:checked+.v98-slider{background:#222}
.v98-switch input:checked+.v98-slider:before{transform:translateX(20px)}
.v98-disabled{opacity:.55}
.v98-back{margin-bottom:14px}
@media(max-width:600px){.v98-settings-group{padding:14px}.v98-setting-row{align-items:flex-start}.v98-setting-label{line-height:1.35}}
</style>
<script id="v98-settings">
(function(){
  const KEY='devenir-soi-settings-v1';
  const defaults={meditation:true,breathing:true,sleep:true,development:true,motivation:true};
  function getSettings(){
    try{return {...defaults,...JSON.parse(localStorage.getItem(KEY)||'{}')}}catch(e){return {...defaults}}
  }
  function saveSettings(settings){localStorage.setItem(KEY,JSON.stringify(settings));}
  window.getDevenirSoiSettings=getSettings;
  window.showSettings=function(){
    const ids=['programSection','journalSection','evolutionSection','v61Dashboard','v64Dashboard','v63Resources'];
    ids.forEach(id=>{const el=document.getElementById(id);if(el)el.classList.add('hidden')});
    const panel=document.getElementById('v98SettingsPanel');
    if(!panel)return;
    panel.classList.remove('hidden');
    document.querySelectorAll('.nav-buttons button').forEach(b=>b.classList.remove('nav-active'));
    const btn=document.getElementById('settingsNavButton');
    if(btn)btn.classList.add('nav-active');
    renderSettings();
    window.scrollTo({top:0,behavior:'smooth'});
  };
  function renderSettings(){
    const panel=document.getElementById('v98SettingsPanel'); if(!panel)return;
    const st=getSettings();
    panel.querySelectorAll('input[data-module]').forEach(input=>{input.checked=!!st[input.dataset.module]});
  }
  function toggleModule(key,value){const st=getSettings();st[key]=!!value;saveSettings(st);}
  function install(){
    if(!document.getElementById('settingsNavButton')){
      const nav=document.querySelector('.nav-buttons');
      if(nav){
        const b=document.createElement('button');
        b.id='settingsNavButton'; b.type='button'; b.textContent='⚙️ Paramètres';
        b.addEventListener('click',window.showSettings);
        nav.appendChild(b);
      }
    }
    if(!document.getElementById('v98SettingsPanel')){
      const panel=document.createElement('section');
      panel.id='v98SettingsPanel'; panel.className='hidden v98-settings-panel';
      panel.innerHTML=`
        <div class="v98-back"><button type="button" class="secondary" id="v98BackToday">← Retour à Aujourd'hui</button></div>
        <div class="card">
          <h2>⚙️ Paramètres</h2>
          <p class="v98-settings-intro">Personnalise ton expérience et choisis ce que tu veux retrouver sur ta page Aujourd'hui.</p>
        </div>
        <div class="v98-settings-group">
          <h3>🧰 Mes modules</h3>
          <p>Active ou désactive les modules complémentaires. Ton choix est mémorisé sur cet appareil.</p>
          ${row('meditation','🧘','Méditation','Pratiques de présence et de pleine conscience')}
          ${row('breathing','🌿','Respiration / relaxation','Calme, détente et retour à l'équilibre')}
          ${row('sleep','😴','Sommeil','Routines et exercices pour mieux récupérer')}
          ${row('development','🧠','Développement personnel','Réflexion, compréhension de soi et évolution')}
          ${row('motivation','💪','Motivation','Passage à l'action, discipline et petits défis')}
        </div>
        <div class="v98-settings-group">
          <h3>🎨 Apparence</h3>
          <p>Les options d'apparence pourront être personnalisées ici.</p>
          <div class="v98-setting-row v98-disabled"><span>Mode sombre / clair</span><span>À venir</span></div>
        </div>
        <div class="v98-settings-group">
          <h3>🔔 Rappels</h3>
          <p>Les rappels quotidiens pourront être configurés ici.</p>
          <div class="v98-setting-row v98-disabled"><span>Rappels du parcours</span><span>À venir</span></div>
        </div>
        <div class="v98-settings-group">
          <h3>📅 Mon parcours</h3>
          <p>Gestion du jour courant et des options du parcours 91 jours.</p>
          <div class="v98-setting-row v98-disabled"><span>Gestion avancée du parcours</span><span>À venir</span></div>
        </div>
        <div class="v98-settings-group">
          <h3>💾 Mes données</h3>
          <p>Les fonctions de sauvegarde et d'export seront regroupées ici.</p>
          <div class="v98-setting-row v98-disabled"><span>Export / import</span><span>À venir</span></div>
        </div>
        <div class="v98-settings-group">
          <h3>ℹ️ À propos</h3>
          <p><strong>DEVENIR SOI</strong> — Parcours de transformation personnelle sur 91 jours.</p>
        </div>`;
      document.body.appendChild(panel);
      panel.querySelectorAll('input[data-module]').forEach(input=>input.addEventListener('change',()=>toggleModule(input.dataset.module,input.checked)));
      document.getElementById('v98BackToday')?.addEventListener('click',()=>{
        panel.classList.add('hidden');
        if(typeof window.showToday==='function') window.showToday();
        else document.getElementById('todayNavButton')?.click();
      });
    }
    renderSettings();
  }
  function row(key,emoji,title,help){return `<div class="v98-setting-row"><div class="v98-setting-label"><span>${emoji}</span><span>${title}<span class="v98-setting-help">${help}</span></span></div><label class="v98-switch"><input type="checkbox" data-module="${key}"><span class="v98-slider"></span></label></div>`}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
  window.addEventListener('load',()=>setTimeout(install,500));
})();
</script>
'''
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V98 settings menu applied')
