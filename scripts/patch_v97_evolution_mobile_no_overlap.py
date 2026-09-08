from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
patch=r'''
<style id="v97-evolution-mobile-no-overlap">
/* V97 — remise à plat du flux mobile de toute la section Évolution. */
#evolutionSection{display:block !important;width:100% !important;min-width:0 !important;overflow:visible !important}
#evolutionSection>.card{position:relative !important;display:block !important;width:100% !important;min-width:0 !important;height:auto !important;min-height:0 !important;overflow:visible !important;clear:both !important;margin-bottom:16px !important}
#evolutionSection .v94-score-cards,
#evolutionSection .v94-grid,
#evolutionSection .v94-periods,
#evolutionSection .v94-records,
#evolutionSection .v96-record-details{position:relative !important;width:100% !important;height:auto !important;min-height:0 !important;display:grid !important;clear:both !important}
#evolutionSection .v94-analysis,
#evolutionSection .v94-score-card,
#evolutionSection .v94-period,
#evolutionSection .v94-record,
#evolutionSection .v96-record-detail{position:relative !important;float:none !important;display:block !important;width:auto !important;height:auto !important;min-height:0 !important;box-sizing:border-box !important;clear:none !important;overflow:visible !important}
#evolutionSection .v94-score-card .label,
#evolutionSection .v94-score-card .value,
#evolutionSection .v94-score-card .delta,
#evolutionSection .v94-analysis h3,
#evolutionSection .v94-analysis p,
#evolutionSection .v94-period span,
#evolutionSection .v94-record strong,
#evolutionSection .v94-record span,
#evolutionSection .v96-record-detail h3,
#evolutionSection .v96-record-detail p{position:static !important;overflow-wrap:anywhere !important;word-break:normal !important}
@media(max-width:700px){
#evolutionSection>.card{margin-left:0 !important;margin-right:0 !important;padding:14px !important}
#evolutionSection .v94-score-cards{grid-template-columns:1fr !important;gap:12px !important}
#evolutionSection .v94-grid{grid-template-columns:1fr !important;gap:12px !important}
#evolutionSection .v94-periods{grid-template-columns:1fr !important;gap:12px !important}
#evolutionSection .v94-records{grid-template-columns:1fr !important;gap:12px !important}
#evolutionSection .v96-record-details{grid-template-columns:1fr !important;gap:12px !important;margin-top:12px !important}
#evolutionSection .v94-score-card,
#evolutionSection .v94-analysis,
#evolutionSection .v94-period,
#evolutionSection .v94-record,
#evolutionSection .v96-record-detail{margin:0 !important;padding:14px !important}
#evolutionSection .v94-score-card .label{line-height:1.4 !important}
#evolutionSection .v94-score-card .value{line-height:1.25 !important;margin-top:6px !important}
#evolutionSection .v94-score-card .delta{line-height:1.4 !important;margin-top:5px !important}
#evolutionSection .v94-analysis h3{line-height:1.35 !important;margin-bottom:8px !important}
#evolutionSection .v94-analysis p{line-height:1.55 !important}
#evolutionSection .v94-record-detail h3{line-height:1.35 !important}
#evolutionSection .score-chart-wrap{position:relative !important;width:100% !important;height:300px !important;min-height:300px !important;overflow:hidden !important}
#evolutionSection #scoreEvolutionChartContainer{position:relative !important;width:100% !important;height:100% !important;min-height:0 !important;overflow:hidden !important}
}
@media(max-width:380px){
#evolutionSection>.card{padding:12px !important}
#evolutionSection .v94-score-card,
#evolutionSection .v94-analysis,
#evolutionSection .v94-period,
#evolutionSection .v94-record,
#evolutionSection .v96-record-detail{padding:12px !important}
#evolutionSection .score-chart-wrap{height:260px !important;min-height:260px !important}
}
</style>
'''
s=s.replace('</body>',patch+'\n</body>',1)
p.write_text(s,encoding='utf-8')
print('V97 evolution mobile no-overlap applied')
