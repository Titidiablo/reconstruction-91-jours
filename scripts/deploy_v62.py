from pathlib import Path
import re

path = Path("index.html")
html = path.read_text(encoding="utf-8")

# V62: remove the redundant in-page save button; the floating save button
# remains the single save action and is already restricted to the program tab.
pattern = r'<button\b[^>]*onclick=["\']saveEntry\(\)["\'][^>]*>\s*💾\s*Sauvegarder ma journée\s*</button>'
count = len(re.findall(pattern, html, flags=re.IGNORECASE))
if count > 1:
    raise SystemExit(f'Expected at most one daily save button, found {count}')
if count == 1:
    html = re.sub(pattern, '', html, count=1, flags=re.IGNORECASE)

if '>V61</div>' not in html and '>V62</div>' not in html:
    raise SystemExit('V61/V62 badge not found')
if '>V61</div>' in html:
    html = html.replace('>V61</div>', '>V62</div>', 1)

marker = '<script id="v62-save-button-cleanup">'
if marker not in html:
    cleanup = '''<script id="v62-save-button-cleanup">
(function(){
  // V62: the floating save button is the only save control on the program tab.
  // Keep this marker explicit so the deployment validates the intended UI state.
  window.v62SaveButtonCleanup = true;
})();
</script>'''
    html = html.replace('</body>', cleanup + '\n</body>', 1)

checks = [
    '>V62</div>',
    'id="v61-dashboard-style"',
    'id="v61-dashboard-runtime"',
    'id="v61-save-visibility"',
    'id="v61Dashboard"',
    'id="dashboardNavButton"',
    'Progression depuis J1',
    'Dimension qui progresse le plus',
    'Dimension à surveiller',
    'syncV61SaveVisibility',
    'id="floatingSaveButton"',
    'id="v62-save-button-cleanup"',
]
for check in checks:
    if check not in html:
        raise SystemExit(f'Missing V62 content: {check}')
if re.search(r'Sauvegarder ma journée', html, flags=re.IGNORECASE):
    raise SystemExit('Redundant daily save button text still present')
if html.count('>V62</div>') != 1:
    raise SystemExit('V62 badge count invalid')
if html.count('id="v61-dashboard-runtime"') != 1:
    raise SystemExit('V61 dashboard runtime count invalid')
if html.count('id="v61-save-visibility"') != 1:
    raise SystemExit('V61 save visibility count invalid')
if html.count('id="v62-save-button-cleanup"') != 1:
    raise SystemExit('V62 cleanup marker count invalid')

path.write_text(html, encoding="utf-8")
print('V62 source prepared and validated')
