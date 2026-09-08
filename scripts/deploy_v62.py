from pathlib import Path
import re

path = Path("index.html")
html = path.read_text(encoding="utf-8")

# V62: remove the redundant in-page save control. The floating save button
# remains the single save action and its existing visibility logic is kept.
html, removed = re.subn(
    r'<button\b[^>]*>[^<]*Sauvegarder ma journée[^<]*</button>',
    '',
    html,
    count=0,
    flags=re.IGNORECASE,
)

# Increment the application version from V61 to V62.
if '>V62</div>' not in html:
    if '>V61</div>' not in html:
        raise SystemExit('Expected V61 application badge')
    html = html.replace('>V61</div>', '>V62</div>', 1)

# Explicit V62 marker for auditability.
marker = '<script id="v62-save-button-cleanup">'
if marker not in html:
    cleanup = '<script id="v62-save-button-cleanup">window.v62SaveButtonCleanup = true;</script>\n'
    if '</body>' in html:
        html = html.replace('</body>', cleanup + '</body>', 1)
    elif '</html>' in html:
        html = html.replace('</html>', cleanup + '</html>', 1)
    else:
        html += '\n' + cleanup

# Final checks: requested change + version + existing floating save control.
if '>V62</div>' not in html:
    raise SystemExit('V62 version badge missing')
if html.count('>V62</div>') != 1:
    raise SystemExit('V62 version badge count invalid')
if 'Sauvegarder ma journée' in html:
    raise SystemExit('Redundant daily save button still present')
if 'id="floatingSaveButton"' not in html:
    raise SystemExit('Floating save button missing')
if marker not in html:
    raise SystemExit('V62 marker missing')

path.write_text(html, encoding='utf-8')
print(f'V62 validated successfully; removed {removed} redundant save button(s)')
