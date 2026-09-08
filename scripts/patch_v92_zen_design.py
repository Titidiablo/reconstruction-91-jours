from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = re.sub(r'\n<style id="v92-zen-design">.*?</style>\s*', '\n', s, flags=re.S)
patch = r'''
<style id="v92-zen-design">
:root{
  --zen-bg:#f5f1e8;--zen-surface:#fffdf8;--zen-soft:#f1eee4;
  --zen-sage:#7b8b69;--zen-sage-dark:#5f704f;--zen-brown:#4b4034;
  --zen-muted:#7d7468;--zen-line:#ded7ca;
  --zen-shadow:0 5px 22px rgba(75,64,52,.08);
}
html,body{background:var(--zen-bg)!important;color:var(--zen-brown)!important}
body{line-height:1.65}
h1,h2,h3,.day-number,.exercise-heading h2{font-family:Georgia,'Times New Roman',serif;color:var(--zen-brown)}
h1{letter-spacing:.03em}.subtitle{color:var(--zen-muted)!important;font-family:Georgia,'Times New Roman',serif;font-style:italic}
.card{background:var(--zen-surface)!important;border:1px solid rgba(222,215,202,.7);box-shadow:var(--zen-shadow)!important;border-radius:18px!important}
.nav-buttons{gap:7px!important}.nav-buttons button{background:#ebe7dd!important;color:var(--zen-brown)!important;border:1px solid #d8d0c2!important;border-radius:12px!important;box-shadow:none!important;font-weight:500!important;transition:all .18s ease!important}.nav-buttons button:hover{background:#e2ddcf!important;transform:translateY(-1px)}
.nav-buttons button.nav-active{background:var(--zen-sage)!important;color:white!important;border:2px solid var(--zen-sage-dark)!important;box-shadow:0 4px 12px rgba(95,112,79,.22)!important;font-weight:bold!important;transform:translateY(-1px)}
.nav-buttons button.nav-active::before{content:'✓ '!important}
button.primary{background:var(--zen-sage-dark)!important;color:white!important;border-radius:11px!important}button.secondary{background:#ebe7dd!important;color:var(--zen-brown)!important;border:1px solid #d8d0c2!important;border-radius:11px!important}button.danger{background:#f2e8df!important;color:#8b563b!important;border-radius:11px!important}
input,textarea,select{background:#fffdf9!important;color:var(--zen-brown)!important;border:1px solid #d8d0c2!important;border-radius:11px!important}input:focus,textarea:focus,select:focus{outline:none;border-color:var(--zen-sage)!important;box-shadow:0 0 0 3px rgba(123,139,105,.13)!important}
.exercise-card{border-top:5px solid var(--zen-sage)!important;background:var(--zen-surface)!important}.exercise-section{background:var(--zen-soft)!important;border-color:var(--zen-line)!important;border-radius:14px!important}.exercise-section-title{color:var(--zen-sage-dark)!important}.week-label,.success{color:var(--zen-muted)!important}.progress-container{background:#dfdbd1!important}.progress-bar{background:var(--zen-sage)!important}
#meditation{background:linear-gradient(135deg,#f4f0e5,#eef1e7)!important;border-radius:16px;padding:20px!important;border:1px solid var(--zen-line)}.meditation-media-picker{background:#f7f4ec!important;border:1px solid var(--zen-line)!important;border-radius:14px!important;box-shadow:none!important}
@media(max-width:700px){body{padding:14px}.card{border-radius:15px!important;padding:20px!important}.nav-buttons{gap:5px!important}.nav-buttons button{padding:9px 12px!important}}
</style>
'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('V92 zen design applied')
