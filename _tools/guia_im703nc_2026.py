# -*- coding: utf-8 -*-
"""Gera o guia de prova web (PT/EN) do IRONMAN 70.3 North Carolina 2026.
Saida: prova/im703nc-2026-yfqwts/index.html
Rodar: python3 _tools/guia_im703nc_2026.py
"""
import os, html

SLUG = 'im703nc-2026-yfqwts'
OUT = os.path.join(os.path.dirname(__file__), '..', 'prova', SLUG, 'index.html')
VERSAO = 'v0.1 · rascunho · 02/out/2026'

# ---------- helpers ----------
def L(pt, en=None):
    """Texto inline bilingue."""
    en = pt if en is None else en
    if pt == en:
        return pt
    return f'<span lang="pt">{pt}</span><span lang="en">{en}</span>'

def P(pt, en, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<p{c} lang="pt">{pt}</p><p{c} lang="en">{en}</p>'

def U(km, mi):
    """Unidade dupla: mostra km ou milhas conforme o seletor."""
    return f'<span class="u-km">{km}</span><span class="u-mi">{mi}</span>'

def C(c, f):
    return f'<span class="u-km">{c}</span><span class="u-mi">{f}</span>'

def tm(hhmm):
    """'07:10' -> PT 7h10 / EN 7:10 AM"""
    h, m = map(int, hhmm.split(':'))
    pt = f'{h}h' + (f'{m:02d}' if m else '')
    ap = 'AM' if h < 12 else 'PM'
    h12 = h % 12 or 12
    en = f'{h12}:{m:02d} {ap}'
    return L(pt, en)

def rng(a, b):
    return f'{tm(a)} – {tm(b)}'

TBC = L('a confirmar', 'to be confirmed')
def tbc():
    return f'<span class="tbc">{TBC}</span>'

def sec_head(num, kick_pt, kick_en, title_pt, title_en, lead_pt=None, lead_en=None):
    h = f'<div class="kick">{num} · {L(kick_pt, kick_en)}</div><h2 class="disp">{L(title_pt, title_en)}</h2>'
    if lead_pt:
        h += P(lead_pt, lead_en, 'lead')
    return h

def box(kind, title_pt, title_en, body_pt, body_en):
    return (f'<div class="box {kind}"><div class="box-t">{L(title_pt, title_en)}</div>'
            f'{P(body_pt, body_en)}</div>')

def bullets(items):
    out = '<ul class="dash">'
    for pt, en in items:
        out += f'<li>{L(pt, en)}</li>'
    return out + '</ul>'

def steps(items):
    out = '<ol class="steps">'
    for pt, en in items:
        out += f'<li>{L(pt, en)}</li>'
    return out + '</ol>'

def kv(rows):
    """Linhas rotulo / detalhe."""
    out = '<div class="kv">'
    for (kpt, ken), (vpt, ven) in rows:
        out += f'<div class="kv-k">{L(kpt, ken)}</div><div class="kv-v">{L(vpt, ven)}</div>'
    return out + '</div>'

def mapa(src, alt_pt, alt_en, cap_pt, cap_en):
    return (f'<figure class="map"><a href="img/{src}" target="_blank" rel="noopener">'
            f'<img src="img/{src}" loading="lazy" alt="{alt_pt}"></a>'
            f'<figcaption>{L(cap_pt, cap_en)} · <span class="muted">{L("toque para ampliar", "tap to enlarge")}</span></figcaption></figure>')

def fotos(*items):
    """items: (arquivo, legenda_pt, legenda_en, classe)"""
    out = '<div class="fotos">'
    for f, cpt, cen, cls in items:
        out += (f'<figure class="foto {cls}"><img src="img/{f}" loading="lazy" alt="{cpt}">'
                f'<figcaption>{L(cpt, cen)}</figcaption></figure>')
    return out + '</div>'

def trechos(rows):
    """rows: (km, mi, nome_pt, nome_en, carac_pt, carac_en, verbo_pt, verbo_en, exec_pt, exec_en)"""
    out = '<div class="segs">'
    for i, r in enumerate(rows, 1):
        km, mi, npt, nen, cpt, cen, vpt, ven, ept, een = r
        out += (f'<article class="seg"><div class="seg-top"><span class="seg-n">{i:02d}</span>'
                f'<span class="seg-d">{U("km " + km, "mi " + mi)}</span></div>'
                f'<h3>{L(npt, nen)}</h3><p class="seg-c">{L(cpt, cen)}</p>'
                f'<div class="verb disp">{L(vpt, ven)}</div><p class="seg-e">{L(ept, een)}</p></article>')
    return out + '</div>'

# ---------- dados ----------
# Agenda: (hora, evento_pt, evento_en, local_pt, local_en, time?, a_confirmar?)
ALOFT = ('Aloft Wilmington Coastline Center', 'Aloft Wilmington Coastline Center')
AGENDA = [
 ('thu', L('Quinta, 15 de outubro', 'Thursday, October 15'), [
   (rng('14:00','19:00'), 'Check-in do atleta e retirada do chip. Leve documento com foto e o QR code da inscrição', 'Athlete check-in and timing chip pick-up. Bring photo ID and your registration QR code', 'Aloft · Atlantic Room', 'Aloft · Atlantic Room', False, False),
   (tm('15:00'), '<b>Time CMTeam:</b> briefing oficial juntos e, logo depois, check-in do time. No check-in, todos escolhem o mesmo horário de bike check-in de sexta (14h)', '<b>CMTeam:</b> official briefing together, then team check-in. At check-in, everyone picks the same Friday bike check-in slot (2:00 PM)', 'Aloft · Outdoor Expo Area', 'Aloft · Outdoor Expo Area', True, True),
   (tm('16:00'), 'Q&amp;A com a diretora de prova (opcional, não substitui o briefing)', 'Q&amp;A with the Race Director (optional, does not replace the briefing)', 'Aloft · Outdoor Expo Area', 'Aloft · Outdoor Expo Area', False, False),
   (tm('17:00'), 'Athlete Briefing, segundo horário. É obrigatório assistir a um', 'Athlete Briefing, second session. Attending one is mandatory', 'Aloft · Outdoor Expo Area', 'Aloft · Outdoor Expo Area', False, False),
   (tm('18:00'), 'Yoga no Battleship (opcional, com inscrição)', 'Yoga on the Battleship (optional, registration required)', 'USS North Carolina', 'USS North Carolina', False, False),
   (tm('18:30'), '<b>Time CMTeam:</b> jantar do time (opcional)', '<b>CMTeam:</b> team dinner (optional)', 'local no grupo do WhatsApp', 'location in the WhatsApp group', True, True),
 ]),
 ('fri', L('Sexta, 16 de outubro', 'Friday, October 16'), [
   (tm('07:10'), '<b>Time CMTeam:</b> retirada das mochilas com o Robério', '<b>CMTeam:</b> backpack pick-up with Robério', 'Hanover Seaside Club', 'Hanover Seaside Club', True, True),
   (tm('07:30'), '<b>Time CMTeam:</b> reconhecimento a pé da saída da natação até a T1, sem entrar na água', '<b>CMTeam:</b> walk-through from the swim exit to T1, without getting in the water', 'Wrightsville Beach', 'Wrightsville Beach', True, True),
   (tm('08:00'), '<b>Time CMTeam:</b> shake-out run, ~20 min leve', '<b>CMTeam:</b> shake-out run, ~20 min easy', 'Wrightsville Beach', 'Wrightsville Beach', True, True),
   (rng('09:00','15:30'), 'Último dia de check-in (prioridade AWA até 12h). Sem check-in no sábado', 'Last check-in window (AWA priority until noon). No check-in on Saturday', 'Aloft · Atlantic Room', 'Aloft · Atlantic Room', False, False),
   (f'{tm("10:00")} · {tm("11:30")} · {tm("14:30")}', 'Athlete Briefing, para quem não assistiu na quinta', 'Athlete Briefing, for those who missed Thursday', 'Aloft · Outdoor Expo Area', 'Aloft · Outdoor Expo Area', False, False),
   (tm('14:00'), '<b>Time CMTeam:</b> bike check-in OBRIGATÓRIO no horário agendado. A bike dorme na T1. O Robério ajuda nos últimos ajustes. A sacola azul pode ficar já', '<b>CMTeam:</b> MANDATORY bike check-in at the booked time. The bike stays overnight in T1. Robério helps with last adjustments. The blue bag can be dropped now', 'T1 · Wrightsville Beach Park', 'T1 · Wrightsville Beach Park', True, True),
   (tm('15:00'), '<b>Time CMTeam:</b> entrega da sacola vermelha (corrida). Fecha às 16h e no sábado ninguém entra na T2', '<b>CMTeam:</b> red run bag drop-off. Closes at 4:00 PM, and nobody gets into T2 on Saturday', 'T2 · Cape Fear Community College', 'T2 · Cape Fear Community College', True, False),
   (tm('15:30'), '<b>Time CMTeam:</b> reunião final com o San: dúvidas e últimos ajustes', '<b>CMTeam:</b> final meeting with San: questions and last tips', 'saída da T2', 'T2 exit', True, False),
   (tm('18:30'), '<b>Time CMTeam:</b> jantar do time (opcional). Jantar cedo, cama cedo', '<b>CMTeam:</b> team dinner (optional). Early dinner, early to bed', 'local no grupo do WhatsApp', 'location in the WhatsApp group', True, True),
 ]),
 ('sat', L('Sábado, 17 de outubro · dia de prova', 'Saturday, October 17 · race day'), [
   (rng('03:45','05:15'), 'Shuttle só para atletas, do centro para a T1', 'Athlete-only shuttle from downtown to T1', 'N 3rd St com Brunswick St', 'N 3rd St & Brunswick St', False, False),
   (tm('04:30'), '<b>Time CMTeam:</b> encontro no ponto do shuttle', '<b>CMTeam:</b> meet at the shuttle stop', 'N 3rd St com Brunswick St', 'N 3rd St & Brunswick St', True, True),
   (rng('04:30','06:25'), 'Transição aberta. Às 6h25 todo mundo fora', 'Transition open. Everyone out by 6:25 AM', 'T1 · Wrightsville Beach Park', 'T1 · Wrightsville Beach Park', False, False),
   (tm('05:45'), '<b>Time CMTeam:</b> encontro na T1 para pegar juntos o shuttle até a largada. Último shuttle às 6h30', '<b>CMTeam:</b> meet at T1 to take the shuttle to the swim start together. Last shuttle at 6:30 AM', 'T1 · Wrightsville Beach Park', 'T1 · Wrightsville Beach Park', True, True),
   (tm('07:10'), 'Largada age group, rolling start por tempo previsto', 'Age group rolling swim start, seeded by expected time', 'Hanover Seaside Club', 'Hanover Seaside Club', False, False),
   (rng('11:30','17:00'), 'Retirada da sacola branca (manhã). Comida pós-prova a partir das 11h', 'White morning clothes bag pick-up. Post-race food from 11:00 AM', 'Water Street Park', 'Water Street Park', False, False),
   (rng('13:45','17:30'), 'Check-out da bike e das sacolas (pulseira obrigatória)', 'Bike and gear bag check-out (wristband required)', 'T2 · Cape Fear Community College', 'T2 · Cape Fear Community College', False, False),
   (rng('14:00','15:00'), '<b>Time CMTeam:</b> bikes e sacolas com o Robério para voltar a Miami. Prazo final 15h15', '<b>CMTeam:</b> bikes and bags to Robério for the trip back to Miami. Hard deadline 3:15 PM', 'saída da T2', 'T2 exit', True, True),
   (tm('16:30'), 'Premiação e vagas para o Mundial 70.3 de 2027 (Chattanooga). Tem que estar presente para aceitar a vaga', 'Awards and 2027 70.3 World Championship slots (Chattanooga). You must be present to accept a slot', 'Aloft · Indoor Ballroom', 'Aloft · Indoor Ballroom', False, False),
   (tm('18:00'), '<b>Time CMTeam:</b> celebração (opcional)', '<b>CMTeam:</b> celebration (optional)', 'local no grupo do WhatsApp', 'location in the WhatsApp group', True, True),
   (tm('19:30'), '<b>Time CMTeam:</b> RiverWalk e sorvete', '<b>CMTeam:</b> RiverWalk and ice cream', 'Downtown RiverWalk · Kilwins', 'Downtown RiverWalk · Kilwins', True, True),
 ]),
]

def agenda_html():
    tabs = '<div class="tabs" role="tablist">'
    panels = ''
    for i, (key, label, rows) in enumerate(AGENDA):
        sel = 'true' if i == 0 else 'false'
        short = {'thu': L('Qui 15', 'Thu 15'), 'fri': L('Sex 16', 'Fri 16'), 'sat': L('Sáb 17', 'Sat 17')}[key]
        tabs += f'<button role="tab" aria-selected="{sel}" data-tab="{key}">{short}</button>'
        panels += f'<div class="tabpanel" data-panel="{key}"{"" if i == 0 else " hidden"}><h3 class="day">{label}</h3><div class="ag">'
        for hora, ept, een, lpt, len_, team, conf in rows:
            cls = 'ag-r team' if team else 'ag-r'
            flag = tbc() if conf else ''
            panels += (f'<div class="{cls}"><div class="ag-t">{hora}</div>'
                       f'<div class="ag-b"><div class="ag-e">{L(ept, een)} {flag}</div>'
                       f'<div class="ag-l">{L(lpt, len_)}</div></div></div>')
        panels += '</div></div>'
    tabs += '</div>'
    return tabs + panels

CHECK = [
 (('Geral', 'General'), [
   ('Documento com foto ou passaporte', 'Photo ID or passport'),
   ('QR code da inscrição', 'Registration QR code'),
   ('Cartão USAT (se anual)', 'USAT card (if annual)'),
   ('Camiseta CMTeam (foto do time)', 'CMTeam t-shirt (team photo)'),
   ('Protetor solar', 'Sunscreen'),
   ('Roupa pós-prova', 'Post-race clothes'),
 ]),
 (('Manhã e natação', 'Morning and swim'), [
   ('Pulseira de atleta no pulso', 'Athlete wristband on'),
   ('Chip no tornozelo esquerdo', 'Timing chip on left ankle'),
   ('Touca oficial da prova', 'Official race swim cap'),
   ('Wetsuit ou speedsuit', 'Wetsuit or speedsuit'),
   ('Óculos de natação (2)', 'Swim goggles (2)'),
   ('Trisuit', 'Trisuit'),
   ('Vaselina ou Body Glide', 'Vaseline or Body Glide'),
   ('Chinelo e casaco velhos', 'Old flip-flops and sweatshirt'),
   ('Relógio', 'Watch'),
   ('Café da manhã e garrafa de água', 'Breakfast and water bottle'),
 ]),
 (('Sacola azul · T1', 'Blue bag · T1'), [
   ('Capacete com adesivo na frente', 'Helmet with sticker on the front'),
   ('Óculos de sol', 'Sunglasses'),
   ('Sapatilha e meias', 'Bike shoes and socks'),
   ('Nutrição da bike', 'Bike nutrition'),
   ('Manguito ou corta-vento (manhã fria)', 'Arm warmers or wind vest (cold morning)'),
 ]),
 (('Bike', 'Bike'), [
   ('Bike com adesivo nos dois lados do quadro', 'Bike with frame sticker visible on both sides'),
   ('Adesivo da mesa (entre o guidão)', 'Stem sticker (between handlebars)'),
   ('Garrafas (2+) e aero bottle', 'Bottles (2+) and aero bottle'),
   ('Câmara, CO2, espátulas e ferramentas', 'Tube, CO2, levers and tools'),
   ('Ciclocomputador carregado', 'Bike computer charged'),
   ('Potenciômetro: bateria e calibração', 'Power meter: battery and calibration'),
   ('Cinta de frequência cardíaca', 'Heart rate strap'),
 ]),
 (('Sacola vermelha · T2', 'Red bag · T2'), [
   ('Tênis de prova e meias', 'Race shoes and socks'),
   ('Boné ou viseira', 'Cap or visor'),
   ('Cinto com o número', 'Race belt with bib'),
   ('Nutrição da corrida', 'Run nutrition'),
   ('Óculos de sol (se não usar os da bike)', 'Sunglasses (if not using the bike pair)'),
 ]),
 (('Sacola branca · pós-prova', 'White bag · post-race'), [
   ('Roupa seca e chinelo', 'Dry clothes and flip-flops'),
   ('Toalha', 'Towel'),
   ('Nada de valor dentro', 'Nothing valuable inside'),
 ]),
]

def checklist_html():
    out = '<div class="ck-grid">'
    n = 0
    for (gpt, gen), items in CHECK:
        out += f'<div class="ck"><div class="ck-h">{L(gpt, gen)}</div>'
        for pt, en in items:
            n += 1
            out += f'<label class="ck-i"><input type="checkbox" data-ck="c{n}"><span>{L(pt, en)}</span></label>'
        out += '</div>'
    out += '</div>'
    out += f'<div class="ck-foot"><span id="ckcount"></span><button type="button" id="ckreset" class="ghost">{L("Limpar marcações", "Clear all")}</button></div>'
    return out

PLANNER = [
 (('Sua meta', 'Your goal'), [('Natação','Swim'),('T1','T1'),('Bike','Bike'),('T2','T2'),('Corrida','Run'),('Total','Total')]),
 (('Logística da manhã', 'Morning logistics'), [('Despertar','Wake up'),('Café da manhã','Breakfast'),('Shuttle centro → T1','Shuttle downtown → T1'),('Shuttle T1 → largada','Shuttle T1 → swim start'),('Chegada na largada','Arrive at swim start'),('Aquecimento','Warm-up'),('Corral','Start corral'),('Sua largada','Your start')]),
 (('Estratégia', 'Pacing'), [('Natação','Swim'),('Bike (IF / watts)','Bike (IF / watts)'),('Corrida (pace / PSE)','Run (pace / RPE)')]),
]

def planner_html():
    out = '<div class="pl-grid">'
    n = 0
    for (gpt, gen), items in PLANNER:
        out += f'<div class="pl"><div class="ck-h">{L(gpt, gen)}</div>'
        for pt, en in items:
            n += 1
            out += f'<label class="pl-i"><span>{L(pt, en)}</span><input type="text" data-pl="p{n}" autocomplete="off"></label>'
        out += '</div>'
    out += (f'<div class="pl pl-wide"><div class="ck-h">{L("Lembretes pessoais", "Personal reminders")}</div>'
            f'<textarea data-pl="notes" rows="4"></textarea></div></div>')
    out += P('Fica salvo só neste aparelho. Ninguém mais vê o que você escreve aqui.',
             'Saved on this device only. Nobody else sees what you write here.', 'muted small')
    return out

# ---------- página ----------
CSS = r"""
:root{--red:#CB333B;--red2:#F9423A;--ink:#1A1A1A;--dark:#111;--dark2:#161616;--sand:#F6F4F1;--line:#E4E1DD;--muted:#5A5A5A;--gold:#FFC72C}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{overflow-x:clip}
body{margin:0;font-family:Arial,Helvetica,sans-serif;background:var(--sand);color:var(--ink);-webkit-font-smoothing:antialiased;line-height:1.55}
img{max-width:100%;display:block}
a{color:var(--red)}
.disp{font-family:'Barlow Condensed',Arial,sans-serif;font-weight:800;font-style:italic;text-transform:uppercase}
html[data-lang="pt"] body [lang="en"],html[data-lang="en"] body [lang="pt"]{display:none !important}
html[data-u="km"] .u-mi,html[data-u="mi"] .u-km{display:none}
.in{max-width:920px;margin:0 auto;padding:0 20px}
/* topo */
.top{position:sticky;top:0;z-index:30;background:var(--dark);color:#fff;border-bottom:1px solid #262626}
.top .in{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:60px}
.top img{height:26px;width:auto}
.tg{display:flex;gap:8px}
.sw{display:flex;border:1.5px solid #4A4A4A;border-radius:999px;overflow:hidden}
.sw button{background:transparent;color:#D6D6D6;border:0;font:inherit;font-size:12px;font-weight:700;letter-spacing:1px;padding:0 12px;min-height:38px;cursor:pointer}
.sw button[aria-pressed="true"]{background:#fff;color:var(--dark)}
.nav{background:var(--dark2);border-top:1px solid #262626}
.nav .in{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-top:10px;padding-bottom:10px}
.nav .in::-webkit-scrollbar{display:none}
.nav a{flex-shrink:0;color:#D6D6D6;text-decoration:none;font-size:12px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;padding:9px 14px;border-radius:999px;border:1px solid #333}
.nav a.on{background:var(--red);border-color:var(--red);color:#fff}
/* rascunho */
.draft{background:var(--gold);color:var(--ink);font-size:14px}
.draft .in{padding-top:10px;padding-bottom:10px}
.tbc{display:inline-block;vertical-align:1px;background:#FFF1C2;border:1px solid #E7B416;color:#6B4E00;font-size:11px;font-weight:700;letter-spacing:.8px;text-transform:uppercase;padding:1px 7px;border-radius:999px;white-space:nowrap}
/* hero */
.hero{position:relative;background:var(--dark);color:#fff;overflow:hidden}
.hero-bg{position:absolute;left:0;right:0;top:0;height:clamp(330px,46vw,600px);background:url(img/hero-capa-2026.jpg) center 68%/cover}
.hero:after{content:"";position:absolute;left:0;right:0;top:0;height:clamp(330px,46vw,600px);background:linear-gradient(180deg,rgba(17,17,17,.05) 0%,rgba(17,17,17,.2) 45%,rgba(17,17,17,1) 100%)}
.racelogo{width:340px;max-width:78%;height:auto;margin:6px 0 34px;filter:drop-shadow(0 4px 18px rgba(0,0,0,.35))}
.hero h1.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.hero-sub{font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;text-transform:uppercase;font-size:34px;line-height:1;color:#fff}
.hero-sub span{color:var(--red2)}
.hero .in{position:relative;z-index:1;padding-top:clamp(150px,30vw,400px);padding-bottom:48px;display:flex;flex-direction:column;gap:16px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--gold)}
.hero h1{margin:0;font-size:68px;line-height:.9;letter-spacing:-.5px}
.hero h1 small{display:block;font-size:.5em;color:var(--red2);letter-spacing:0}
.hero-meta{font-size:17px;color:#E6E6E6;font-weight:700}
.letter{margin-top:8px;border-left:3px solid var(--red);padding-left:18px;max-width:680px}
.letter p{margin:0 0 12px;font-size:17px;line-height:1.65;color:#D9D9D9}
.letter .sig{color:#fff;font-weight:700;font-size:15px}
.stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:10px}
.stat{background:rgba(255,255,255,.06);border:1px solid #333;border-radius:14px;padding:14px 16px}
.stat b{display:block;font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;font-size:30px;line-height:1;color:#fff}
.stat span{font-size:13px;color:#B5B5B5}
/* secoes */
section{padding:56px 0;scroll-margin-top:110px}
section.alt{background:#fff}
section.darkband{background:var(--dark);color:#fff}
.kick{font-size:12px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--red);margin-bottom:8px}
h2{margin:0 0 14px;font-size:52px;line-height:.95}
h3{margin:30px 0 10px;font-size:20px;line-height:1.25}
.lead{font-size:18px;line-height:1.6;color:#3A3A3A;margin:0 0 8px;max-width:760px}
p{margin:0 0 12px}
.muted{color:var(--muted)}
.small{font-size:13px}
.dash{margin:8px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:10px}
.dash li{position:relative;padding-left:22px;font-size:16px;line-height:1.55}
.dash li:before{content:"";position:absolute;left:0;top:.72em;width:12px;height:2px;background:var(--red)}
.steps{margin:8px 0 0;padding:0;list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:12px}
.steps li{counter-increment:s;display:grid;grid-template-columns:34px 1fr;gap:10px;font-size:16px;line-height:1.55}
.steps li:before{content:counter(s,decimal-leading-zero);font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;color:var(--red);font-size:20px;line-height:1.2}
/* caixas */
.box{border-radius:16px;padding:20px 22px;margin:22px 0;background:var(--sand);border-left:4px solid var(--ink)}
section.alt .box{background:var(--sand)}
section:not(.alt) .box{background:#fff}
.box-t{font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px}
.box p{margin:0;font-size:16px;line-height:1.6}
.box.warn{border-left-color:var(--red)}
.box.warn .box-t{color:var(--red)}
.box.gold{border-left-color:var(--gold);background:#FFF8E1 !important}
.box.quote p{font-size:19px;font-style:italic;line-height:1.5}
/* numeros */
.legs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:18px}
.leg{background:#fff;border-radius:18px;padding:22px}
section.alt .leg{background:var(--sand)}
.leg .disp{font-size:34px;line-height:1;color:var(--red)}
.leg .d{font-size:20px;font-weight:700;margin:6px 0 10px}
.leg p{font-size:15px;color:#3A3A3A;margin:0 0 8px}
.leg .cut{font-size:13px;font-weight:700;letter-spacing:.5px;color:var(--ink);border-top:1px solid var(--line);padding-top:10px;margin-top:10px}
/* kv */
.kv{display:grid;grid-template-columns:200px 1fr;border-top:1px solid var(--line);margin-top:10px}
.kv-k,.kv-v{padding:14px 0;border-bottom:1px solid var(--line);font-size:16px;line-height:1.5}
.kv-k{font-weight:700;padding-right:16px}
/* agenda */
.tabs{display:flex;gap:8px;margin:18px 0 6px;position:sticky;top:108px;z-index:5;background:inherit;padding:8px 0}
.tabs button{flex:1;font:inherit;font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;text-transform:uppercase;font-size:22px;padding:10px 6px;border-radius:12px;border:1.5px solid var(--line);background:#fff;color:var(--ink);cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--ink);border-color:var(--ink);color:var(--gold)}
.day{margin:18px 0 6px;font-size:15px;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}
.ag{border-top:1px solid var(--line)}
.ag-r{display:grid;grid-template-columns:150px 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--line)}
.ag-t{font-weight:700;font-size:16px;white-space:nowrap}
.ag-e{font-size:16px;line-height:1.5}
.ag-l{font-size:14px;color:var(--muted);margin-top:4px}
.ag-r.team{background:linear-gradient(90deg,rgba(203,51,59,.07),transparent 70%);border-left:3px solid var(--red);padding-left:12px;margin-left:-15px}
.ag-r.team .ag-t{color:var(--red)}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin-top:12px}
.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;background:var(--red);vertical-align:-1px;margin-right:6px}
/* trechos */
.segs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:16px}
.seg{background:#fff;border-radius:18px;padding:20px 22px;display:flex;flex-direction:column}
section.alt .seg{background:var(--sand)}
.seg-top{display:flex;justify-content:space-between;align-items:center;gap:10px}
.seg-n{font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;font-size:20px;color:var(--red)}
.seg-d{font-size:13px;font-weight:700;letter-spacing:.5px;background:var(--ink);color:#fff;border-radius:999px;padding:4px 10px}
.seg h3{margin:12px 0 4px;font-size:19px}
.seg-c{font-size:14px;color:var(--muted);margin:0 0 12px}
.verb{font-size:40px;line-height:1;color:var(--red);margin-top:auto;padding-top:8px;border-top:1px solid var(--line)}
.seg-e{font-size:15px;line-height:1.55;margin:8px 0 0}
/* mapas */
.maps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:18px}
.map{margin:0;background:#fff;border-radius:16px;padding:10px;border:1px solid var(--line)}
.map img{border-radius:10px;width:100%;height:auto}
.map figcaption{font-size:13px;font-weight:700;padding:10px 4px 2px}
.map .muted{font-weight:400}
.mapwide{grid-column:1/-1}
/* sacolas */
.bags{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:16px}
.bag{background:#fff;border-radius:18px;padding:18px;display:flex;flex-direction:column;gap:8px}
section.alt .bag{background:var(--sand)}
.bag img{height:84px;width:auto;object-fit:contain;align-self:flex-start}
.bag b{font-size:16px}
.bag p{font-size:14px;color:#3A3A3A;margin:0}
/* postos */
.aid{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.aid>span{background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:6px 12px;font-size:14px;font-weight:700}
section.alt .aid>span{background:var(--sand)}
/* tabela regras */
.rules{border-top:1px solid var(--line);margin-top:12px}
.rule{display:grid;grid-template-columns:1fr 2fr auto;gap:16px;padding:14px 0;border-bottom:1px solid var(--line);font-size:15px;line-height:1.5}
.rule b{font-size:15px}
.pen{justify-self:start;font-size:12px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:4px 10px;border-radius:999px;background:var(--ink);color:#fff;white-space:nowrap;align-self:start}
.pen.blue{background:#1F4FB5}.pen.yel{background:var(--gold);color:var(--ink)}.pen.red{background:var(--red)}
/* clima */
.wx{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:16px}
.wx div{background:var(--sand);border-radius:16px;padding:16px}
.wx b{display:block;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted)}
.wx .t{font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;font-size:34px;line-height:1.1;color:var(--ink)}
.wx p{font-size:14px;margin:6px 0 0}
/* duas colunas */
.cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.cols h3{margin-top:10px}
/* checklist */
.ck-grid,.pl-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:18px}
.ck,.pl{background:#fff;border-radius:18px;padding:18px}
section.alt .ck,section.alt .pl{background:var(--sand)}
.ck-h{font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--red);margin-bottom:8px}
.ck-i{display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-top:1px solid var(--line);font-size:15px;line-height:1.4;cursor:pointer}
.ck-i input{width:22px;height:22px;flex-shrink:0;accent-color:var(--red);margin:0}
.ck-i input:checked+span{color:#9A9A9A;text-decoration:line-through}
.ck-foot{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:14px;font-weight:700}
.ghost{font:inherit;font-size:14px;font-weight:700;background:transparent;border:1.5px solid var(--line);border-radius:999px;padding:10px 16px;cursor:pointer;color:var(--ink)}
.pl-i{display:grid;grid-template-columns:1fr 1.1fr;gap:10px;align-items:center;padding:7px 0;border-top:1px solid var(--line);font-size:14px}
.pl-i input,.pl textarea{font:inherit;font-size:16px;border:1.5px solid var(--line);border-radius:10px;padding:8px 10px;background:#fff;width:100%;min-height:40px}
section.alt .pl-i input{background:#fff}
.pl textarea{resize:vertical}
.pl-wide{grid-column:1/-1}
/* regras de ouro */
.gold-rules{margin:20px 0 0;padding:0;list-style:none;counter-reset:g;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 28px}
.gold-rules li{counter-increment:g;display:grid;grid-template-columns:44px 1fr;gap:8px;padding:14px 0;border-top:1px solid #333;font-size:16px;line-height:1.5;color:#E6E6E6}
.gold-rules li:before{content:counter(g,decimal-leading-zero);font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;font-size:26px;line-height:1;color:var(--gold)}
.darkband h2{color:#fff}
.darkband .kick{color:var(--gold)}
.mantra{margin:36px 0 0;border-left:3px solid var(--red);padding-left:20px}
.mantra p{font-size:22px;line-height:1.45;font-style:italic;color:#fff;margin:0 0 4px}
.final p{font-size:17px;line-height:1.7;color:#D9D9D9;max-width:720px}
.motto{margin-top:28px;font-family:'Barlow Condensed',Arial,sans-serif;font-style:italic;font-weight:800;font-size:30px;color:#fff}
.motto span{color:var(--red)}
.fotos{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:24px 0}
.foto{margin:0;position:relative;border-radius:16px;overflow:hidden;background:var(--ink)}
.foto img{width:100%;height:100%;object-fit:cover;aspect-ratio:4/3}
.foto.tall img{aspect-ratio:3/4}
.foto.wide{grid-column:1/-1}
.foto.wide img{aspect-ratio:16/9}
.foto figcaption{position:absolute;left:0;right:0;bottom:0;padding:28px 14px 10px;background:linear-gradient(transparent,rgba(0,0,0,.72));color:#fff;font-size:13px;font-weight:700;letter-spacing:.3px}
.photos{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:28px}
.photos img{border-radius:16px;aspect-ratio:4/3;object-fit:cover;width:100%}
footer{background:#0B0B0B;color:#9A9A9A;font-size:13px;line-height:1.6}
footer .in{padding-top:28px;padding-bottom:40px;display:flex;flex-direction:column;gap:8px}
footer b{color:#fff}
.totop{position:fixed;right:16px;bottom:16px;z-index:40;width:48px;height:48px;border-radius:999px;background:var(--red);color:#fff;display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:22px;box-shadow:0 8px 24px rgba(0,0,0,.3);opacity:0;pointer-events:none;transition:opacity .25s}
.totop.show{opacity:1;pointer-events:auto}
@media (max-width:760px){
 .hero h1{font-size:48px}
 .racelogo{width:240px;margin-bottom:24px}
 .hero-sub{font-size:28px}
 h2{font-size:40px}
 section{padding:44px 0}
 .legs,.segs,.maps,.bags,.cols,.ck-grid,.pl-grid,.gold-rules{grid-template-columns:minmax(0,1fr)}
 .wx{grid-template-columns:repeat(2,minmax(0,1fr))}
 .kv{grid-template-columns:minmax(0,1fr)}
 .kv-k{border-bottom:0;padding-bottom:0}
 .ag-r{grid-template-columns:minmax(0,1fr);gap:4px}
 .ag-r.team{margin-left:-12px}
 .rule{grid-template-columns:minmax(0,1fr)}
 .stats{grid-template-columns:repeat(3,minmax(0,1fr))}
 .stat b{font-size:24px}
 .tabs{top:104px}
 .tabs button{font-size:18px}
 .photos{grid-template-columns:1fr 1fr}
 .fotos{gap:8px}
 .foto figcaption{font-size:12px;padding:22px 10px 8px}
}
@media print{
 .top,.nav,.tabs,.totop,.ck-foot,.draft{display:none !important}
 [hidden]{display:block !important}
 body,section,section.alt,section.darkband,.hero,footer{background:#fff !important;color:#000 !important}
 .hero-bg,.hero:after,.photos,.maps,.fotos{display:none !important}
 .hero .in{padding-top:0}
 .racelogo{filter:invert(1)}
 .hero h1,.darkband h2,.gold-rules li,.mantra p,.final p,.motto,.letter p,.letter .sig,.stat b,.hero-meta{color:#000 !important}
 .verb,.kick,.seg-n,.ag-r.team .ag-t,.box.warn .box-t,.ck-h,.hero h1 small,.motto span,.gold-rules li:before{color:#000 !important}
 .seg,.leg,.box,.ck,.pl,.bag,.stat,.wx div{border:1px solid #999;background:#fff !important}
 .seg-d,.pen{background:#fff !important;color:#000 !important;border:1px solid #000}
 .ag-r.team{background:#EEE !important;border-left-color:#000}
 section{padding:18px 0;break-inside:auto}
 .seg,.box,.ag-r,.rule{break-inside:avoid}
}
"""

JS = r"""
(function(){
var K='cmteam-'+document.body.getAttribute('data-k');
function get(k){try{return localStorage.getItem(K+k)}catch(e){return null}}
function set(k,v){try{localStorage.setItem(K+k,v)}catch(e){}}
var root=document.documentElement;
var qp=new URLSearchParams(location.search);
var lang=qp.get('lang')||get(':lang')||'pt'; if(lang!=='en')lang='pt';
var unit=get(':u')||(lang==='en'?'mi':'km');
function apply(){root.setAttribute('data-lang',lang);root.lang=lang==='pt'?'pt-BR':'en';root.setAttribute('data-u',unit);
 document.querySelectorAll('[data-setlang]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-setlang')===lang)});
 document.querySelectorAll('[data-setu]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-setu')===unit)});
 document.title=lang==='pt'?'Guia de prova · IRONMAN 70.3 North Carolina 2026 · CMTeam':'Race guide · IRONMAN 70.3 North Carolina 2026 · CMTeam';
 count();}
document.querySelectorAll('[data-setlang]').forEach(function(b){b.addEventListener('click',function(){var had=get(':u');lang=b.getAttribute('data-setlang');set(':lang',lang);if(!had)unit=lang==='en'?'mi':'km';apply();})});
document.querySelectorAll('[data-setu]').forEach(function(b){b.addEventListener('click',function(){unit=b.getAttribute('data-setu');set(':u',unit);apply();})});
// abas da agenda
var tabs=document.querySelectorAll('[data-tab]');
function openTab(k){tabs.forEach(function(t){t.setAttribute('aria-selected',t.getAttribute('data-tab')===k)});document.querySelectorAll('[data-panel]').forEach(function(p){p.hidden=p.getAttribute('data-panel')!==k});set(':tab',k);}
tabs.forEach(function(t){t.addEventListener('click',function(){openTab(t.getAttribute('data-tab'))})});
var d=new Date(),tk=get(':tab');
var ymd=d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate();
if(ymd===20261016)tk='fri'; else if(ymd>=20261017)tk='sat'; else if(ymd===20261015)tk='thu';
if(tk)openTab(tk);
// checklist
var cks=document.querySelectorAll('[data-ck]');
function count(){var n=0;cks.forEach(function(c){if(c.checked)n++});var el=document.getElementById('ckcount');if(el)el.textContent=lang==='pt'?(n+' de '+cks.length+' itens prontos'):(n+' of '+cks.length+' items ready');}
cks.forEach(function(c){c.checked=get(':'+c.getAttribute('data-ck'))==='1';c.addEventListener('change',function(){set(':'+c.getAttribute('data-ck'),c.checked?'1':'0');count();})});
var rs=document.getElementById('ckreset');if(rs)rs.addEventListener('click',function(){cks.forEach(function(c){c.checked=false;set(':'+c.getAttribute('data-ck'),'0')});count();});
// planner
document.querySelectorAll('[data-pl]').forEach(function(i){var v=get(':'+i.getAttribute('data-pl'));if(v)i.value=v;i.addEventListener('input',function(){set(':'+i.getAttribute('data-pl'),i.value)})});
// nav ativa + voltar ao topo
var links=[].slice.call(document.querySelectorAll('.nav a'));var secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))});
var tt=document.querySelector('.totop');
function onScroll(){var y=scrollY+140,cur=null;secs.forEach(function(s,i){if(s&&s.offsetTop<=y)cur=i});links.forEach(function(a,i){a.classList.toggle('on',i===cur)});
 if(cur!==null){var a=links[cur],nav=a.parentNode;var l=a.offsetLeft-nav.clientWidth/2+a.clientWidth/2;if(Math.abs(nav.scrollLeft-l)>40)nav.scrollTo({left:l,behavior:'smooth'})}
 tt.classList.toggle('show',scrollY>800);}
addEventListener('scroll',onScroll,{passive:true});
apply();onScroll();
})();
"""

def build():
    H = []
    a = H.append
    a('<!doctype html>\n<html lang="pt-BR" data-lang="pt" data-u="km">\n<head>\n<meta charset="utf-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      '<meta name="robots" content="noindex, nofollow, noarchive">\n'
      '<title>Guia de prova · IRONMAN 70.3 North Carolina 2026 · CMTeam</title>\n'
      '<link rel="icon" type="image/png" sizes="32x32" href="../../img/favicon-32.png?v=3">\n'
      '<link rel="apple-touch-icon" href="../../img/apple-touch-icon.png?v=3">\n'
      '<meta name="theme-color" content="#111111">\n'
      '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
      '<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,700;0,800;1,800&amp;display=swap" rel="stylesheet">\n'
      f'<style>{CSS}</style>\n'
      '<script data-goatcounter="https://cmteam.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
      '</head>\n')
    a(f'<body data-k="{SLUG}">\n')
    # topo
    a('<div class="top"><div class="in"><a href="../../" aria-label="CMTeam"><img src="../../img/cmteam-logo-branco.png" alt="CMTeam"></a>'
      '<div class="tg"><div class="sw" role="group" aria-label="Idioma / Language"><button type="button" data-setlang="pt" aria-pressed="true">PT</button><button type="button" data-setlang="en" aria-pressed="false">EN</button></div>'
      '<div class="sw" role="group" aria-label="km / mi"><button type="button" data-setu="km" aria-pressed="true">KM</button><button type="button" data-setu="mi" aria-pressed="false">MI</button></div></div></div>')
    nav = [('agenda', 'Agenda', 'Schedule'), ('prova', 'A prova', 'The race'), ('logistica', 'Logística', 'Logistics'),
           ('natacao', 'Natação', 'Swim'), ('bike', 'Bike', 'Bike'), ('corrida', 'Corrida', 'Run'),
           ('clima', 'Clima', 'Weather'), ('semana', 'Race week', 'Race week'), ('checklist', 'Checklist', 'Checklist'),
           ('planner', 'Planner', 'Planner'), ('regras', 'Regras de ouro', 'Golden rules')]
    a('<nav class="nav"><div class="in">' + ''.join(f'<a href="#{i}">{L(p, e)}</a>' for i, p, e in nav) + '</div></nav></div>')
    a('<div class="draft"><div class="in">' + L(
        '<b>Rascunho para o San revisar.</b> Os itens marcados “a confirmar” dependem da logística do time.',
        '<b>Draft for San to review.</b> Items marked “to be confirmed” depend on team logistics.') + '</div></div>')

    # hero
    a('<header class="hero"><div class="hero-bg"></div><div class="in">'
      '<img class="racelogo" src="img/logo-703nc-branco.png" alt="IRONMAN 70.3 North Carolina">'
      f'<div class="eyebrow">{L("Material exclusivo dos atletas CMTeam", "For CMTeam athletes only")}</div>'
      '<h1 class="sr">IRONMAN 70.3 North Carolina 2026</h1>'
      f'<div class="hero-sub">{L("Guia de prova", "Race guide")} <span>2026</span></div>'
      f'<div class="hero-meta">{L("Sábado, 17 de outubro · Wilmington, NC", "Saturday, October 17 · Wilmington, NC")}</div>'
      '<div class="letter">'
      + P('Race week chegou. North Carolina não é uma prova de força: é uma prova de consciência. Começa fria, com a água te despertando. Na bike, o vento conversa e pede paciência. Na corrida, o sol volta, a sombra do lago ajuda e o calor é leve, quase um presente depois de um verão inteiro treinando em Miami.',
            'Race week is here. North Carolina is not a race of strength: it is a race of awareness. It starts cold, with the water waking you up. On the bike, the wind talks and asks for patience. On the run, the sun comes back, the shade around the lake helps, and the heat is mild, almost a gift after a whole summer of training in Miami.')
      + P('Aqui está tudo o que você precisa para o fim de semana: a agenda do time, a logística oficial de 2026, o plano de cada etapa e as regras que mais custam tempo. O que precisava ser feito, já foi feito. Agora é executar com calma.',
            'Here is everything you need for the weekend: the team schedule, the official 2026 logistics, the plan for each leg, and the rules that cost the most time. What had to be done is done. Now it is about executing with calm.')
      + f'<p class="sig">San Palma · CMTeam {tbc()}</p></div>'
      '<div class="stats">'
      f'<div class="stat"><b>{U("1,9 km", "1.2 mi")}</b><span>{L("natação · a favor da maré", "swim · with the tide")}</span></div>'
      f'<div class="stat"><b>{U("90 km", "56 mi")}</b><span>{L("bike · 1 volta, plana", "bike · 1 loop, flat")}</span></div>'
      f'<div class="stat"><b>{U("21,1 km", "13.1 mi")}</b><span>{L("corrida · 2 voltas no lago", "run · 2 laps of the lake")}</span></div>'
      '</div></div></header>\n')

    # 01 agenda
    a('<section id="agenda" class="alt"><div class="in">')
    a(sec_head('01', 'Agenda do time', 'Team schedule', 'O fim de semana', 'The weekend',
               'Horários oficiais do IRONMAN (atualizados em 16/09) e os encontros do time, em destaque vermelho. Mudou algo? O grupo do WhatsApp sempre tem a última palavra.',
               'Official IRONMAN times (updated Sept 16) plus team meet-ups, highlighted in red. If anything changes, the WhatsApp group always has the final word.'))
    a(agenda_html())
    a(f'<div class="legend"><span><i></i>{L("Encontro do time CMTeam", "CMTeam team meet-up")}</span><span>{tbc()} {L("depende da logística do time", "depends on team logistics")}</span></div>')
    a(box('warn', 'Bike check-in com hora marcada', 'Bike check-in by appointment',
          'Novidade de 2026: no check-in do atleta você escolhe o horário de levar a bike para a T1 na sexta, e esse horário é conferido. Para irmos juntos com o Robério, todos escolhem o mesmo horário.',
          'New for 2026: at athlete check-in you choose your Friday bike drop-off time at T1, and that time is checked. To go together with Robério, everyone picks the same slot.'))
    a(fotos(('foto-vaga-mundial.jpg', 'Vaga para o Mundial 70.3 em North Carolina 2025', '70.3 World Championship slot at North Carolina 2025', 'tall'),
            ('foto-finisher.jpg', 'Medalha no peito', 'Medal on', 'tall')))
    a('</div></section>\n')

    # 02 a prova
    a('<section id="prova"><div class="in">')
    a(sec_head('02', 'A prova em números', 'The race in numbers', 'Plana, rápida e com vento', 'Flat, fast and windy',
               'Natação ponto a ponto a favor da maré, bike de uma volta da praia até o centro, corrida em duas voltas pelo Greenfield Lake. O que decide North Carolina não é a altimetria: é a disciplina de potência no vento e a paciência na corrida.',
               'Point-to-point swim with the tide, a one-loop bike from the beach to downtown, and a two-lap run around Greenfield Lake. What decides North Carolina is not the elevation: it is power discipline in the wind and patience on the run.'))
    a('<div class="legs">'
      f'<div class="leg"><div class="disp">{L("Natação", "Swim")}</div><div class="d">{U("1,9 km", "1.2 mi")}</div>'
      f'<p>{L("Banks Channel, Wrightsville Beach. Rolling start por tempo previsto.", "Banks Channel, Wrightsville Beach. Rolling start by expected time.")}</p>'
      f'<div class="cut">{L("Corte: 1h10 a partir da sua entrada na água", "Cut-off: 1:10 from your own start")}</div></div>'
      f'<div class="leg"><div class="disp">Bike</div><div class="d">{U("90 km · D+ 196 m", "56 mi · 643 ft gain")}</div>'
      f'<p>{L("Uma volta, de Wrightsville Beach até o centro de Wilmington. As pontes são as únicas subidas.", "One loop, from Wrightsville Beach to downtown Wilmington. The bridges are the only climbs.")}</p>'
      f'<div class="cut">{L("Corte: 5h30 (natação + T1 + bike). Intermediário: posto 3, ", "Cut-off: 5:30 (swim + T1 + bike). Intermediate: aid station 3, ")}{U("km 76", "mi 47")}, {tm("13:00")}</div></div>'
      f'<div class="leg"><div class="disp">{L("Corrida", "Run")}</div><div class="d">{U("21,1 km · D+ 80 m", "13.1 mi · 261 ft gain")}</div>'
      f'<p>{L("Centro de Wilmington e duas voltas no Greenfield Lake, quase toda na sombra.", "Downtown Wilmington and two laps of Greenfield Lake, mostly in the shade.")}</p>'
      f'<div class="cut">{L("Cortes: ", "Cut-offs: ")}{U("km 11,2", "mi 6.97")} {L("às", "at")} {tm("15:20")} · {U("km 18,2", "mi 11.3")} {L("às", "at")} {tm("16:20")} · {L("total 8h30", "8:30 total")}</div></div>'
      '</div>')
    a(box('gold', 'O que mudou desde 2025', 'What changed since 2025',
          'A corrida agora tem <b>duas voltas</b> no Greenfield Lake, com retirada de pulseira para a segunda volta. O shuttle do centro para a T1 começa mais cedo, às 3h45, e vai só até 5h15. O bike check-in passou a ter hora marcada. A ponte Isabel Holmes também entrou na lista de trechos sem posição aero.',
          'The run now has <b>two laps</b> of Greenfield Lake, with a wristband pick-up for the second lap. The downtown-to-T1 shuttle starts earlier, at 3:45 AM, and runs only until 5:15 AM. Bike check-in is now by appointment. The Isabel Holmes Bridge was added to the no-aero sections.'))
    a('</div></section>\n')

    # 03 logistica
    a('<section id="logistica" class="alt"><div class="in">')
    a(sec_head('03', 'Logística', 'Logistics', 'Duas transições, três sacolas', 'Two transitions, three bags',
               'A natação acaba em Wrightsville Beach, e a bike, no centro. São duas transições separadas, a 20 minutos de carro uma da outra. Quem entende isso no sábado de manhã não corre atrás de nada.',
               'The swim finishes at Wrightsville Beach and the bike finishes downtown. They are two separate transitions, 20 minutes apart by car. Knowing this on Saturday morning means you never chase anything.'))
    a('<h3>' + L('Os lugares', 'The places') + '</h3>')
    a(kv([
        (('Village, check-in, briefings, premiação', 'Village, check-in, briefings, awards'), ('Aloft Wilmington Coastline Center, 501 Nutt St', 'Aloft Wilmington Coastline Center, 501 Nutt St')),
        (('Largada da natação', 'Swim start'), ('Hanover Seaside Club, 601 Lumina Ave S, Wrightsville Beach', 'Hanover Seaside Club, 601 Lumina Ave S, Wrightsville Beach')),
        (('T1 · natação → bike', 'T1 · swim → bike'), ('Wrightsville Beach Park, 3 Bob Sawyer Dr', 'Wrightsville Beach Park, 3 Bob Sawyer Dr')),
        (('T2 · bike → corrida', 'T2 · bike → run'), ('Cape Fear Community College Lot, 610 N Front St. O estacionamento é inclinado: cuidado ao pendurar a bike', 'Cape Fear Community College Lot, 610 N Front St. The lot slopes downhill: rack your bike carefully')),
        (('Chegada', 'Finish'), ('Water Street Park, Water St com Princess St', 'Water Street Park, Water St & Princess St')),
        (('Shuttle do atleta', 'Athlete shuttle'), ('N 3rd St com Brunswick St, uma quadra a leste da T2. Garagem mais próxima: 155 Brunswick St (fechada das 8h30 às 14h)', 'N 3rd St & Brunswick St, one block east of T2. Closest garage: 155 Brunswick St (closed 8:30 AM – 2:00 PM)')),
        (('Atendimento ao atleta', 'Athlete services'), ('813-415-1133 · northcarolina70.3@ironman.com', '813-415-1133 · northcarolina70.3@ironman.com')),
    ]))
    a('<div class="maps">' + mapa('mapa-centro.jpg', 'Mapa do centro de Wilmington', 'Downtown Wilmington map',
                                  'Centro: T2, shuttle, Aloft e chegada', 'Downtown: T2, shuttle, Aloft and finish')
      + mapa('mapa-t1.jpg', 'Mapa da T1', 'T1 map', 'T1 · Wrightsville Beach', 'T1 · Wrightsville Beach')
      + mapa('mapa-t2.jpg', 'Mapa da T2', 'T2 map', 'T2 · entrada da bike e saída da corrida', 'T2 · bike in and run out') + '</div>')
    a('<h3>' + L('As três sacolas', 'The three bags') + '</h3>')
    a('<div class="bags">'
      f'<div class="bag"><img src="img/sacola-azul.png" alt="" loading="lazy"><b>{L("Azul · bike", "Blue · bike")}</b><p>{L("Fica no seu rack na T1. Na saída da água, tudo de natação vai para dentro dela: wetsuit, touca, óculos. Amarre bem. Ela é levada para a T2.", "Stays at your rack in T1. After the swim, all swim gear goes inside: wetsuit, cap, goggles. Tie it tight. It is taken to T2.")}</p></div>'
      f'<div class="bag"><img src="img/sacola-vermelha.png" alt="" loading="lazy"><b>{L("Vermelha · corrida", "Red · run")}</b><p>{L("Entregue na sexta, na T2, até as 16h. No sábado ninguém entra na T2, então ela vai pronta e completa.", "Dropped at T2 on Friday by 4:00 PM. Nobody gets into T2 on Saturday, so it goes in ready and complete.")}</p></div>'
      f'<div class="bag"><img src="img/sacola-branca.png" alt="" loading="lazy"><b>{L("Branca · manhã", "White · morning")}</b><p>{L("Deixe na largada da natação com o que você quer na chegada. Retirada no Water Street Park. Nada de valor e nada que não caiba nela.", "Drop it at the swim start with what you want at the finish. Pick it up at Water Street Park. Nothing valuable and nothing that does not fit inside.")}</p></div>'
      '</div>')
    a('<h3>' + L('A manhã, passo a passo', 'The morning, step by step') + '</h3>')
    a(steps([
        ('Acordar com tempo. Café da manhã que você já usou nos longões, cerca de 3 horas antes da sua largada real.', 'Wake up with time to spare. A breakfast you have already used before long sessions, about 3 hours before your actual start.'),
        (f'{tm("04:30")}: encontro do time no ponto do shuttle (N 3rd com Brunswick). Pulseira, chip e touca com você, os três. O último shuttle sai às 5h15.', f'{tm("04:30")}: team meets at the shuttle stop (N 3rd & Brunswick). Wristband, chip and cap with you, all three. The last shuttle leaves at 5:15 AM.'),
        ('Na T1: a bike está lá desde sexta. Calibrar pneus, garrafas e nutrição na bike, câmbio na marcha de saída, ciclocomputador ligado. Capacete, sapatilha e óculos ao lado da bike, nunca presos nela. A transição fecha às 6h25.', 'At T1: your bike has been there since Friday. Pump tires, bottles and nutrition on the bike, gear set for the start, bike computer on. Helmet, shoes and glasses next to the bike, never clipped to it. Transition closes at 6:25 AM.'),
        (f'{tm("05:45")}: encontro na T1 e shuttle juntos até a largada. Todo mundo embarcado até 6h30. Também dá para ir a pé, {U("2,3 km", "1.42 mi")}, longe da pista.', f'{tm("05:45")}: meet at T1 and take the shuttle together to the start. Everyone on board by 6:30 AM. You can also walk {U("2.3 km", "1.42 mi")}, off the road.'),
        ('Na largada: sacola branca no local indicado, banheiro, aquecimento fora da água (5 a 10 minutos de mobilidade de ombro e caminhada rápida).', 'At the start: white bag at the drop area, bathroom, warm-up out of the water (5 to 10 minutes of shoulder mobility and brisk walking).'),
        ('Corral pelo seu tempo previsto de natação. Seu tempo começa quando você cruza o tapete.', 'Seed yourself by expected swim time. Your race time starts when you cross the mat.'),
    ]))
    a(box('warn', 'Ninguém entra na água antes da largada', 'Nobody gets in the water before the start',
          'Por causa da correnteza da maré, quem tentar nadar antes da largada de sábado é desclassificado. Em 2026 não existe nado oficial de reconhecimento. Aquecimento é fora da água.',
          'Because of the tidal currents, anyone who tries to swim before Saturday’s start is disqualified. There is no official practice swim in 2026. Warm up out of the water.'))
    a(box('', 'O que não pode faltar em cada ponto', 'What you must have at each point',
          'Na transição: pulseira, touca, chip no tornozelo esquerdo. Não use o número na natação. Na bike: adesivo do quadro visível dos dois lados, adesivo do capacete na frente, capacete afivelado sempre que tocar na bike. Na corrida: número na frente do corpo. Sem fones em etapa nenhuma.',
          'In transition: wristband, cap, chip on your left ankle. No bib on the swim. On the bike: frame sticker visible on both sides, helmet sticker on the front, helmet buckled whenever you touch the bike. On the run: bib on the front. No headphones at any point.'))
    a('</div></section>\n')

    # 04 natacao
    a('<section id="natacao"><div class="in">')
    a(sec_head('04', f'Natação · {U("1,9 km", "1.2 mi")}', f'Swim · {U("1.9 km", "1.2 mi")}', 'A água desperta', 'The water wakes you up',
               'Ponto a ponto no Banks Channel, um canal de água salgada ligado à Intracoastal, não o mar aberto. A maré enchente empurra a favor: é uma natação rápida. Larga no Hanover Seaside Club e chega perto do Seapath Yacht Club.',
               'Point-to-point in Banks Channel, a saltwater channel connected to the Intracoastal Waterway, not the open ocean. The incoming tide pushes you along: it is a fast swim. It starts at Hanover Seaside Club and finishes near Seapath Yacht Club.'))
    a(kv([
        (('Formato', 'Format'), ('Rolling start por tempo previsto, grupos pequenos a cada poucos segundos', 'Rolling start by expected time, small groups every few seconds')),
        (('Percurso', 'Course'), ('Siga a linha de boias de visada. As boias de curva são vermelhas', 'Follow the line of sighting buoys. Turn buoys are red')),
        (('Água', 'Water'), (f'Em 2025 ficou entre {C("19 e 22 °C", "66 and 72 °F")}. Wetsuit liberado até {C("24,5 °C", "76.1 °F")}. A temperatura oficial sai na manhã da prova', f'In 2025 it was {C("19 to 22 °C", "66 to 72 °F")}. Wetsuit legal up to {C("24.5 °C", "76.1 °F")}. The official temperature is announced race morning')),
        (('Saída da água', 'Swim exit'), (f'Escada com voluntários e strippers para tirar o wetsuit. Depois, corrida de {U("~450 m", "~500 yd")} até a T1', f'Stairs with volunteers and wetsuit strippers. Then a {U("~450 m", "~500 yd")} run to T1')),
        (('Proibido', 'Not allowed'), ('Nadadeira, palmar, luva, boia, snorkel. Touca oficial por cima de qualquer outra', 'Fins, paddles, gloves, pull buoys, snorkels. The official cap goes over any other cap')),
    ]))
    a('<h3>' + L('Como nadar North Carolina', 'How to swim North Carolina') + '</h3>')
    a(bullets([
        ('A água fria assusta nos primeiros segundos. É normal. Controle a respiração e deixe o corpo entender. Em um ou dois minutos ele se adapta e flui.', 'The cold water is a shock for the first few seconds. That is normal. Control your breathing and let your body catch up. Within a minute or two it adapts and flows.'),
        ('Saída controlada. Sem sprint nos primeiros 200 m. A maré vai te dar velocidade de qualquer jeito.', 'Controlled start. No sprint in the first 200 m. The tide will give you speed anyway.'),
        ('Cole na linha de boias e use o vácuo de quem nada no seu ritmo. Na natação, nadar atrás é permitido e economiza energia.', 'Stay close to the buoy line and draft off swimmers at your pace. Drafting is legal in the swim and saves energy.'),
        ('Sighting calmo, a cada 8 a 10 braçadas. A correnteza desvia; corrigir demais custa mais que o desvio.', 'Calm sighting every 8 to 10 strokes. The current pushes you off line; over-correcting costs more than the drift.'),
        ('Nos últimos 5 minutos, pernada mais ativa para mandar sangue para as pernas antes da escada.', 'In the last 5 minutes, kick a bit more to send blood to your legs before the stairs.'),
        ('Saia da água fresco. Se a natação tirou algo de você, você nadou a natação de outra pessoa.', 'Come out of the water fresh. If the swim took something out of you, you swam someone else’s race.'),
    ]))
    a(fotos(('hero-natacao-aerea.jpg', 'A natação vista de cima: a linha de atletas no Banks Channel', 'The swim from above: the line of swimmers in Banks Channel', 'wide'),
            ('foto-wetsuit.jpg', 'Banks Channel, manhã fria e água calma', 'Banks Channel, cold morning and calm water', 'tall'),
            ('foto-time-largada.jpg', 'O time na largada, Wrightsville Beach', 'The team at the swim start, Wrightsville Beach', 'tall')))
    a('<h3>' + L('T1 · da água para a bike', 'T1 · water to bike') + '</h3>')
    a(steps([
        ('Saída pela escada. Strippers ajudam a tirar o wetsuit, se você quiser.', 'Exit up the stairs. Strippers help you out of your wetsuit if you want.'),
        (f'Corrida de {U("~450 m", "~500 yd")} até a T1. O chip continua no tornozelo.', f'Run {U("~450 m", "~500 yd")} to T1. The chip stays on your ankle.'),
        ('No rack: tudo de natação dentro da sacola azul, amarrada e deixada no seu espaço.', 'At your rack: all swim gear into the blue bag, tied and left in your spot.'),
        ('Capacete afivelado antes de tirar a bike do rack. Óculos, sapatilha, nutrição no bolso.', 'Helmet buckled before you take the bike off the rack. Glasses, shoes, nutrition in your pocket.'),
        ('Respire. A T1 é o primeiro reset do dia: a natação acabou e não vai junto para a bike.', 'Breathe. T1 is the first reset of the day: the swim is over and it does not come with you on the bike.'),
        ('Empurre a bike até a linha de monte e só suba depois dela.', 'Push the bike to the mount line and only get on after it.'),
    ]))
    a('<div class="maps">' + mapa('mapa-natacao.jpg', 'Mapa da natação', 'Swim course map', 'Natação · percurso oficial', 'Swim · official course') + '</div>')
    a('</div></section>\n')

    # 05 bike
    a('<section id="bike" class="alt"><div class="in">')
    a(sec_head('05', f'Bike · {U("90 km", "56 mi")}', f'Bike · {U("90 km", "56 mi")}', 'O vento ensina paciência', 'The wind teaches patience',
               'Uma volta da praia até o centro, por estradas rurais. Plana e rápida, mas exposta. O vento de Wilmington não é o de Miami: é mais constante, sem rajadas, e cobra de quem acelera para manter a velocidade. Em 2025 ele veio de frente na ida para o norte e a favor na volta.',
               'One loop from the beach to downtown on rural roads. Flat and fast, but exposed. The Wilmington wind is not the Miami wind: it is steadier, without gusts, and it punishes anyone who pushes harder to hold speed. In 2025 it was a headwind going north and a tailwind coming back.'))
    a(fotos(('foto-time-bike.jpg', 'O time CMTeam no pedal', 'The CMTeam squad on the bike', 'wide')))
    a('<h3>' + L('O percurso por trecho', 'The course by section') + '</h3>')
    a(trechos([
        ('0 – 18', '0 – 11', 'Saída e cidade', 'Start and city',
         'Ponte levadiça de Wrightsville, Market St, College, MLK Pkwy, retorno da Hwy 133 e ponte Isabel Holmes. Muita gente junta.', 'Wrightsville drawbridge, Market St, College, MLK Pkwy, the Hwy 133 turnaround and the Isabel Holmes Bridge. Crowded.',
         'Conter', 'Hold back', 'Sentar, achar a potência-alvo, primeiro gole. Sem ultrapassar no impulso e respeitando as zonas sem aero e sem ultrapassagem.', 'Settle in, find your target power, first sip. No impulse passing, and respect the no-aero and no-passing zones.'),
        ('18 – 45', '11 – 28', 'Rodovia 421, ida', 'Hwy 421 northbound',
         'Retas longas para o norte. Em 2025, vento de frente. Posto 1 perto do km 23.', 'Long straights heading north. Headwind in 2025. Aid station 1 near mile 14.',
         'Sustentar', 'Sustain', 'Aero, constante, watts no alvo. Aceite a velocidade menor no vento: todo mundo perde a mesma coisa.', 'Aero, steady, watts on target. Accept the lower speed into the wind: everyone loses the same.'),
        ('45 – 68', '28 – 42', 'Laço do norte', 'Northern loop',
         'Estradas rurais: Union Chapel, Rivenbark, Porter, Brinson, Borough, Blueberry. Mais curvas. Posto 2 perto do km 53. Proibido ultrapassar da Porter com Brinson até a Hwy 210.', 'Rural roads: Union Chapel, Rivenbark, Porter, Brinson, Borough, Blueberry. More turns. Aid station 2 near mile 33. No passing from Porter/Brinson to Hwy 210.',
         'Alimentar', 'Fuel', 'Alimentação e hidratação em dia, atenção nas curvas e no piso. Aqui se prepara a corrida.', 'Stay on top of food and fluids, careful on turns and road surface. This is where you set up your run.'),
        ('68 – 88', '42 – 55', 'Rodovia 421, volta', 'Hwy 421 southbound',
         'De volta para o sul, em 2025 com vento a favor. Posto 3 perto do km 76, com corte às 13h.', 'Back south, with a tailwind in 2025. Aid station 3 near mile 47, cut-off at 1:00 PM.',
         'Segurar', 'Hold the floor', 'Com vento a favor, não pare de pedalar: segure o piso da potência. Também não acelere demais: a corrida vem aí.', 'With a tailwind, keep pedaling and hold the bottom of your power range. Do not overcook it either: the run is next.'),
        ('88 – 90', '55 – 56', 'Ponte e T2', 'Bridge and T2',
         'Ponte Isabel Holmes (sem aero, sem ultrapassar), centro de Wilmington, desmonte.', 'Isabel Holmes Bridge (no aero, no passing), downtown Wilmington, dismount.',
         'Preparar', 'Prepare', 'Últimos 10 minutos girando mais leve, último gole, soltar as pernas. A bike acabou; agora é outra prova.', 'Spin easier for the last 10 minutes, last sip, loosen your legs. The bike is over; now it is a different race.'),
    ]))
    a('<h3>' + L('Intensidade: IF de 0,80 a 0,82', 'Intensity: IF 0.80 to 0.82') + ' ' + tbc() + '</h3>')
    a(P('IF é a potência normalizada da etapa dividida pelo seu FTP. Entre 0,80 e 0,82 você pedala forte o bastante para fazer um bom tempo e controlado o bastante para correr os 21 km depois. O seu alvo individual vale mais que a referência do time.',
        'IF is your normalized power for the leg divided by your FTP. Between 0.80 and 0.82 you ride hard enough for a good split and controlled enough to run the 21 km afterward. Your individual target overrides the team reference.'))
    a(bullets([
        ('O alvo é média, não piso nem teto. Num percurso plano, a média sai fácil se você não brigar com o vento.', 'The target is an average, not a floor or a ceiling. On a flat course the average comes easily if you do not fight the wind.'),
        ('Nas pontes, o teto é 100% do FTP, a fronteira do A3. Passar disso numa rampa curta é a conta mais cara do dia.', 'On the bridges, the ceiling is 100% of FTP, the top of A3. Going over it on a short ramp is the most expensive bill of the day.'),
        ('Variabilidade baixa: VI até 1,05. Em percurso plano, VI alto é ego, não terreno.', 'Low variability: VI up to 1.05. On a flat course, a high VI is ego, not terrain.'),
        ('No vento contra, mesmos watts, menos velocidade. Quem aumenta os watts para manter a velocidade chega na corrida sem margem.', 'Into the wind: same watts, less speed. Raising watts to hold speed means starting the run with nothing left.'),
        ('Sem potenciômetro: FC como teto e PSE de 5 a 6 (de 0 a 10). FC é auditoria, não volante.', 'No power meter: heart rate as a ceiling and RPE of 5 to 6 (out of 10). Heart rate is an audit, not a steering wheel.'),
    ]))
    a(box('warn', 'Sem aero e sem ultrapassar', 'No aero, no passing',
          'Proibido ficar em posição aero e ultrapassar na ponte levadiça de Wrightsville Beach e na ponte Isabel Holmes. Proibido ultrapassar no retorno da Hwy 133 para a MLK Pkwy e da Porter Rd com Brinson Rd até a Hwy 210. Quem desrespeitar pode ser desclassificado.',
          'No aero position and no passing on the Wrightsville Beach drawbridge and the Isabel Holmes Bridge. No passing on the Hwy 133 turnaround onto MLK Pkwy, or from Porter Rd & Brinson Rd through Hwy 210. Violations can mean disqualification.'))
    a('<h3>' + L('Regras de bike que custam tempo', 'Bike rules that cost time') + '</h3>')
    rules = [
        ('Zona de vácuo: 12 m', 'Draft zone: 12 m', 'Seis bikes de distância entre a sua roda da frente e a traseira de quem vai à frente.', 'Six bike lengths between your front wheel and the rear wheel ahead.', 'blue', L('Azul · 2 min', 'Blue · 2 min')),
        ('Ultrapassagem em 25 s', 'Pass within 25 s', 'Entrou na zona, completa a passagem em 25 segundos, sempre pela esquerda, e volta para a direita.', 'Once in the zone, complete the pass in 25 seconds, always on the left, then move back right.', 'blue', L('Azul · 2 min', 'Blue · 2 min')),
        ('Foi ultrapassado', 'Being passed', 'Saia da zona na hora, ficando para trás. Repassar antes de sair dela é penalidade.', 'Drop back out of the zone immediately. Re-passing before you are out is a penalty.', 'yel', L('Amarelo · 30 s', 'Yellow · 30 s')),
        ('Lado direito', 'Keep right', 'Sempre à direita, em fila única. Lado a lado é bloqueio.', 'Always on the right, single file. Side by side is blocking.', 'yel', L('Amarelo · 30 s', 'Yellow · 30 s')),
        ('Lixo fora do posto', 'Littering', 'Embalagem, garrafa e até a pontinha do gel, só dentro da zona do posto.', 'Wrappers, bottles, even the gel tab: only inside the aid station zone.', 'blue', L('Azul · 2 min', 'Blue · 2 min')),
        ('Capacete', 'Helmet', 'Afivelado sempre que estiver com a bike, inclusive na transição.', 'Buckled whenever you have your bike, including in transition.', 'red', 'DSQ'),
        ('Garrafas', 'Bottles', 'Na frente, no máximo 2 litros somados. Atrás, no máximo 2 garrafas de 1 litro. Dentro do quadro não conta.', 'Front-mounted: 2 liters max combined. Rear: max 2 bottles of 1 liter. Inside the frame triangle does not count.', '', L('Ilegal', 'Illegal')),
        ('Três cartões azuis', 'Three blue cards', 'Desclassificação.', 'Disqualification.', 'red', 'DSQ'),
    ]
    a('<div class="rules">' + ''.join(
        f'<div class="rule"><b>{L(a1, a2)}</b><span>{L(b1, b2)}</span><span class="pen {c}">{d}</span></div>'
        for a1, a2, b1, b2, c, d in rules) + '</div>')
    a(P('Levou cartão? Pare na próxima tenda de penalidade, diga a cor do cartão, assine e cumpra o tempo. Não discuta com o árbitro. Não parar na tenda é desclassificação.',
        'Got a card? Stop at the next penalty tent, state the card color, sign in and serve the time. Do not argue with the referee. Skipping the tent means disqualification.', 'muted small'))
    a('<h3>' + L('Postos de apoio', 'Aid stations') + '</h3>')
    a(f'<div class="aid"><span>1 · {U("km 23", "mi 14")}</span><span>2 · {U("km 53", "mi 33")}</span><span>3 · {U("km 76", "mi 47")}</span></div>')
    a(P('Todos com banheiro. Oferecem água, Precision Fuel &amp; Hydration, Maurten Gel 100 e 100 CAF, Maurten Solid 160 e 160 C, barras e banana. Ninguém passa pelo posto em aero: mão no freio, olho no voluntário, aponte o que quer.',
        'All with toilets. They offer water, Precision Fuel &amp; Hydration, Maurten Gel 100 and 100 CAF, Maurten Solid 160 and 160 C, bars and bananas. Nobody rides through an aid station in aero: hands on the brakes, eyes on the volunteer, point at what you want.'))
    a(box('gold', 'Só o que você treinou', 'Only what you trained with',
          'O que está no posto é reposição, não plano. O seu plano de nutrição é individual e foi construído com o que você usou nos longões. Produto novo no dia da prova é o jeito mais rápido de transformar um bom pedal numa corrida andando.',
          'What is at the aid station is backup, not the plan. Your nutrition plan is individual and built from what you used on long sessions. A new product on race day is the fastest way to turn a good ride into a walk.'))
    a('<h3>' + L('T2 · da bike para a corrida', 'T2 · bike to run') + '</h3>')
    a(steps([
        ('Desmonte antes da linha. Empurre a bike até o seu rack e pendure antes de tirar o capacete. O estacionamento é inclinado: pendure com cuidado.', 'Dismount before the line. Push the bike to your rack and hang it before taking off your helmet. The lot slopes: rack carefully.'),
        ('Sacola vermelha: material de bike dentro, tênis, boné e cinto com o número virado para a frente.', 'Red bag: bike gear in, then shoes, cap and race belt with the bib facing forward.'),
        ('Protetor solar disponível na T2.', 'Sunscreen is available in T2.'),
        ('Segundo reset do dia. A bike acabou, boa ou ruim. O que vem agora é outra prova.', 'Second reset of the day. The bike is over, good or bad. What comes next is a different race.'),
    ]))
    a('<div class="maps">' + mapa('mapa-bike.jpg', 'Mapa da bike', 'Bike course map', 'Bike · percurso oficial e postos', 'Bike · official course and aid stations')
      + mapa('bike-direcoes.jpg', 'Altimetria e direções da bike', 'Bike elevation and directions', 'Bike · altimetria e direções', 'Bike · elevation and directions') + '</div>')
    a('</div></section>\n')

    # 06 corrida
    a('<section id="corrida"><div class="in">')
    a(sec_head('06', f'Corrida · {U("21,1 km", "13.1 mi")}', f'Run · {U("21.1 km", "13.1 mi")}', 'O sol lembra quem você é', 'The sun reminds you who you are',
               'Novo em 2026: sai da T2, desce pela Front St e faz duas voltas no Greenfield Lake, entre árvores com musgo e quase toda na sombra. Depois volta pela Front St até a chegada no Water Street Park. Quase plana, com leves ondulações em volta do lago.',
               'New for 2026: out of T2, south on Front St and two laps around Greenfield Lake, under moss-draped trees and mostly in the shade. Then back up Front St to the finish at Water Street Park. Nearly flat, with gentle rollers around the lake.'))
    a(trechos([
        ('0 – 4', '0 – 2.5', 'Saída e Front St', 'Start and Front St',
         'T2, Hanover St, calçadão do rio, Water St e Front St para o sul. Torcida forte.', 'T2, Hanover St, the riverfront boardwalk, Water St and Front St heading south. Big crowds.',
         'Conter', 'Hold back', 'As pernas ainda são de ciclista. Passada curta, cadência alta, ritmo abaixo do alvo nos primeiros 15 a 20 minutos.', 'Your legs are still bike legs. Short stride, high cadence, below target pace for the first 15 to 20 minutes.'),
        ('4 – 11,2', '2.5 – 7', 'Lago, 1ª volta', 'Lake, lap 1',
         'Lake Shore Dr e o caminho em volta do Greenfield Lake. Sombra, leves ondulações.', 'Lake Shore Dr and the path around Greenfield Lake. Shade, gentle rollers.',
         'Assentar', 'Settle', 'Aqui o corpo encontra o ritmo de corrida. Trave no pace-alvo e confira a sensação. Ritmo, não ego.', 'This is where your body finds its running rhythm. Lock onto target pace and check in with yourself. Rhythm, not ego.'),
        ('11,2 – 18,2', '7 – 11.3', 'Lago, 2ª volta', 'Lake, lap 2',
         'Pulseira na entrada da segunda volta. Corte às 15h20 no início dela e às 16h20 na saída.', 'Wristband at the start of lap 2. Cut-offs at 3:20 PM at its start and 4:20 PM at its end.',
         'Sustentar', 'Sustain', 'Mesma volta, mesmo ritmo. Caminhada curta nos postos, se precisar, faz parte do plano. Mente ocupada com o próximo posto.', 'Same lap, same pace. A short walk through aid stations, if needed, is part of the plan. Keep your mind on the next station.'),
        ('18,2 – 21,1', '11.3 – 13.1', 'Front St e chegada', 'Front St and finish',
         'Saída do lago, Front St para o norte e Water Street Park.', 'Out of the lake, north on Front St to Water Street Park.',
         'Liberar', 'Let it go', 'É aqui que a prova é decidida. Postura alta, respiração, o que sobrou. Na reta final, nada guardado.', 'This is where the race is decided. Tall posture, breathing, whatever is left. In the final stretch, hold nothing back.'),
    ]))
    a('<h3>' + L('Como correr North Carolina', 'How to run North Carolina') + '</h3>')
    a(bullets([
        ('Divida a meia em três blocos: conservar, assentar, levar para casa.', 'Break the half into three blocks: conserve, settle, bring it home.'),
        ('A perna pesada dos primeiros quilômetros não é diagnóstico. É a fisiologia trocando de tarefa.', 'Heavy legs in the first kilometers are not a diagnosis. It is your physiology switching tasks.'),
        ('Na sombra do lago a sensação de esforço cai e o ritmo sobe sem você perceber. Corra pela régua, não pela sensação.', 'In the shade of the lake, perceived effort drops and pace creeps up without you noticing. Run by the numbers, not by feel.'),
        ('Da metade em diante, se precisar, caminhe 20, 30 ou até 40 segundos nos postos. Com propósito: beber de verdade, gelo, esponja. Não é fraqueza, é inteligência.', 'From halfway on, if you need to, walk 20, 30 or even 40 seconds through aid stations. With purpose: drink properly, ice, sponge. It is not weakness, it is intelligence.'),
        ('Calor leve não é desculpa para pular a hidratação. Hidratação por plano, não por sede.', 'Mild heat is no excuse to skip fluids. Drink to plan, not to thirst.'),
        ('Reta final: a torcida puxa. Aproveite a energia, mas mantenha a forma.', 'Final stretch: the crowd pulls you. Use the energy, but keep your form.'),
    ]))
    a('<h3>' + L('Postos de apoio', 'Aid stations') + '</h3>')
    aid_km = ['0,9', '2,7', '4,2', '6,1', '8,0', '10,0', '11,3', '13,2', '15,1', '17,1', '18,2', '19,8']
    aid_mi = ['0.59', '1.7', '2.6', '3.8', '5', '6.2', '7', '8.2', '9.4', '10.6', '11.3', '12.3']
    a('<div class="aid">' + ''.join(f'<span>{U("km " + k, "mi " + m)}</span>' for k, m in zip(aid_km, aid_mi)) + '</div>')
    a(P('Doze postos, todos com banheiro: água, Precision Fuel &amp; Hydration, Coca-Cola, Maurten Gel 100 e 100 CAF, Maurten Solid 160 e 160 C, barras, chips, pretzel, banana e laranja. O primeiro posto é reforçado em hidratação. Descarte só dentro da zona do posto.',
        'Twelve stations, all with toilets: water, Precision Fuel &amp; Hydration, cola, Maurten Gel 100 and 100 CAF, Maurten Solid 160 and 160 C, bars, chips, pretzels, bananas and oranges. The first station is heavy on fluids. Discard only inside the aid station zone.'))
    a('<h3>' + L('Regras de corrida', 'Run rules') + '</h3>')
    a(bullets([
        ('Número na frente, visível o tempo todo. Dobrar, cortar ou esconder o número é desclassificação.', 'Bib on the front, visible at all times. Folding, cutting or hiding it means disqualification.'),
        ('Sem torso nu. Zíper pode ficar aberto, mas preso embaixo.', 'No bare torso. The zipper can be open, but connected at the bottom.'),
        ('Ninguém de fora corre com você, nem por 50 metros. Atleta que ainda está na prova pode.', 'No outsiders running with you, not even for 50 meters. Athletes still racing can.'),
        ('Ninguém cruza a chegada com você: nem filho, nem cônjuge, nem cachorro. É desclassificação automática.', 'Nobody crosses the finish line with you: not your kid, not your partner, not your dog. It is an automatic DSQ.'),
        ('Na corrida não existe tenda: a penalidade se cumpre na hora, no local.', 'There is no penalty tent on the run: penalties are served on the spot.'),
    ]))
    a('<div class="maps">' + mapa('mapa-corrida.jpg', 'Mapa da corrida', 'Run course map', 'Corrida · percurso oficial (01/09/2026)', 'Run · official course (Sept 1, 2026)')
      + mapa('corrida-direcoes.jpg', 'Altimetria e direções da corrida', 'Run elevation and directions', 'Corrida · altimetria e direções', 'Run · elevation and directions') + '</div>')
    a('<h3>' + L('Onde o time torce', 'Where the team cheers') + ' ' + tbc() + '</h3>')
    a(P('A Front St é o melhor ponto: os atletas passam por ela na ida (por volta do km 2) e na volta (por volta do km 19). A segunda zona fica na chegada, no Water Street Park.',
        'Front St is the best spot: athletes pass it on the way out (around mile 1.5) and on the way back (around mile 12). The second zone is the finish at Water Street Park.'))
    a(fotos(('foto-chegada-2022.jpg', 'Medalhas no peito, North Carolina 2022', 'Medals on, North Carolina 2022', 'wide'),
            ('foto-familia.jpg', 'Quem torce também faz parte da prova', 'The people cheering are part of the race too', 'wide')))
    a('</div></section>\n')

    # 07 clima
    a('<section id="clima" class="alt"><div class="in">')
    a(sec_head('07', 'Clima', 'Weather', 'Começa fria, termina quente', 'Starts cold, ends warm',
               'Médias históricas de meados de outubro em Wilmington. A previsão real entra aqui na semana da prova.',
               'Historical mid-October averages for Wilmington. The real forecast goes here during race week.'))
    a('<div class="wx">'
      f'<div><b>{L("Largada", "Start")}</b><div class="t">{C("13 °C", "56 °F")}</div><p>{L("Escuro até perto das 7h15. Casaco velho ou na sacola branca.", "Dark until about 7:15 AM. Old sweatshirt, or put it in the white bag.")}</p></div>'
      f'<div><b>{L("Água", "Water")}</b><div class="t">{C("20–22 °C", "68–72 °F")}</div><p>{L("Wetsuit liberado provável. Confirmação na manhã da prova.", "Wetsuit-legal likely. Confirmed race morning.")}</p></div>'
      f'<div><b>Bike</b><div class="t">{C("15–21 °C", "59–70 °F")}</div><p>{L("Vento constante. Manguito ou colete para os primeiros quilômetros, se estiver frio.", "Steady wind. Arm warmers or a vest for the first miles if it is cold.")}</p></div>'
      f'<div><b>{L("Corrida", "Run")}</b><div class="t">{C("24 °C", "75 °F")}</div><p>{L("Sol, sombra no lago. Gelo e água na cabeça antes de sentir calor.", "Sun, shade at the lake. Ice and water on your head before you feel hot.")}</p></div>'
      '</div>')
    a(box('warn', 'Frio na largada, calor na corrida', 'Cold start, warm run',
          'É a combinação clássica de erro: o atleta sai da bike com pouca água no corpo porque não sentiu sede, e a corrida cobra a diferença. Comece a beber desde o primeiro posto da bike.',
          'This is the classic trap: athletes get off the bike under-hydrated because they never felt thirsty, and the run makes them pay. Start drinking from the first bike aid station.'))
    a('</div></section>\n')

    # 08 race week
    a('<section id="semana"><div class="in">')
    a(sec_head('08', 'As últimas semanas', 'The final weeks', 'Afinar, não testar', 'Sharpen, do not test',
               'Agora não existe mais o que ganhar em forma, só em clareza. O corpo já sabe o caminho. A mente, se estiver calma, vai apenas seguir.',
               'There is no more fitness to gain now, only clarity. Your body already knows the way. If your mind is calm, it will simply follow.'))
    a('<div class="cols"><div>')
    a('<h3>' + L('Treino', 'Training') + '</h3>')
    a(bullets([
        ('Respeite o polimento. Na última semana não se ganha condicionamento.', 'Respect the taper. You gain no fitness in the final week.'),
        ('Ensaio geral de bike e corrida com o material de prova.', 'Dress rehearsal ride and run with your race gear.'),
        ('Conheça seus alvos: zonas, watts, FC e PSE.', 'Know your targets: zones, watts, heart rate and RPE.'),
        ('Mais importante estar descansado do que afiado. Não pule o dia de folga.', 'Being rested matters more than being sharp. Do not skip your day off.'),
    ]))
    a('<h3>' + L('Race week', 'Race week') + '</h3>')
    a(bullets([
        ('Sono como prioridade: 7 a 8 horas por noite.', 'Sleep is the priority: 7 to 8 hours a night.'),
        ('Hidratação em dia, além do que você perde nos treinos.', 'Stay hydrated, on top of what you lose in training.'),
        ('Use nos treinos os produtos que vai usar na prova. É treino de intestino.', 'Use the products you will race with in training. It is gut training.'),
        ('Comida normal, sem novidade. O máximo de tempo possível com os pés para cima.', 'Normal food, nothing new. As much time off your feet as possible.'),
    ]))
    a('</div><div>')
    a('<h3>' + L('Cabeça', 'Mind') + '</h3>')
    a(bullets([
        ('Reduza a pressão de fora, do jeito que der.', 'Reduce outside pressure as best you can.'),
        ('Foque no que você controla: atitude e plano de combustível.', 'Focus on what you control: attitude and fueling plan.'),
        ('Visualize: como é um grande dia, e como você responde se algo sair diferente.', 'Visualize: what a great day looks like, and how you respond if something goes differently.'),
        ('Separe metas (100% sob seu controle) de alvos (números: zonas, watts, FC, PSE).', 'Separate goals (100% in your control) from targets (numbers: zones, watts, HR, RPE).'),
        ('Menos comparação, mais presença. Menos ansiedade, mais método.', 'Less comparison, more presence. Less anxiety, more method.'),
    ]))
    a('<h3>' + L('Véspera', 'Day before') + '</h3>')
    a(bullets([
        ('Carregue os eletrônicos: relógio, ciclocomputador, potenciômetro.', 'Charge your electronics: watch, bike computer, power meter.'),
        ('Separe o material da manhã e confirme como você chega ao shuttle.', 'Lay out your morning gear and confirm how you get to the shuttle.'),
        ('Jantar cedo, cama cedo, vários alarmes.', 'Early dinner, early to bed, several alarms.'),
    ]))
    a('</div></div>')
    a('</div></section>\n')

    # 09 checklist
    a('<section id="checklist" class="alt"><div class="in">')
    a(sec_head('09', 'Checklist', 'Checklist', 'O que vai para a mala', 'What goes in the bag',
               'Marque conforme separa. Equipamento novo na prova é experimento, e prova não é lugar de experimento.',
               'Tick items as you pack. New gear on race day is an experiment, and race day is no place for experiments.'))
    a(checklist_html())
    a('</div></section>\n')

    # 10 planner
    a('<section id="planner"><div class="in">')
    a(sec_head('10', 'Race-day planner', 'Race-day planner', 'O seu dia, por escrito', 'Your day, in writing',
               'O planejamento é a ferramenta que organiza todos os passos para alcançar o objetivo. Preencha com os seus números e horários.',
               'Planning is the tool that organizes every step toward your goal. Fill it in with your own numbers and times.'))
    a(planner_html())
    a('</div></section>\n')

    # 11 regras de ouro
    a('<section id="regras" class="darkband"><div class="in">')
    a(sec_head('11', 'Regras de ouro', 'Golden rules', 'Para levar na cabeça', 'Keep these in your head'))
    gold = [
        ('Ninguém entra na água antes da largada. Aquecimento é seco.', 'Nobody gets in the water before the start. Warm up dry.'),
        ('A sacola vermelha vai pronta na sexta. No sábado não existe T2.', 'The red bag goes in ready on Friday. On Saturday, T2 does not exist for you.'),
        ('A maré é aliada. Saia da água fresco.', 'The tide is your ally. Come out of the water fresh.'),
        ('Bike em IF de 0,80 a 0,82. Nas pontes, teto de 100% do FTP.', 'Bike at IF 0.80 to 0.82. On the bridges, a ceiling of 100% FTP.'),
        ('Pontes: sem aero, sem ultrapassar. Respeitar as zonas faz parte do plano.', 'Bridges: no aero, no passing. Respecting the zones is part of the plan.'),
        ('Vento contra: mesmos watts. Vento a favor: segure o piso.', 'Headwind: same watts. Tailwind: hold the floor.'),
        ('Os últimos 10 minutos de bike preparam a corrida.', 'The last 10 minutes of the bike set up the run.'),
        ('Na primeira volta do lago, paciência. Na segunda, decisão.', 'Lap one of the lake is patience. Lap two is decision.'),
        ('Caminhar nos postos com propósito é estratégia, não fraqueza.', 'Walking aid stations with purpose is strategy, not weakness.'),
        ('Só o que você treinou: produto, ritmo, equipamento.', 'Only what you trained with: product, pace, gear.'),
    ]
    a('<ol class="gold-rules">' + ''.join(f'<li>{L(p, e)}</li>' for p, e in gold) + '</ol>')
    a('<div class="mantra">'
      + P('Que o frio me desperte.', 'May the cold wake me up.')
      + P('Que o vento me ensine paciência.', 'May the wind teach me patience.')
      + P('Que o sol me lembre quem sou.', 'May the sun remind me who I am.')
      + P('E que, no silêncio do esforço, eu encontre minha força.', 'And in the silence of effort, may I find my strength.')
      + '</div>')
    a('<div class="final" style="margin-top:36px">')
    a(f'<h3 style="color:#fff">{L("Palavra final", "Final word")}</h3>')
    a(P('Este guia foi construído a partir do que cada um de vocês fez nas últimas semanas: zonas, testes, resposta ao treino e provas anteriores. O plano de prova é a última página de um ciclo inteiro, e é o ciclo que faz a diferença no sábado.',
        'This guide was built from what each of you did over the last weeks: zones, tests, response to training and past races. The race plan is the last page of a whole cycle, and it is the cycle that makes the difference on Saturday.'))
    a(P('Você compete como você treinou. Agora é respeitar o percurso, controlar o esforço e deixar o treino aparecer.',
        'You race the way you trained. Now it is about respecting the course, controlling the effort and letting your training show.'))
    a('</div>')
    a('<div class="photos"><img src="img/time-bikes.jpg" alt="Time CMTeam com as bikes em Wilmington" loading="lazy"><img src="img/time-expo.jpg" alt="Time CMTeam no IRONMAN 70.3 North Carolina" loading="lazy"></div>')
    a('<div class="motto">bePatient <span>|</span> beHumble <span>|</span> beStrong</div>')
    a('</div></section>\n')

    a('<footer><div class="in">'
      f'<div><b>CMTeam</b> · cmteam.us | @cmteam</div>'
      f'<div>{L("Material exclusivo dos atletas CMTeam. Não compartilhe este link.", "For CMTeam athletes only. Please do not share this link.")}</div>'
      f'<div>{L("Fontes: Athlete Guide e Event Schedule oficiais de 2026 (atualizados em 16/09/2026) e mapas oficiais. Se o briefing mudar algo, o briefing vence.", "Sources: official 2026 Athlete Guide and Event Schedule (updated Sept 16, 2026) and official course maps. If the briefing changes anything, the briefing wins.")}</div>'
      f'<div>{L("Mapas dos percursos e das transições © World Triathlon Corporation.", "Course and transition maps © World Triathlon Corporation.")} · {VERSAO}</div>'
      '</div></footer>'
      '<a href="#" class="totop" aria-label="Topo">↑</a>\n')
    a(f'<script>{JS}</script>\n</body>\n</html>\n')
    return ''.join(H)

if __name__ == '__main__':
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    s = build()
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(s)
    print('ok', OUT, len(s) // 1024, 'KB')
