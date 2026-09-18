"""Render the single autonomous Côte d'Azur sheet and legacy redirects."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data/cote_azur_complete_2026.json").read_text(encoding="utf-8"))

HTML = '''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <title>Feuille de route Côte d'Azur · Retouch'Up</title>
  <style>
    :root{--blue:#1155cc;--navy:#0a3a8a;--bg:#cfe2ff;--row:#e8f0fe;--alt:#d2e3fc;--text:#1c2b4a;--muted:#5f6b7a;--border:#a8c0e8;--edit:#fffde5}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:12px/1.45 Inter,system-ui,sans-serif}a{color:#0a4db5}button,input,textarea{font:inherit}button{cursor:pointer}
    a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid #fbbc04;outline-offset:2px}
    header{background:var(--navy);color:#fff;padding:16px 18px;display:flex;justify-content:space-between;align-items:center;gap:15px;flex-wrap:wrap}header h1{margin:0 0 3px;font-size:18px}header p{margin:0;opacity:.84;font-size:11px}header a{color:#fff;font-weight:700}
    .stats{display:flex;gap:8px;flex-wrap:wrap;padding:12px 16px;background:#f5f8ff;border-bottom:1px solid var(--border)}.stat{padding:7px 10px;border-radius:6px;background:#e8f0fe;font-weight:700}.stat strong{font-size:14px;color:var(--navy)}
    .filters{display:flex;gap:7px;align-items:center;flex-wrap:wrap;padding:9px 16px;background:var(--bg);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:4}.fb{border:1px solid #7baee4;background:#fff;color:var(--text);border-radius:5px;padding:5px 9px;font-weight:700}.fb.active{background:var(--blue);border-color:var(--blue);color:#fff}.filters input{border:1px solid #7baee4;border-radius:5px;padding:6px 9px;min-width:200px;flex:1;max-width:400px}
    .notice{margin:0;padding:10px 16px;background:#fff3cd;color:#584300;border-bottom:1px solid #e7d485}.jump{padding:10px 16px;background:#f5f8ff;display:flex;gap:16px;font-weight:700}.jump a{text-decoration:none}.jump a:hover{text-decoration:underline}
    main{padding:0 0 30px}section{scroll-margin-top:60px}h2{font-size:16px;padding:15px 16px 4px;margin:0;color:var(--navy)}.section-note{padding:0 16px 9px;margin:0;color:var(--muted)}.section-count{padding:6px 16px;background:#f5f8ff;border-top:1px solid var(--border);border-bottom:1px solid var(--border);font-weight:700}
    .tablewrap{overflow-x:auto}table{width:100%;border-collapse:collapse;background:#fff}#hotel-table{min-width:1050px}#contact-table{min-width:1180px}thead{background:var(--blue);color:#fff}th{text-align:left;padding:9px;font-size:10px;letter-spacing:.05em;text-transform:uppercase}td{padding:8px 9px;vertical-align:top;border-right:1px solid var(--border);border-bottom:1px solid var(--border)}tbody tr:nth-child(odd){background:var(--row)}tbody tr:nth-child(even){background:var(--alt)}tbody tr[hidden]{display:none}.name{font-weight:750;font-size:12px}.sub{font-size:10.5px;color:var(--muted);margin-top:3px}.badges{display:flex;gap:4px;flex-wrap:wrap;margin-top:4px}.badge{font-size:10px;font-weight:700;border-radius:4px;padding:2px 6px;background:#e7f0ff;color:#0a3a8a}.badge.generic{background:#ece7f7;color:#543b85}.badge.uncertain{background:#fff2df;color:#865000}
    .links{display:inline-flex;gap:4px;margin-left:4px;vertical-align:middle}.icon{display:inline-block;border-radius:4px;text-decoration:none;padding:2px 6px;font-weight:800}.in{background:#0a66c2;color:#fff}.map{background:#fff;color:#d93025;border:1px solid var(--border)}.fallback{background:#fff8ef;color:#8a4a08;border:1px dashed #bc7e33}.hs{background:#ff7a59;color:#1c2b4a}.source{display:inline-block;margin-top:5px;font-size:10px}.address{margin-top:4px;color:var(--muted)}.empty{font-style:italic;color:var(--muted)}
    .check{width:16px;height:16px;accent-color:#188038}.done{opacity:.6}textarea{width:100%;min-height:50px;resize:vertical;padding:6px;background:var(--edit);border:1px solid var(--border);border-radius:4px;color:var(--text)}input[type=date]{width:100%;max-width:145px;padding:5px;border:1px solid var(--border);border-radius:4px;background:var(--edit)}.foot{padding:12px 16px;color:var(--muted);font-size:11px}
    @media(max-width:720px){header h1{font-size:16px}.stats{gap:5px}.stat{flex:1;min-width:120px}.filters{position:static}.notice{line-height:1.5}}
    @media print{.filters{position:static}.tablewrap{overflow:visible}table{min-width:0!important}.jump{display:none}}
  </style>
</head>
<body>
<header><div><h1>Feuille de route terrain — Côte d'Azur</h1><p>Nice · Cannes · Antibes · hôtels génériques · Retouch'Up · relevé du 18 septembre 2026</p></div><a href="index.html">Toutes les feuilles</a></header>
<div class="stats"><div class="stat"><strong id="hotel-total"></strong> hôtels vérifiés</div><div class="stat"><strong id="person-total"></strong> personnes nommées</div><div class="stat"><strong id="establishment-total"></strong> fiches établissement</div><div class="stat"><strong id="membership-total"></strong> inscriptions dans les 4 listes</div></div>
<div class="filters"><button type="button" class="fb active" data-city="all">Tout</button><button type="button" class="fb" data-city="nice">Nice (62)</button><button type="button" class="fb" data-city="cannes">Cannes (47)</button><button type="button" class="fb" data-city="antibes">Antibes (11)</button><button type="button" class="fb" data-city="hotels">Hôtels génériques (99)</button><input id="search" type="search" placeholder="Chercher un hôtel, une personne ou une fonction" aria-label="Rechercher dans la feuille"></div>
<p class="notice">Inventaire des quatre campagnes : une fiche présente dans plusieurs listes apparaît une seule fois, avec toutes ses origines. Un rattachement « à confirmer » ne constitue pas une visite planifiée. Vérifier la fiche CRM avant toute prise de contact. Coches, dates et notes restent uniquement dans ce navigateur : elles ne se synchronisent pas.</p>
<nav class="jump"><a href="#hotels">Hôtels et itinéraire</a><a href="#contacts">Toutes les fiches des campagnes</a></nav>
<main>
  <section id="hotels"><h2>Hôtels et itinéraire</h2><p class="section-note">Adresses sourcées, organisées par zone. Les dates et résultats sont à remplir sur place. La liste des 156 fiches est juste après.</p><div id="hotel-count" class="section-count" aria-live="polite"></div><div class="tablewrap"><table id="hotel-table"><thead><tr><th>✓</th><th>Zone</th><th>Établissement</th><th>Adresse et accès</th><th>Date</th><th>Angle d’approche</th><th>Résultat de visite</th><th>Prochaine étape</th></tr></thead><tbody id="hotel-body"></tbody></table></div></section>
  <section id="contacts"><h2>Toutes les fiches des quatre campagnes</h2><p class="section-note">144 personnes et 12 fiches d’hôtel sans personne nommée ; 219 inscriptions regroupées en 156 fiches distinctes. Les liens « ? » ouvrent une recherche à vérifier.</p><div id="contact-count" class="section-count" aria-live="polite"></div><div class="tablewrap"><table id="contact-table"><thead><tr><th>✓</th><th>Personne ou fiche hôtel</th><th>Listes d’origine</th><th>Établissement indiqué</th><th>Fonction</th><th>LinkedIn</th><th>HubSpot</th><th>Note terrain</th><th>Prochaine étape</th></tr></thead><tbody id="contact-body"></tbody></table></div></section>
</main>
<p class="foot">Sources : feuille de prospection Côte d'Azur, quatre campagnes et portail HubSpot Retouch'Up. Les adresses des hôtels renvoient vers les sites des établissements. La page ne publie aucun e-mail nominatif, numéro mobile ou commande de campagne.</p>
<script>
const DATA=__DATA__;
const HOTELS=Object.entries(DATA.hotels).flatMap(([city,rows])=>rows.map(h=>({...h,city})));
const RECORDS=DATA.records;
const LABELS={nice:'Nice',cannes:'Cannes',antibes:'Antibes',hotels:'Hôtels génériques'};
const KEY='retouchup_cote_azur_complete_2026_v1';let saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const enc=encodeURIComponent;
const link=(url,title,display,cls='')=>'<a class="'+cls+'" href="'+esc(url)+'" target="_blank" rel="noopener noreferrer" title="'+esc(title)+'" aria-label="'+esc(title)+'">'+display+'</a>';
const hsSearch=name=>'https://app.hubspot.com/contacts/19495777/objects/0-1/views/all/list?query='+enc(name);
const liSearch=(name,type)=>'https://www.linkedin.com/search/results/'+type+'/?keywords='+enc(name);
const maps=h=>'https://www.google.com/maps/search/?api=1&query='+enc(h.name+', '+h.address);
function hotelLi(h){const p=h.contacts.find(c=>c.linkedin);return p?link(p.linkedin,'Profil LinkedIn de '+p.name+', personne associée à '+h.name,'in','icon in'):link(liSearch(h.name,'companies'),'Recherche LinkedIn de '+h.name+' ; page officielle non vérifiée','in ?','icon in fallback')}
function recordLi(r){return r.linkedin?link(r.linkedin,'Profil LinkedIn enregistré pour '+r.name+' ; identité à revérifier','in','icon in'):link(liSearch(r.name,r.kind==='person'?'people':'companies'),'Recherche LinkedIn de '+r.name+' ; profil non vérifié','in ?','icon in fallback')}
function recordHs(r){return r.hubspotId?link('https://app.hubspot.com/contacts/19495777/record/0-1/'+enc(r.hubspotId),'Fiche HubSpot correspondant à '+r.name,'HubSpot','icon hs'):link(hsSearch(r.name),'Rechercher '+r.name+' dans HubSpot ; fiche directe non vérifiée','HubSpot ?','icon hs fallback')}
const hb=document.getElementById('hotel-body');
HOTELS.forEach(h=>{const id='h_'+h.city+'_'+h.name;const tr=document.createElement('tr');tr.dataset.city=h.city;tr.dataset.search=(h.name+' '+h.address+' '+h.city).toLocaleLowerCase('fr');tr.innerHTML='<td><input class="check" type="checkbox" data-save="'+esc(id+'_done')+'" aria-label="Visite '+esc(h.name)+' effectuée" '+(saved[id+'_done']?'checked':'')+'></td><td><span class="badge">'+esc(LABELS[h.city])+'</span><div class="sub">'+esc(h.sector)+'</div></td><td class="name">'+esc(h.name)+'</td><td><div class="address">'+esc(h.address)+'</div><span class="links">'+hotelLi(h)+link(maps(h),'Recherche Google Maps : '+h.name+', '+h.address,'📍','icon map')+'</span><br>'+link(h.source,'Site de '+h.name+' : source de l’adresse','Source / adresse','source')+'</td><td><input type="date" data-save="'+esc(id+'_date')+'" aria-label="Date de visite : '+esc(h.name)+'" value="'+esc(saved[id+'_date']||'')+'"></td>'+['angle','result','next'].map(k=>'<td><textarea data-save="'+esc(id+'_'+k)+'" aria-label="'+esc(k+' : '+h.name)+'" placeholder="À remplir">'+esc(saved[id+'_'+k]||'')+'</textarea></td>').join('');if(saved[id+'_done'])tr.classList.add('done');hb.appendChild(tr)});
const cb=document.getElementById('contact-body');
RECORDS.forEach(r=>{const id='c_'+r.key;const tr=document.createElement('tr');tr.dataset.origins=r.origins.join(' ');tr.dataset.search=(r.name+' '+r.role+' '+r.association+' '+r.origins.map(o=>LABELS[o]).join(' ')).toLocaleLowerCase('fr');const origins=r.origins.map(o=>'<span class="badge '+(o==='hotels'?'generic':'')+'">'+esc(LABELS[o])+'</span>').join('');const assoc=r.association?'<div>'+esc(r.association)+'</div><div class="sub">'+esc(r.associationLabel)+'</div>':'<span class="badge uncertain">À confirmer</span>';tr.innerHTML='<td><input class="check" type="checkbox" data-save="'+id+'_done" aria-label="Fiche '+esc(r.name)+' traitée" '+(saved[id+'_done']?'checked':'')+'></td><td><span class="name">'+esc(r.name)+'</span>'+(r.kind==='hotel_record'?'<div class="sub">Sans personne nommée</div>':'')+'</td><td><div class="badges">'+origins+'</div></td><td>'+assoc+'</td><td>'+esc(r.role)+'</td><td>'+recordLi(r)+'</td><td>'+recordHs(r)+'</td><td><textarea data-save="'+id+'_note" aria-label="Note terrain : '+esc(r.name)+'" placeholder="Observation">'+esc(saved[id+'_note']||'')+'</textarea></td><td><textarea data-save="'+id+'_next" aria-label="Prochaine étape : '+esc(r.name)+'" placeholder="À définir">'+esc(saved[id+'_next']||'')+'</textarea></td>';if(saved[id+'_done'])tr.classList.add('done');cb.appendChild(tr)});
document.getElementById('hotel-total').textContent=HOTELS.length;
document.getElementById('person-total').textContent=RECORDS.filter(r=>r.kind==='person').length;
document.getElementById('establishment-total').textContent=RECORDS.filter(r=>r.kind==='hotel_record').length;
document.getElementById('membership-total').textContent=DATA.campaigns.reduce((n,c)=>n+c.memberships,0);
function save(){try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(e){}}
document.querySelectorAll('tbody').forEach(body=>{body.addEventListener('input',e=>{const k=e.target.dataset.save;if(!k)return;saved[k]=e.target.type==='checkbox'?e.target.checked:e.target.value;if(k.endsWith('_done'))e.target.closest('tr').classList.toggle('done',e.target.checked);save()});body.addEventListener('change',e=>{if(e.target.type==='checkbox')e.target.dispatchEvent(new Event('input',{bubbles:true}))})});
let city=new URLSearchParams(location.search).get('zone')||'all';if(!LABELS[city])city='all';
function selectCity(value){city=value;document.querySelectorAll('.fb').forEach(b=>b.classList.toggle('active',b.dataset.city===city));applyFilter()}
document.querySelectorAll('.fb').forEach(b=>b.addEventListener('click',()=>selectCity(b.dataset.city)));
document.getElementById('search').addEventListener('input',applyFilter);
function applyFilter(){const q=document.getElementById('search').value.trim().toLocaleLowerCase('fr');let hc=0,rc=0;[...hb.children].forEach(row=>{const show=(city==='all'||row.dataset.city===city)&&(!q||row.dataset.search.includes(q));row.hidden=!show;if(show)hc++});[...cb.children].forEach(row=>{const show=(city==='all'||row.dataset.origins.split(' ').includes(city))&&(!q||row.dataset.search.includes(q));row.hidden=!show;if(show)rc++});document.getElementById('hotel-count').textContent=hc+' / '+HOTELS.length+' hôtels affichés';document.getElementById('contact-count').textContent=rc+' / '+RECORDS.length+' fiches affichées'}
selectCity(city);
</script>
</body>
</html>
'''

embedded = json.dumps(DATA, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
(ROOT / "cote_azur_2026.html").write_text(HTML.replace("__DATA__", embedded), encoding="utf-8")
for city in ("nice", "cannes", "antibes"):
    target = f"cote_azur_2026.html?zone={city}"
    redirect = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><title>Feuille Côte d'Azur</title></head><body><p>La feuille de route est réunie sur <a href="{target}">la page Côte d'Azur</a>.</p></body></html>'''
    (ROOT / f"{city}_2026.html").write_text(redirect, encoding="utf-8")
print(f"1 page, {sum(len(v) for v in DATA['hotels'].values())} hôtels, {len(DATA['records'])} fiches, {sum(c['memberships'] for c in DATA['campaigns'])} inscriptions")
