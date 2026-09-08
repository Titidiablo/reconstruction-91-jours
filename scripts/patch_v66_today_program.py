from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'id="v66-today-program-fix"' not in s:
    patch = r'''
<style id="v66-today-program-fix">
/* V66 — Programme : conserver la navigation actuelle, retirer les éléments UX parasites. */
.v64-stepper { display: none !important; }
.v64-save-main {
  position: static !important;
  bottom: auto !important;
  z-index: auto !important;
  margin: 20px 0 !important;
}
</style>
<script id="v66-today-program-fix">
(function(){
  function cleanupProgram(){
    // Le stepper V64 (Comprendre / Pratiquer / Méditer / Écrire / Évaluer)
    // n'est pas une étape de navigation : il encombre le contenu du Programme.
    document.querySelectorAll('.v64-stepper').forEach(el => el.remove());

    // Il ne doit rester qu'un seul bouton de sauvegarde : celui du bandeau V64.
    document.querySelectorAll('button[onclick="saveEntry()"], button[onclick*=\"saveEntry()\"]').forEach(btn => {
      if (!btn.closest('.v64-save-main')) btn.remove();
    });

    // Le bouton de sauvegarde reste dans le flux de la page, juste avant la navigation.
    const program = document.getElementById('programSection');
    const save = document.querySelector('.v64-save-main');
    if (program && save && save.parentElement !== program) program.appendChild(save);
  }

  function observe(){
    cleanupProgram();
    const root = document.getElementById('programSection');
    if (!root || root.dataset.v66Observed) return;
    root.dataset.v66Observed = '1';
    new MutationObserver(cleanupProgram).observe(root, {childList:true, subtree:true});
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', observe);
  else observe();
  window.addEventListener('load', observe);
})();
</script>
'''
    s = s.replace('</head>', patch + '</head>', 1)

p.write_text(s, encoding='utf-8')
print('V66 program cleanup applied')
