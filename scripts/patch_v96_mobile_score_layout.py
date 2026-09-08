from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
s = re.sub(r'\n<style id="v96-mobile-score-layout">.*?</style>\s*', '\n', s, flags=re.S)
patch = r'''
<style id="v96-mobile-score-layout">
#v94Reflection,#v94Reflection *{box-sizing:border-box}
#v94Reflection{width:100%;min-width:0;overflow:hidden}
#v94Reflection .v95-pillars{width:100%;min-width:0}
#v94Reflection .v95-pillar,#v94Reflection .v95-encouragement{min-width:0;height:auto;overflow:visible}
#v94Reflection .v95-pillar-head{min-width:0;flex-wrap:wrap;align-items:flex-start}
#v94Reflection .v95-pillar-title,#v94Reflection .v95-pillar-score,#v94Reflection .v95-pillar-text,#v94Reflection .v95-pillar-path,#v94Reflection p,#v94Reflection strong{overflow-wrap:anywhere;word-break:normal}
@media(max-width:700px){
#v94Reflection{overflow:visible}
#v94Reflection .v95-pillars{display:flex;flex-direction:column;gap:14px;margin:16px 0}
#v94Reflection .v95-pillar{width:100%;display:block;padding:14px}
#v94Reflection .v95-pillar-head{display:flex;justify-content:space-between;gap:6px 10px;margin-bottom:8px}
#v94Reflection .v95-pillar-title{flex:1 1 150px;min-width:0;line-height:1.35}
#v94Reflection .v95-pillar-score{flex:0 1 auto;white-space:normal;line-height:1.3}
#v94Reflection .v95-pillar-text,#v94Reflection .v95-pillar-path{width:100%;display:block}
#v94Reflection .v95-encouragement{width:100%;padding:15px;margin-top:16px}
#v94Reflection .v95-encouragement .main{font-size:18px;line-height:1.4}
#v94Reflection .v95-encouragement .sub{font-size:14px;line-height:1.55}
}
@media(max-width:380px){
#v94Reflection .v95-pillar-head{display:block}
#v94Reflection .v95-pillar-score{display:block;margin-top:5px}
}
</style>
'''
s = s.replace('</body>', patch + '\n</body>', 1)
p.write_text(s, encoding='utf-8')
print('V96 mobile score layout applied')
