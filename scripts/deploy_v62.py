from pathlib import Path
import re

path = Path("index.html")
html = path.read_text(encoding="utf-8")

# V62: one save control only. The existing floating save button remains;
# remove the redundant in-page button if it exists.
html, removed = re.subn(
    r'<button\b[^>]*>[^<]*Sauvegarder ma journée[^<]*</button>',
    '',
    html,
    count=1,
    flags=re.IGNORECASE,
)

# Increment the visible application version exactly once.
if '>V62</div>' not in html:
    version_matches = re.findall(r'>V\d+</div>', html)
    if not version_matches:
        raise SystemExit('Application version badge not found')
    html = re.sub(r'>V\d+</div>', '>V62</div>', html, count=1)

marker = '<script id="v62-save-button-cleanup">'
if marker not in html:
    cleanup = '''<script id="v62-save-button-cleanup">
(function(){
  window.v62SaveButtonCleanup = true;
})();
</script>'''
    if '</body>' not in html:
        raise SystemExit('Closing body tag not found')
    html = html.replace('</body>', cleanup + '\n</body>', 1)

# Required V62 invariants.
checks = [
    '>V62</div>',
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
if html.count('id="v62-save-button-cleanup"') != 1:
    raise SystemExit('V62 cleanup marker count invalid')

path.write_text(html, encoding='utf-8')
print(f'V62 validated; redundant button removed: {removed}')
