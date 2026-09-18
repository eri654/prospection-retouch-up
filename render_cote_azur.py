"""Render one autonomous Côte d'Azur prospecting sheet using the Paris visual model."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data/cote_azur_complete_2026.json").read_text(encoding="utf-8"))
TRIP = json.loads((ROOT / "data/cote_azur_tripadvisor_2026.json").read_text(encoding="utf-8"))
PARIS = (ROOT / "paris_equiphotel_2026.html").read_text(encoding="utf-8")
PARIS_CSS = re.findall(r"<style[^>]*>(.*?)</style>", PARIS, re.S)[-1]

CSS = PARIS_CSS + r"""
body{font-size:12px}button,input,textarea{font:inherit}
.topbar{min-height:48px;height:auto;padding-top:7px;padding-bottom:7px}
.filter-bar{top:48px;align-items:center}.filter-bar input{min-width:180px;flex:1;max-width:400px;border:1.5px solid var(--border-h);border-radius:4px;background:var(--surface);color:var(--text);padding:5px 8px;font-size:11px}
.count-bar{padding:7px 16px;background:var(--surface);border-bottom:1px solid var(--border);font-size:11px;font-weight:700}
.table-wrap{padding-bottom:15px}table{min-width:1800px}thead th{position:static}
.review-cell{min-width:235px;max-width:280px;vertical-align:top}.review-badge{display:inline-block;padding:2px 6px;border-radius:4px;font-size:9px;font-weight:800;margin-bottom:4px}.review-badge.direct{background:#fce4dc;color:#9c361c}.review-badge.general{background:#fff0c7;color:#785307}.review-badge.historical{background:#e8e9ee;color:#4e5361}.review-badge.neutral,.review-badge.no_reviews{background:#e9f4ed;color:#23623c}.review-badge.technical{background:#e7eef8;color:#234f86}.review-summary{font-size:10px;line-height:1.4}.review-opportunity{font-size:10px;margin-top:4px;color:var(--navy-dark)}.review-date{font-size:9px;color:var(--muted);margin-top:4px}
.hotel-name{font-weight:750;font-size:12px}.hotel-address{color:var(--muted);margin-top:3px;font-size:10px}.hotel-source{font-size:10px;margin-top:5px;display:inline-block}
.small-note{font-size:10px;color:var(--muted);margin-top:3px}.origin-tags{display:flex;gap:3px;flex-wrap:wrap}.origin-tag{font-size:9px;font-weight:700;padding:1px 5px;border-radius:3px;background:#e7f0ff;color:#0a3a8a}.origin-tag.generic{background:#ece7f7;color:#543b85}
.contact-item{padding:4px 0 4px 6px}.contact-head{display:flex;align-items:flex-start;gap:4px}.contact-check{width:15px;height:15px;accent-color:#188038;flex:none;margin-top:2px}.contact-name{font-weight:700}.contact-fn{font-size:10px}.contact-proof{font-size:9px;color:var(--muted);margin-top:2px}
.proof-link{display:inline-block;margin-top:3px;color:var(--navy);font-size:10px;font-weight:700}.fallback{border:1px dashed #bd8b44!important;background:#fff8ef!important;color:#7b4b0a!important}.icon-link.linkedin.fallback{color:#7b4b0a}
.status-pill.s-qual{background:#9aa0a6;color:#fff}.row-done{opacity:.62}.section-title{padding:12px 16px 5px;background:var(--bg);font-size:14px;color:var(--navy-dark)}.section-intro{padding:0 16px 9px;color:var(--muted);font-size:11px;background:var(--bg)}
.edit-date{width:120px;max-width:100%;background:var(--edit-bg);color:var(--text);border:1px solid var(--border);padding:4px;font-size:10px}.plain-check{width:16px;height:16px;accent-color:#188038}.editable-col .note-cell{min-height:50px}
.source-proof{display:block;font-size:10px;margin:3px 0}.source-proof em{font-style:normal;color:var(--muted)}.blank{color:var(--muted);font-style:italic}.priority-explain{font-size:10px;color:var(--muted)}
.annex-table{min-width:1120px}.annex-table th{position:static}.annex-table td{padding:7px 9px}.annex-table .note-cell{min-height:42px}.annex-table tr[data-hidden]{display:none}
.footer{padding:16px;background:var(--bg);font-size:10px;color:var(--muted)}
@media(max-width:760px){.topbar{position:relative}.filter-bar{position:relative;top:0}.topbar-stats{width:100%}.filter-bar input{max-width:none;width:100%}.legend-bar{gap:8px}.table-wrap{overflow-x:auto}thead th{position:static}}
@media print{.topbar,.filter-bar{position:relative;top:0}.table-wrap{overflow:visible}table{min-width:0}.annex-table{min-width:0}textarea{border:0}}
"""

HTML = r'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Feuille de route terrain — Côte d’Azur · Retouch’Up</title><style>__CSS__</style></head><body>
<div class="topbar"><div><div class="topbar-title">Suivi Prospection Terrain — Nice · Cannes · Antibes</div><div class="topbar-sub">Retouch’Up · une feuille pour les quatre campagnes · relevé du 18 septembre 2026</div></div><div class="topbar-stats"><span class="tstat ts-p2" id="stat-hotels"></span><span class="tstat ts-p3" id="stat-people"></span><span class="tstat ts-ae" id="stat-campaigns"></span></div></div>
<div class="filter-bar" role="group" aria-label="Filtres de la feuille"><button class="fb active" data-f="all">Tous les hôtels</button><button class="fb" data-f="P2">P2 · contact décisionnaire</button><button class="fb" data-f="P3">P3 · contact identifié</button><button class="fb" data-f="Qual">À qualifier</button><button class="fb" data-f="nice">Nice</button><button class="fb" data-f="cannes">Cannes</button><button class="fb" data-f="antibes">Antibes</button><button class="fb" data-f="annex">Autres fiches</button><input id="search" type="search" aria-label="Rechercher hôtel ou contact" placeholder="Rechercher hôtel, personne, fonction..."></div>
<p class="privacy-note">Les coches, dates, priorités et notes restent sur cet appareil : elles ne se synchronisent pas entre personnes. Les liens « ? » ouvrent une recherche à vérifier. Aucun numéro mobile n’est publié.</p>
<div class="legend-bar"><strong>Comme la feuille Paris :</strong><span class="leg-item">✓ hôtel et personne</span><span class="leg-item">P2 = direction ou technique identifiée</span><span class="leg-item">P3 = autre contact identifié</span><span class="leg-item">À qualifier = hôtel sans contact rattaché</span><span class="leg-item">Avis Tripadvisor = témoignage daté, à vérifier sur place</span><span class="leg-item">✏️ jaune = saisie terrain</span><span class="leg-item">Priorité = clic pour modifier sur cet appareil</span></div>
<div class="count-bar" id="main-count"></div>
<div class="table-wrap"><table id="main-table"><thead><tr><th style="width:36px">✓</th><th style="width:90px">Priorité</th><th style="width:155px">Établissement</th><th style="width:75px">Secteur</th><th style="width:180px">Contact principal</th><th style="width:215px">Tous contacts sur place</th><th style="width:110px">Campagnes</th><th style="width:180px">Rattachement & preuve</th><th style="width:245px">Avis Tripadvisor & signal Retouch’Up</th><th style="width:160px">Adresse & accès</th><th style="width:115px">Date</th><th class="editable-col" style="width:150px">✏️ Angle d’approche</th><th class="editable-col" style="width:160px">✏️ Résultat de visite</th><th class="editable-col" style="width:150px">✏️ Prochaine étape</th></tr></thead><tbody id="tbody"></tbody></table></div>
<h2 class="section-title" id="autres">Contacts locaux à rattacher</h2><p class="section-intro">Ces six contacts sont liés à Nice par les sources de prospection, mais leur établissement exact reste à confirmer. Aucune visite d’hôtel ne leur est attribuée automatiquement.</p><div class="count-bar" id="annex-count"></div>
<div class="table-wrap"><table class="annex-table"><thead><tr><th>✓</th><th>Origine</th><th>Personne</th><th>Hôtel / organisation</th><th>Fonction</th><th>Preuve</th><th>LinkedIn</th><th>HubSpot</th><th>✏️ Note terrain</th><th>✏️ Prochaine étape</th></tr></thead><tbody id="annex-body"></tbody></table></div>
<p class="footer">Périmètre : Nice, Cannes, Antibes et communes voisines des hôtels du parcours. Sources des adresses : sites officiels des hôtels ou annuaire public. Rattachements : profils et publications LinkedIn, documents de prospection et fiches CRM signalés dans chaque ligne. Avis Tripadvisor : 68 fiches consultées au 18 septembre 2026 ; les avis reflètent l'expérience de voyageurs et doivent être revalidés avant prospection. Une case sans défaut matériel précis ne constitue pas un besoin Retouch’Up. Les prestations possibles renvoient à <a href="https://retouch-up.fr/" target="_blank" rel="noopener noreferrer">Retouch’Up</a>. 124 fiches locales, dont 90 personnes et 34 fiches d’établissement ; 168 inscriptions locales issues des quatre campagnes. Les listes sources comptent 219 inscriptions au total, dont 51 hors de ce périmètre. Les personnes présentes dans deux hôtels sont affichées dans chacun des deux parcours. <a href="index.html">Toutes les feuilles</a>.</p>
<script>
const DATA=__DATA__;
const TRIP=__TRIP__;
const HOTELS=Object.entries(DATA.hotels).flatMap(([city,rows])=>rows.map(h=>({...h,city})));
const RECORDS=DATA.records;
const CITY={nice:'Nice',cannes:'Cannes',antibes:'Antibes',hotels:'Hôtels génériques'};
const ORDER=['nice','cannes','antibes'];
const KEY='retouchup_cote_azur_complete_2026_v1';
let state={};try{state=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const enc=encodeURIComponent;
const link=(url,label,display,cls='')=>'<a class="'+cls+'" href="'+esc(url)+'" target="_blank" rel="noopener noreferrer" title="'+esc(label)+'" aria-label="'+esc(label)+'">'+display+'</a>';
const liSearch=(name,type='companies')=>'https://www.linkedin.com/search/results/'+type+'/?keywords='+enc(name);
const hsSearch=name=>'https://app.hubspot.com/contacts/19495777/objects/0-1/views/all/list?query='+enc(name);
const maps=h=>'https://www.google.com/maps/search/?api=1&query='+enc(h.name+', '+h.address);
const hs=r=>r.hubspotId?link('https://app.hubspot.com/contacts/19495777/record/0-1/'+enc(r.hubspotId),'Fiche HubSpot de '+r.name,'HubSpot','hubspot-link'):link(hsSearch(r.name),'Recherche HubSpot de '+r.name+' ; fiche directe non vérifiée','HubSpot ?','hubspot-link search fallback');
const li=r=>r.linkedin?link(r.linkedin,'Profil LinkedIn enregistré pour '+r.name,'in','icon-link linkedin'):link(liSearch(r.name,'people'),'Recherche LinkedIn ; profil personnel non vérifié pour '+r.name,'in ?','icon-link linkedin fallback');
function hotelLi(h,people){const r=people.find(p=>p.linkedin);return r?link(r.linkedin,'Profil LinkedIn de '+r.name+' associé à '+h.name,'in','icon-link linkedin'):link(liSearch(h.name),'Recherche LinkedIn de '+h.name+' ; page officielle non vérifiée','in ?','icon-link linkedin fallback')}
function origins(rs){const all=[...new Set(rs.flatMap(r=>r.origins))];return all.map(o=>'<span class="origin-tag '+(o==='hotels'?'generic':'')+'">'+esc(CITY[o])+'</span>').join('')}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){}}
const byHotel=new Map(HOTELS.map(h=>[h.name,[]]));
RECORDS.forEach(r=>r.hotelNames.forEach(name=>{if(byHotel.has(name))byHotel.get(name).push(r)}));
function rank(r){const role=r.role.toLowerCase();if(/directeur|directrice|direction|g[eé]n[eé]ral|technique|maintenance/.test(role))return 3;if(/gouvernante|housekeeping|exploitation|op[eé]ration/.test(role))return 2;return 1}
function defaultStatus(rs){const people=rs.filter(r=>r.kind==='person'&&!r.associationLabel.includes('non concluant'));if(people.some(r=>rank(r)>=2))return 'P2';return people.length?'P3':'Qual'}
function contact(r,check=true){const id='c_'+r.key;return '<div class="contact-item"><div class="contact-head">'+(check?'<input type="checkbox" class="contact-check" data-save="'+id+'_done" aria-label="Contact '+esc(r.name)+' traité" '+(state[id+'_done']?'checked':'')+'>':'')+'<div><span class="contact-name">'+esc(r.name)+'</span><span class="inline-links">'+li(r)+'</span><span class="contact-fn">'+esc(r.role)+'</span>'+hs(r)+'</div></div></div>'}
function proof(r){const label=esc(r.associationLabel);return '<div class="source-proof"><strong>'+esc(r.name)+'</strong> · <em>'+label+'</em>'+(r.associationSource?' '+link(r.associationSource,'Source du rattachement de '+r.name,'Source ↗','proof-link'):'')+'</div>'}
function review(h){const r=TRIP.hotels[h.name];if(!r)throw new Error('Avis Tripadvisor manquant : '+h.name);const badges={historical:'Avis ancien à revalider',direct:'Défaut matériel décrit',general:'Rafraîchissement évoqué',neutral:'Aucun défaut ciblé',technical:'Sujet technique ou service',no_reviews:'Aucun avis publié'};return '<td class="review-cell"><span class="review-badge '+esc(r.level)+'">'+(badges[r.level]||'Avis consultés')+'</span><div class="review-summary">'+esc(r.summary)+'</div>'+(r.opportunity?'<div class="review-opportunity"><strong>Angle Retouch’Up :</strong> '+esc(r.opportunity)+'</div>':'')+'<div class="review-date">Avis : '+esc(r.date)+'</div>'+link(r.url,'Lire la fiche Tripadvisor de '+h.name,'Voir la fiche ↗','proof-link')+'</td>'}
const tbody=document.getElementById('tbody');
ORDER.forEach((city,ci)=>{
  const sep=document.createElement('tr');sep.className='day-sep';sep.dataset.city=city;sep.innerHTML='<td colspan="14">Étape '+(ci+1)+' · '+CITY[city]+' · dates de passage à fixer</td>';tbody.appendChild(sep);
  HOTELS.filter(h=>h.city===city).forEach(h=>{
    const records=byHotel.get(h.name)||[];const people=records.filter(r=>r.kind==='person').sort((a,b)=>rank(b)-rank(a)||a.name.localeCompare(b.name,'fr'));const main=people[0];
    const id='h_'+h.city+'_'+h.name;const prio=state[id+'_prio']||defaultStatus(records);const row=document.createElement('tr');row.dataset.city=city;row.dataset.prio=prio;row.dataset.search=(h.name+' '+h.address+' '+h.sector+' '+(TRIP.hotels[h.name]?.summary||'')+' '+records.map(r=>r.name+' '+r.role+' '+r.association+' '+r.origins.join(' ')).join(' ')).toLocaleLowerCase('fr');row.dataset.key=id;
    const hotelBadge=records.filter(r=>r.kind==='hotel_record').length;
    row.innerHTML='<td class="checkbox-col"><input type="checkbox" class="plain-check" data-save="'+esc(id+'_done')+'" aria-label="Visite '+esc(h.name)+' effectuée" '+(state[id+'_done']?'checked':'')+'></td>'+
      '<td><button type="button" class="status-pill '+(prio==='P2'?'s-p2':prio==='P3'?'s-p3':'s-qual')+'" data-status="'+esc(id)+'" aria-label="Modifier priorité '+esc(h.name)+'">'+(prio==='Qual'?'À qualifier':prio)+'</button></td>'+
      '<td><div class="hotel-name">'+esc(h.name)+' <span class="inline-links">'+hotelLi(h,people)+link(maps(h),'Ouvrir '+h.name+' dans Google Maps','📍','icon-link maps')+'</span></div><div class="small-note">'+(hotelBadge?hotelBadge+' fiche(s) d’établissement dans les campagnes':'Établissement du parcours')+'</div></td>'+
      '<td>'+esc(CITY[city])+'<div class="small-note">'+esc(h.sector)+'</div></td>'+
      '<td>'+(main?contact(main,false):'<span class="blank">Aucun contact rattaché</span>')+'</td>'+
      '<td><div class="contacts-list">'+(people.length?people.map(contact).join(''):'<span class="blank">À identifier sur place</span>')+'</div></td>'+
      '<td><div class="origin-tags">'+(records.length?origins(records):'<span class="blank">Prospection terrain</span>')+'</div></td>'+
      '<td>'+(people.length?people.map(proof).join(''):'<span class="blank">Adresse vérifiée ; contact à identifier</span>')+'</td>'+
      review(h)+
      '<td><div class="hotel-address">'+esc(h.address)+'</div>'+link(maps(h),'Itinéraire Google Maps vers '+h.name,'Maps ↗','hotel-source')+' · '+link(h.source,'Source de l’adresse de '+h.name,'Adresse ↗','hotel-source')+'</td>'+
      '<td class="editable-col"><input type="date" class="edit-date" data-save="'+esc(id+'_date')+'" aria-label="Date de visite '+esc(h.name)+'" value="'+esc(state[id+'_date']||'')+'"></td>'+
      ['angle','result','next'].map((k,i)=>'<td class="editable-col"><span class="edit-label">'+['Angle d’approche','Résultat de visite','Prochaine étape'][i]+'</span><textarea class="note-cell" data-save="'+esc(id+'_'+k)+'" aria-label="'+['Angle','Résultat','Prochaine étape'][i]+' '+esc(h.name)+'" placeholder="À remplir">'+esc(state[id+'_'+k]||'')+'</textarea></td>').join('');
    if(state[id+'_done'])row.classList.add('row-done');tbody.appendChild(row);
  });
});
const annex=document.getElementById('annex-body');const unplaced=RECORDS.filter(r=>!r.hotelNames.length);
unplaced.forEach(r=>{const id='c_'+r.key;const row=document.createElement('tr');row.dataset.origins=r.origins.join(' ');row.dataset.search=(r.name+' '+r.association+' '+r.role+' '+r.origins.join(' ')).toLocaleLowerCase('fr');row.innerHTML='<td><input type="checkbox" class="plain-check" data-save="'+id+'_done" aria-label="Fiche '+esc(r.name)+' traitée" '+(state[id+'_done']?'checked':'')+'></td><td><div class="origin-tags">'+origins([r])+'</div></td><td><strong>'+esc(r.name)+'</strong></td><td>'+(r.association?esc(r.association):'<span class="blank">Établissement non identifié</span>')+'<div class="small-note">'+esc(r.associationLabel)+'</div></td><td>'+esc(r.role)+'</td><td>'+(r.associationSource?link(r.associationSource,'Source pour '+r.name,'Source ↗','proof-link'):'<span class="blank">Document de prospection</span>')+'</td><td>'+li(r)+'</td><td>'+hs(r)+'</td>'+['note','next'].map((k,i)=>'<td class="editable-col"><textarea class="note-cell" data-save="'+id+'_'+k+'" aria-label="'+(i?'Prochaine étape':'Note')+' '+esc(r.name)+'">'+esc(state[id+'_'+k]||'')+'</textarea></td>').join('');if(state[id+'_done'])row.classList.add('row-done');annex.appendChild(row)});
document.getElementById('stat-hotels').textContent=HOTELS.length+' hôtels';
document.getElementById('stat-people').textContent=RECORDS.filter(r=>r.kind==='person').length+' personnes · '+RECORDS.filter(r=>r.kind==='hotel_record').length+' fiches hôtel';
document.getElementById('stat-campaigns').textContent=RECORDS.reduce((n,r)=>n+r.origins.length,0)+' inscriptions locales · 4 campagnes';
document.querySelectorAll('tbody').forEach(body=>{
  body.addEventListener('input',e=>{const key=e.target.dataset.save;if(!key)return;state[key]=e.target.type==='checkbox'?e.target.checked:e.target.value;if(e.target.type==='checkbox')e.target.closest('tr').classList.toggle('row-done',e.target.checked);save()});
  body.addEventListener('change',e=>{if(e.target.type==='checkbox')e.target.dispatchEvent(new Event('input',{bubbles:true}))});
});
tbody.addEventListener('click',e=>{const b=e.target.closest('[data-status]');if(!b)return;const key=b.dataset.status+'_prio';const order=['Qual','P3','P2'];const current=state[key]||b.closest('tr').dataset.prio;const next=order[(order.indexOf(current)+1)%order.length];state[key]=next;b.closest('tr').dataset.prio=next;b.className='status-pill '+(next==='P2'?'s-p2':next==='P3'?'s-p3':'s-qual');b.textContent=next==='Qual'?'À qualifier':next;save();applyFilter()});
let active='all';document.querySelectorAll('.fb[data-f]').forEach(b=>b.addEventListener('click',()=>{active=b.dataset.f;document.querySelectorAll('.fb').forEach(x=>x.classList.toggle('active',x===b));applyFilter()}));document.getElementById('search').addEventListener('input',applyFilter);
function applyFilter(){const q=document.getElementById('search').value.trim().toLocaleLowerCase('fr');let shown=0;let aux=0;[...tbody.querySelectorAll('tr:not(.day-sep)')].forEach(row=>{const f=active;const show=(f==='all'||f==='annex'?f==='all':f==='P2'||f==='P3'||f==='Qual'?row.dataset.prio===f:row.dataset.city===f)&&(!q||row.dataset.search.includes(q));row.toggleAttribute('data-hidden',!show);if(show)shown++});tbody.querySelectorAll('.day-sep').forEach(sep=>{let next=sep.nextElementSibling;let any=false;while(next&&!next.classList.contains('day-sep')){if(!next.hasAttribute('data-hidden'))any=true;next=next.nextElementSibling}sep.toggleAttribute('data-hidden',!any)});[...annex.children].forEach(row=>{const show=(active==='all'||active==='annex'||['nice','cannes','antibes'].includes(active)&&row.dataset.origins.split(' ').includes(active))&&(!q||row.dataset.search.includes(q));row.toggleAttribute('data-hidden',!show);if(show)aux++});document.getElementById('main-count').textContent=shown+' / '+HOTELS.length+' hôtels affichés';document.getElementById('annex-count').textContent=aux+' / '+unplaced.length+' autres fiches affichées'}
const zone=new URLSearchParams(location.search).get('zone');if(['nice','cannes','antibes'].includes(zone)){active=zone;document.querySelectorAll('.fb').forEach(b=>b.classList.toggle('active',b.dataset.f===zone))}applyFilter();
</script></body></html>'''

embedded = json.dumps(DATA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
trip_embedded = json.dumps(TRIP, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
(ROOT / "cote_azur_2026.html").write_text(HTML.replace("__CSS__", CSS).replace("__DATA__", embedded).replace("__TRIP__", trip_embedded), encoding="utf-8")
for city in ("nice", "cannes", "antibes"):
    target = f"cote_azur_2026.html?zone={city}"
    redirect = f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><title>Feuille Côte d’Azur</title></head><body><p>La feuille de route est réunie sur <a href="{target}">la page Côte d’Azur</a>.</p></body></html>'
    (ROOT / f"{city}_2026.html").write_text(redirect, encoding="utf-8")
print(f"1 page Côte d'Azur, {sum(len(v) for v in DATA['hotels'].values())} hôtels, {len(DATA['records'])} fiches locales, {sum(len(r['origins']) for r in DATA['records'])} inscriptions locales, {len(TRIP['hotels'])} fiches Tripadvisor")
