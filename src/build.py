# Generates the static HTML pages.  Usage: python3 src/build.py  (from anywhere)
import os
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(R)
SZ={f[:-4]:Image.open('img/'+f).size for f in os.listdir('img') if f.endswith('.jpg') and not f.endswith('-800.jpg')}
EMAIL='soukainaaitali321@gmail.com'; TEL='+212 631 309 171'; TELH='+212631309171'; CV='cv/Soukaina_Ait_Ali_CV.pdf'

def fig(n,alt,cap='',cls='',eager=False,sizes='(min-width:900px) 60vw, 100vw',lb=True):
    w,h=SZ[n]; c=f'<figcaption>{cap}</figcaption>' if cap else ''
    o,e=(f'<a href="img/{n}.jpg" data-lb aria-label="Enlarge: {cap or alt}">','</a>') if lb else ('','')
    return (f'<figure class="fig {cls}">{o}'
            f'<img src="img/{n}-800.jpg" srcset="img/{n}-800.jpg 800w, img/{n}.jpg {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" '
            f'{"fetchpriority=high" if eager else "loading=lazy"} decoding=async>{e}{c}</figure>')

def page(fn,title,desc,body,cls='',og='rc-main'):
    nav=''.join(f'<a href="{h}"{" aria-current=page" if h==fn else ""}>{t}</a>' for h,t in
        [('projects.html','Projects'),('about.html','About'),('contact.html','Contact'),(CV,'CV')])
    open(fn,'w',encoding='utf-8').write(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:image" content="img/{og}.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png"><link rel="icon" type="image/png" sizes="192x192" href="favicon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css"></head>
<body class="{cls}"><a class="skip" href="#main">Skip to content</a>
<header class="top"><a class="brand" href="index.html">Soukaina Ait Ali</a><nav aria-label="Main navigation">{nav}</nav></header>
<main id="main">{body}</main>
<footer class="foot"><p class="foot-big">Let’s talk about your space.</p>
<p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{TELH}">{TEL}</a><br>Marrakech, Morocco</p>
<p><a href="projects.html">Projects</a><br><a href="about.html">About</a><br><a href="{CV}">Download CV (PDF)</a></p>
<p class="small">© 2026 Soukaina Ait Ali</p></footer>
<dialog id="lb" aria-label="Enlarged image"><button class="x" aria-label="Close">Close</button><img alt=""></dialog>
<script src="js/site.js" defer></script></body></html>''')

P={
 'rehabilitation':dict(fn='project-rehabilitation.html',t='Rehabilitation Centre',cls='t-rehab',cover='rc-main',meta='Academic project · Rabat',num='01',
   tag='A rehabilitation centre in Rabat for behavioural addictions linked to instant gratification, organised around a central garden.',
   alt='Garden of the rehabilitation centre at sunset: curved stone bench, wooden pergola and orange tree',
   thumbs=[('rc-plan-layout','Floor plan','sheet'),('rc-bedroom-mood','Bedroom moodboard','board'),('rc-art-render','Art therapy room','')]),
 'reborn':dict(fn='project-reborn.html',t='REBORN',cls='t-reborn',cover='reborn-persp-salon',meta='Concept store',num='02',
   tag='A concept store that gives furniture a second life, with a workshop where customers learn to repair and customise.',
   alt='REBORN lounge: grey sofa, copper pendant lamps and black pipework on the wall',
   thumbs=[('reborn-logo-palette','Logo and palette','sheet'),('reborn-plans-amenagement-electricite','Floor and electrical plans','sheet'),('reborn-persp-entree','Entrance','')]),
 'allure':dict(fn='project-allure.html',t='Parapharmacy Allure',cls='t-allure',cover='para-persp-boutique',meta='Parapharmacy and spa concept',num='03',
   tag='A parapharmacy and a wellness spa under one roof, over three levels.',
   alt='Parapharmacy shop seen from the mezzanine: wooden shelving, counter and parquet floor',
   thumbs=[('para-moodboard','Moodboard','board'),('para-plan-etage','First-floor plan','sheet'),('para-persp-spa','Spa treatment rooms','')]),
}
order=list(P)
def nxt(k):
    n=P[order[(order.index(k)+1)%3]]; return f'<a class="next" href="{n["fn"]}"><span>Next project</span><b>{n["t"]}</b></a>'
def sec(i,id_,title,intro,inner):
    return f'<section class="sec" id="{id_}"><header class="sec-h"><span class="num">{i:02d}</span><h2>{title}</h2>{f"<p>{intro}</p>" if intro else ""}</header><div class="sec-b">{inner}</div></section>'
def case(k,lead,secs,idx):
    p=P[k]; ix=''.join(f'<a href="#{a}">{b}</a>' for a,b in idx)
    body=f'''<header class="cs-hero"><div class="cs-t"><p class="kind">{p["meta"]}</p><h1>{p["t"]}</h1><p class="lead">{lead}</p><nav class="cs-idx" aria-label="Sections">{ix}</nav></div>
{fig(p["cover"],p["alt"],cls="cs-cover",eager=True,sizes="(min-width:900px) 58vw, 100vw")}</header>{secs}<div class="end">{nxt(k)}</div>'''
    page(p['fn'],f'{p["t"]} — Soukaina Ait Ali',p['tag'],body,p['cls'],p['cover'])
def room(id_,title,txt,mats,render,rcap,mood,mcap,sheets,flip=False,ra=''):
    return f'''<article class="room{" flip" if flip else ""}" id="{id_}"><div class="room-t"><h3>{title}</h3><p>{txt}</p><p class="mats"><b>Materials</b>{mats}</p></div>
<div class="room-g">{fig(render,ra or rcap,rcap,"cover")}{fig(mood,mcap+" moodboard",mcap+" moodboard","board")}</div><div class="room-s">{sheets}</div></article>'''

# ----- Rehabilitation Centre
s=sec(1,'concept','Concept','The question that started the project.',
 '<p class="big">How can a rehabilitation centre treat behavioural addictions linked to instant gratification, with an interior that supports well-being, digital detox and reconnection with oneself?</p>'
 '<p>Social media, smartphone dependency, short-form content and compulsive shopping affect well-being, relationships and quality of life. The centre answers with architecture, nature and interior design working together in a modern Mediterranean spirit.</p>')
s+=sec(2,'plans','Plans and sections','The centre is organised around a central garden.',
 '<div class="sheets">'+fig('rc-plan-layout','Floor plan of the rehabilitation centre','Floor plan','sheet')+fig('rc-plan-electrical','Electrical plan of the rehabilitation centre','Electrical plan','sheet')+'</div>'
 '<div class="sheets">'+fig('rc-plan-ceiling','Ceiling plan with two material samples','Ceiling plan','sheet')+fig('rc-sections','Sections A and C through the centre','Sections A and C','sheet')+'</div>')
r=room('bedroom','Bedroom','A calm room for rest: wooden headboard, lime-plastered wall and a large arched window.','woven rattan, travertine, walnut, matte lime plaster','rc-bedroom-render','Bedroom seen from above','rc-bedroom-mood','Bedroom',
 fig('rc-bedroom-plans','Bedroom plan and elevations with dimensions','Plan and elevations','sheet'),ra='Bedroom seen from above: bed, walnut headboard, rug and arched window')
r+=room('cafeteria','Cafeteria','Arches, natural-fibre pendants and a sand-pink counter for a quiet place to eat.','stone, tile','rc-cafe-render-1','Cafeteria','rc-cafe-mood','Cafeteria',
 fig('rc-cafe-plan','Cafeteria floor plan','Plan','sheet')+'<div class="sheets">'+fig('rc-cafe-elev-a','Cafeteria counter and planted wall elevations','Elevations','sheet')+fig('rc-cafe-elev-b','Elevations of the arched windows','Window elevations','sheet')+'</div>',True,ra='Cafeteria with rattan pendants, arched niche and pink counter')
r+=room('art-therapy','Art therapy room','A solid wood table, vaulted niches and warm tones for studio work.','polished concrete floor, terrazzo sink, Arizona dust walls','rc-art-render','Art therapy room','rc-art-mood','Art therapy',
 fig('rc-art-plan','Art therapy room plan and views','Plan and views','sheet'),ra='Art therapy room with wooden tables, vaulted niches and framed artworks')
r+=room('yoga','Yoga room','A linen ceiling, a light wood floor and a row of columns that sets the rhythm.','matte lime plaster, natural stone, linen, woven rattan, wood flooring','rc-yoga-render','Yoga room','rc-yoga-mood','Yoga',
 fig('rc-yoga-plan','Yoga room plan and elevations','Plan and elevations','sheet'),True,ra='Yoga room with wood floor, columns and a stretched fabric ceiling')
s+=sec(3,'spaces','Four spaces','Each room comes with its moodboard, plan and elevations.',r)
s+=sec(4,'perspectives','Perspectives','The courtyard and the pergola.',
 '<div class="gal">'+fig('rc-pool','Courtyard with a swimming pool and arched façade lit at dusk','Courtyard and pool','wide')+fig('rc-pergola','Wooden pergola and bougainvillea in front of an arched door','Pergola')+fig('rc-cafe-render-2','Cafeteria opening onto the garden through large arched doors','Cafeteria, garden side')+'</div>')
case('rehabilitation','Interior architecture for a rehabilitation centre in Rabat: calm, light and a garden at the centre.',s,[('concept','Concept'),('plans','Plans'),('spaces','Spaces'),('perspectives','Perspectives')])

# ----- REBORN
rows=[('Reception','7 m²','1','Spacious, with sofa and coffee table'),('Showroom','75 m²','2',''),('Recycling workshop','30 m²','1',''),('WC','8 m²','2',''),('Storage','16 m²','1',''),('Office','8 m²','1','Admin space with staff storage'),('Kitchenette','15 m²','1','')]
tb='<table class="prog"><caption>Spatial programme</caption><thead><tr><th>Space</th><th>Area</th><th>Qty</th><th>Note</th></tr></thead><tbody>'+''.join(f'<tr><th scope=row>{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a,b,c,d in rows)+'</tbody></table>'
sw=''.join(f'<li><i style="background:{c}"></i><b>{n}</b>{c}</li>' for n,c in [('Green','#98A869'),('Text','#F2F0EF'),('Background','#111111')])
s=sec(1,'concept','Concept','Repair, transform, learn.',
 '<p class="big">REBORN gives furniture and decor a second life.</p><p>The store showcases recycled, restored and transformed pieces. A participatory workshop lets customers learn to repair, customise or create their own objects, encouraging conscious, lasting consumption.</p>'
 +fig('reborn-persp-accueil','REBORN reception: logo wall, pipe shelving and wooden bench','Reception — “New life, old soul”','wide'))
s+=sec(2,'identity','Identity','Green and black for nature, durability and modernity.',
 '<p>A textured white wordmark suggests transformation, with a circular leaf icon for rebirth and recycling. The vintage, textured typeface echoes raw material.</p>'
 +fig('reborn-logo-palette','REBORN logo on black with a three-colour palette','Logo and palette','sheet wide')+f'<ul class="sw">{sw}</ul>'
 +'<div class="gal">'+fig('reborn-mockups','Logo applied to a coffee cup, a black notebook and an armchair cushion','Brand applications')+fig('reborn-site-web','REBORN website mockup on laptop and phone','Website mockup')+'</div>')
s+=sec(3,'programme','Programme','Seven spaces, from the entrance to the workshop.','<div class="gal two">'+tb+fig('reborn-organigramme','Spatial diagram: entrance, reception, showrooms, workshop, storage, office, kitchenette and WC','Spatial diagram','sheet')+'</div>')
s+=sec(4,'plans','Plans and details','A large showroom, with the workshop at the back.',
 fig('reborn-plans-amenagement-electricite','Layout plan and electrical plan of the store','Layout and electrical plans','sheet wide')+fig('reborn-plans-sol-plafond','Floor plan in polished concrete and ceiling plan','Floor and ceiling plans','sheet wide')
 +'<div class="sheets">'+fig('reborn-coupe-elevation','Section and elevation of the store','Section and elevation','sheet')+fig('reborn-elevations','Elevations of the display wall and the pipe wall','Elevations','sheet')+'</div>'
 +fig('reborn-details-reception','Reception details: plans, front and side profiles of the counter','Reception details','sheet wide'))
s+=sec(5,'perspectives','Perspectives','Copper, polished concrete, reclaimed wood and plants.',
 '<div class="gal">'+fig('reborn-persp-salon','Store lounge: grey sofa, copper pendants and black pipes on the wall','Lounge','wide')+fig('reborn-persp-entree','Entrance with round mirror, wooden bench and black glass partition','Entrance')+fig('reborn-persp-equipe','Two team members in REBORN t-shirts in the sales area','In use')
 +fig('reborn-sanitaires','Two views of the restroom: basin, round mirror and copper pipes','Restroom','board')+fig('reborn-facade','Store front in a shopping gallery with the REBORN logo','Store front')+'</div>')
case('reborn','A furniture concept store, from visual identity to interior perspectives.',s,[('concept','Concept'),('identity','Identity'),('programme','Programme'),('plans','Plans'),('perspectives','Perspectives')])

# ----- Allure
s=sec(1,'concept','Concept','The rigour of a parapharmacy, the elegance of a spa.',
 '<p class="big">A place where health, beauty and relaxation meet, designed to inspire trust and serenity.</p><p>The parapharmacy offers dermocosmetic products, natural care and quality supplements. The spa, inside the same space, offers relaxing treatments and wellness rituals.</p>'
 +fig('para-moodboard','Moodboard: terracotta treatment room, stone, pink and gold tones, wooden shelving','Moodboard','wide'))
s+=sec(2,'plans','Three levels','Basement, first floor and mezzanine: layout first, then flooring.',
 '<div class="trio">'+fig('para-plan-sous-sol','Basement layout plan','Basement','sheet')+fig('para-plan-etage','First-floor layout plan','First floor','sheet')+fig('para-plan-mezzanine','Mezzanine layout plan','Mezzanine','sheet')+'</div>'
 +'<p class="mats"><b>Floors</b>28 × 10 cm parquet in the basement and on the first floor; 120 × 120 cm Portofino marble on the mezzanine.</p>'
 +'<div class="trio">'+fig('para-sol-sous-sol','Basement flooring plan, parquet','Basement floor','sheet')+fig('para-sol-etage','First-floor flooring plan, parquet','First-floor floor','sheet')+fig('para-sol-mezzanine','Mezzanine flooring plan, marble','Mezzanine floor','sheet')+'</div>')
s+=sec(3,'elevations','Elevations','The levels in section: shelving, mirrors and a spiral staircase.',
 '<div class="sheets">'+fig('para-elevations-2','Section with hairdressing mirrors, shelving and a spiral staircase','Long section','sheet')+fig('para-elevations-1','Four level elevations with shelving and staircase','Elevations by level','sheet')+'</div>')
s+=sec(4,'perspectives','Perspectives','Shop, hair area, reception and spa.',
 '<div class="gal">'+fig('para-persp-spa','Spa treatment rooms: sculpted partition, plant and terracotta stools','Spa','wide')+fig('para-persp-accueil','Reception lounge with a blue sofa, wooden bar and spiral staircase','Reception')+fig('para-persp-spa-cabine','Glazed sliding door in a curved wooden cabin','Treatment cabin')
 +fig('para-persp-coiffure-2','Hair area: three large oval mirrors and cream chairs','Hair area')+fig('para-persp-coiffure-3','Hair area: black line-drawn face mural and pink armchairs','Hair area')+'</div>')
case('allure','A concept that brings retail and well-being together under one roof.',s,[('concept','Concept'),('plans','Plans'),('elevations','Elevations'),('perspectives','Perspectives')])

# ----- Home
pj=''
for k in order:
    p=P[k]
    pj+=f'''<section class="pj {p["cls"]}" aria-labelledby="h-{k}"><div class="pj-in"><div class="pj-t"><p class="kind">{p["meta"]}</p><h2 id="h-{k}">{p["t"]}</h2><p>{p["tag"]}</p><a class="go" href="{p["fn"]}">View project</a></div>
{fig(p["cover"],p["alt"],cls="pj-fig",sizes="(min-width:900px) 55vw, 100vw",lb=False)}</div></section>'''
meth=''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a,b in [('Survey','Measurements and observations on site, starting from what exists.'),('Choose materials','Textures, colours and materials gathered into boards before any drawing is final.'),('Model','Plans, sections and elevations in AutoCAD; 3D models and renders in SketchUp, Enscape, V-Ray and 3ds Max.'),('Present','Clear presentations for clients, and follow-up of materials and trades.')])
hero=f'''<section class="hero"><div class="hero-t"><p class="kind">Interior designer · Marrakech</p>
<h1><span>Soukaina</span><span>Ait Ali</span></h1><p class="lead">Spaces that read first as a plan, then as material and light.</p></div>
{fig('hero-2','Bedroom with an arched, lit headboard, a bed with a throw, and soft curtains','',cls='h-b',eager=True,sizes='(min-width:900px) 52vw, 100vw',lb=False)}
{fig('hero-1','Entrance corner with a sculptural mirror, a potted plant and a stone stool','',cls='h-a',eager=True,sizes='(min-width:900px) 26vw, 55vw',lb=False)}</section>'''
page('index.html','Soukaina Ait Ali — Interior designer','Portfolio of Soukaina Ait Ali, interior designer: a rehabilitation centre in Rabat, the REBORN concept store and the Parapharmacy Allure.',
 hero+f'<div class="stack">{pj}</div><section class="method wrap"><h2>How I work</h2><ol>{meth}</ol></section><section class="about-cta wrap"><p class="big">Interior design graduate, freelance since 2024.</p><a class="go" href="about.html">About me</a><a class="go" href="contact.html">Get in touch</a></section>','home','hero-2')

# ----- Projects
rws=''
for i,k in enumerate(order):
    p=P[k]; th=''.join(fig(n,a,'',c,sizes='(min-width:900px) 18vw, 33vw',lb=False) for n,a,c in p['thumbs'])
    rws+=f'''<article class="row {p["cls"]} r{i%2}"><div class="row-t"><span class="num">{p["num"]}</span><p class="kind">{p["meta"]}</p><h2><a href="{p["fn"]}">{p["t"]}</a></h2><p>{p["tag"]}</p><span class="go">View project</span></div>
<div class="row-m">{fig(p["cover"],p["alt"],cls="row-cover",sizes="(min-width:900px) 58vw, 100vw",lb=False)}<div class="strip">{th}</div></div></article>'''
page('projects.html','Projects — Soukaina Ait Ali','Three projects by Soukaina Ait Ali: a rehabilitation centre in Rabat, the REBORN concept store and the Parapharmacy Allure.',
 f'<div class="wrap"><h1 class="pg-h">Projects</h1></div><div class="rows">{rws}</div>','proj')

# ----- About
def li(t,s,d): return f'<li><b>{t}</b><span>{s}</span><em>{d}</em></li>'
ab=f'''<div class="wrap about"><div class="about-l">{fig('about-soukaina','Portrait of Soukaina Ait Ali','','portrait',eager=True,sizes='(min-width:900px) 34vw, 100vw')}</div>
<div class="about-r"><h1 class="pg-h">About</h1><p class="big">Interior design graduate, passionate about creating aesthetic, functional spaces that fit their users’ needs.</p>
<section><h2>Education</h2><ul class="tl">{li('Diploma in Interior Design','Collège LaSalle, Marrakech','2023 – 2026')}{li('Bachelor’s in English Studies','Cadi Ayyad University, Marrakech','2020 – 2023')}</ul></section>
<section><h2>Experience</h2><ul class="tl">{li('Freelance interior designer','Design of a residential kitchen and a master bedroom: site surveys, 3D modelling, material selection and client presentations.','2024 – present')}{li('Internship','Arhazi Creation, Marrakech','Jul – Sep 2025')}{li('Client advisor','Majorel, Marrakech','Jul – Sep 2024')}</ul></section>
<section><h2>Software</h2><p>AutoCAD · SketchUp · 3ds Max · Photoshop · V-Ray · Enscape · Canva</p></section>
<section><h2>Skills</h2><p>Space planning, interior design, 3D visualisation, moodboards, materials, project coordination and client relations.</p></section>
<section><h2>Languages</h2><p>Arabic (native), French (fluent), English (fluent).</p></section>
<p><a class="go" href="{CV}">Download CV (PDF)</a></p></div></div>'''
page('about.html','About — Soukaina Ait Ali','Education, experience and software of Soukaina Ait Ali, interior designer, graduate of Collège LaSalle (2023–2026).',ab,'about-pg','about-soukaina')
ct=f'''<div class="wrap contact"><h1 class="pg-h">Contact</h1><p class="big">A project, a collaboration, a question? Write or call.</p>
<dl><div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div><div><dt>Phone</dt><dd><a href="tel:{TELH}">{TEL}</a></dd></div><div><dt>City</dt><dd>Marrakech, Morocco</dd></div><div><dt>CV</dt><dd><a href="{CV}">Download the PDF</a></dd></div></dl></div>'''
page('contact.html','Contact — Soukaina Ait Ali','Contact Soukaina Ait Ali, interior designer: email, phone and CV.',ct,'contact-pg')
print('pages ok')
