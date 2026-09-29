# -*- coding: utf-8 -*-
import re, json
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'index.html'); DST=os.path.join(ROOT,'en','index.html')
s=open(SRC,encoding='utf-8').read()

TEXT={
'CMTeam — Triathlon, Corrida e Endurance':'CMTeam — Triathlon, Running & Endurance Coaching',
'Grátis':'Free',
'Baixe o e-book':'Download the e-book',
', de San Palma':', by San Palma (in Portuguese)',
'Baixar agora →':'Download now →',
'Manifesto':'Manifesto','Método ECO':'ECO Method','Treinadores':'Coaches','Livros':'Books','Treinos':'Training',
'Fale conosco':'Contact us',
'Triathlon · Corrida · Endurance':'Triathlon · Running · Endurance',
'Aqui, cada treino tem motivo.':'Every session has a reason.',
'Assessoria especializada em triathlon, corrida e esportes de endurance. Metodologia própria, acompanhamento próximo e visão de longo prazo — do iniciante ao competitivo.':'Triathlon, running and endurance coaching. Our own methodology, close guidance and a long-term vision — from first-timers to competitive athletes.',
'Falar no WhatsApp':'Message us on WhatsApp','Conheça o método':'Discover the method',
'anos de CMTeam':'years of CMTeam','atletas treinados':'athletes coached','países':'countries','continentes':'continents',
'Nossos atletas em':'Our athletes at',
'Ironman Itália — Emilia-Romagna':'Ironman Italy — Emilia-Romagna','Maratona de Buenos Aires':'Buenos Aires Marathon',
'O Manifesto CMTeam':'The CMTeam Manifesto',
'Não somos um time feito de resultados. Somos um time feito de processos.':'We are not a team built on results. We are a team built on process.',
'A CMTeam nasceu da vontade de construir algo diferente: um espaço onde a performance é consequência, não cobrança. Onde a paciência é tão valorizada quanto a intensidade, e onde cada atleta aprende que evoluir é um caminho, não uma meta de calendário.':'CMTeam was born from the desire to build something different: a place where performance is a consequence, not a demand. Where patience is valued as much as intensity, and where every athlete learns that progress is a path, not a date on the calendar.',
'Treinamos com ciência, mas também com alma. Com planilha, mas com propósito. Com técnica, mas com verdade. Acreditamos que disciplina é mais poderosa do que motivação, e que ser consistente é a forma mais pura de ser forte.':'We train with science, but also with soul. With a plan, but with purpose. With technique, but with honesty. We believe discipline is more powerful than motivation, and that consistency is the purest form of strength.',
'Nosso objetivo não é ser o melhor time. É ser o time que não desiste de ser melhor.':'Our goal is not to be the best team. It is to be the team that never stops trying to be better.',
'Nada grande nasce apressado. A consistência vale mais do que o talento, e cada adaptação precisa de tempo para se tornar parte de quem você é. Ser paciente é saber esperar enquanto se constrói.':'Nothing great is born in a hurry. Consistency is worth more than talent, and every adaptation needs time to become part of who you are. Being patient means waiting while you build.',
'O aprendizado nunca termina. Humildade não é se diminuir: é ter a grandeza de continuar curioso, de ouvir, de respeitar — e entender que o sucesso individual só tem valor quando soma ao coletivo.':'Learning never ends. Humility is not making yourself smaller: it is having the greatness to stay curious, to listen, to respect — and to understand that individual success only matters when it adds to the team.',
'Ser forte não é vencer sempre. É continuar quando não se tem mais certeza. A força verdadeira não se mede no FTP, no pace ou no ranking: se mede na capacidade de recomeçar.':'Being strong is not winning every time. It is carrying on when you are no longer sure. True strength is not measured in FTP, pace or rankings: it is measured by the ability to start again.',
'Metodologia própria':'Our own methodology',
'O ECO parte de um princípio claro: o corpo evolui melhor quando o esforço é bem distribuído, respeita o momento do atleta e evita o desgaste silencioso causado por excesso de intensidade mal aplicada.':'ECO starts from a clear principle: the body improves best when effort is well distributed, respects where the athlete is right now, and avoids the silent wear caused by too much poorly applied intensity.',
'Base aeróbia sólida':'A solid aerobic base','A base é prioridade. É ela que sustenta toda a evolução.':'The base comes first. It supports every step of progress.',
'Intensidade estratégica':'Strategic intensity','Intensidade usada de forma estratégica, não emocional.':'Intensity used strategically, not emotionally.',
'Ciclos com lógica':'Cycles with logic','Ciclos organizados para construir, consolidar e realizar.':'Cycles organized to build, consolidate and perform.',
'Carga da vida real':'Real-life load','Carga ajustada ao treino, ao trabalho, à família e à recuperação.':'Load adjusted to training, work, family and recovery.',
'Tudo é individualizado, respeitando os princípios do treinamento: individualidade biológica, adaptação, relação volume × intensidade, sobrecarga e especificidade.':'Everything is individualized, following the principles of training: biological individuality, adaptation, volume × intensity, overload and specificity.',
'Como trabalhamos':'How we work','Planejamento claro. Acompanhamento de perto.':'Clear planning. Close follow-up.',
'Todos os treinos são prescritos e acompanhados pelo TrainingPeaks. O feedback pós-treino faz parte ativa do processo e orienta as decisões semana a semana.':'Every session is prescribed and tracked on TrainingPeaks. Post-workout feedback is an active part of the process and guides our decisions week by week.',
'Planejamento semanal claro e organizado':'Clear, organized weekly planning','Treinos explicados, com objetivo e orientação prática':'Every workout explained, with a purpose and practical guidance','Acompanhamento contínuo e ajustes frequentes':'Ongoing follow-up and frequent adjustments','Feedback direto dentro do aplicativo':'Direct feedback inside the app',
'Modalidades':'Disciplines','Do primeiro 5 km ao Ironman.':'From your first 5K to Ironman.',
'Do sprint ao Ironman, com natação, bike e corrida integradas num só plano.':'From sprint to Ironman, with swim, bike and run integrated in one plan.',
'Corrida de rua':'Road running','Do 5 km à maratona, com foco em ritmo, economia e consistência.':'From 5K to the marathon, focused on pace, economy and consistency.',
'Trail e montanha':'Trail & mountain','Subidas, descidas e terreno técnico, com preparação específica para cada prova.':'Climbs, descents and technical terrain, with race-specific preparation.',
'Ultramaratona':'Ultramarathon','Longas distâncias com estratégia de ritmo, nutrição e resistência mental.':'Long distances with pacing strategy, nutrition and mental endurance.',
'Duas trajetórias. Uma convicção.':'Two journeys. One conviction.',
'Por trás da CMTeam existem duas trajetórias construídas no esporte de alto rendimento, guiadas pela mesma ideia: performance só faz sentido quando vem acompanhada de processo, consciência e longevidade.':'Behind CMTeam are two journeys built in high-performance sport, guided by the same idea: performance only makes sense when it comes with process, awareness and longevity.',
'CMTeam é Carla Moreno Team.':'CMTeam stands for Carla Moreno Team.',
'O time nasceu de duas pessoas, San e Carla, e de um grupo que acreditou que a ciência e a alma podem caminhar juntas.':'The team was born from two people, San and Carla, and from a group that believed science and soul can go hand in hand.',
'Co-fundador e Head Coach':'Co-founder & Head Coach',
'Treinador desde 2003 e atleta há mais de 30 anos, com certificações USA Triathlon, IRONMAN e TrainingPeaks. Conduziu Carla Moreno em sua fase de supremacia no triathlon nacional — anos vencendo as principais provas olímpicas do Brasil e mais de seis temporadas invicta em Miami. Já classificou atletas para mundiais ITU, Ironman 70.3 e Ironman 140.6 e foi treinador da delegação brasileira em competições internacionais. Especialista em Fisiologia do Esforço e Prescrição do Treinamento, é o criador do Método ECO.':'Coaching since 2003 and an athlete for more than 30 years, certified by USA Triathlon, IRONMAN and TrainingPeaks. He coached Carla Moreno through her era of dominance in Brazilian triathlon — years winning Brazil’s top Olympic-distance races and more than six seasons unbeaten in Miami. He has qualified athletes for ITU, Ironman 70.3 and Ironman 140.6 world championships and coached the Brazilian national team at international events. A specialist in exercise physiology and training prescription, he is the creator of the ECO Method.',
'“O contato com a ciência não substitui o campo. Ele qualifica o olhar sobre o campo.”':'“Science does not replace time in the field. It sharpens the way we see the field.”',
'Co-fundadora e Treinadora':'Co-founder & Coach',
'Campeã Mundial Júnior de Triathlon, integrou a Seleção Brasileira por 14 anos consecutivos e representou o Brasil em dois Jogos Olímpicos — Sydney 2000 e Atenas 2004 —, com títulos mundiais, pan-americanos e vitórias em Copas do Mundo. Hoje atua diretamente no atendimento e na orientação dos atletas, traduzindo o treinamento em decisões práticas, estratégia de prova e equilíbrio entre esporte e vida pessoal.':'Junior Triathlon World Champion, she was part of the Brazilian national team for 14 consecutive years and represented Brazil at two Olympic Games — Sydney 2000 and Athens 2004 — with world and Pan American titles and World Cup wins. Today she works directly with our athletes, turning training into practical decisions, race strategy and balance between sport and personal life.',
'“Carregar meu nome no time é uma honra que nunca se tornou rotina. A CMTeam é, sim, o meu nome, mas, mais do que isso, é a soma de todas as pessoas que decidiram acreditar no mesmo propósito.”':'“Having my name on this team is an honor that has never become routine. CMTeam is my name, yes — but more than that, it is the sum of everyone who chose to believe in the same purpose.”',
'Livros e textos':'Books & writing','Ensinar o atleta também é treino.':'Teaching the athlete is training too.',
'Nossa missão vai além da planilha: queremos que cada atleta entenda o que está fazendo e por quê. Por isso, o conhecimento do time circula toda semana no grupo exclusivo dos atletas — e, ao fim de cada ano, vira livro, registrando a vivência real do que é treinado e aprendido dentro da CMTeam.':'Our mission goes beyond the training plan: we want every athlete to understand what they are doing and why. That is why knowledge flows every week in our athletes’ private group — and, at the end of each year, it becomes a book (in Portuguese) that records what is truly trained and learned inside CMTeam.',
'Segunda':'Monday','Texto reflexivo sobre treino, processo e mentalidade':'A reflective piece on training, process and mindset',
'Quarta':'Wednesday','Infográficos técnicos e educativos':'Technical, educational infographics',
'Sexta':'Friday','Textos diretos, aplicáveis ao treino do dia a dia':'Straightforward pieces you can apply to everyday training',
'Publicado':'Published',
'Reflexões, aprendizados e os pilares que moldaram um ano de treinos. O primeiro livro da CMTeam reúne os textos escritos para o time ao longo de 2025.':'Reflections, lessons and the pillars that shaped a year of training. CMTeam’s first book brings together the texts written for the team throughout 2025. In Portuguese.',
'Amazon Brasil':'Amazon Brazil','Amazon EUA':'Amazon US',
'Saindo do forno':'Coming soon',
'Construído semana a semana a partir dos textos de segunda de 2026. Cada texto que o time recebe hoje é uma página do próximo livro.':'Built week by week from our 2026 Monday texts. Every piece the team receives today is a page of the next book.',
'Quero ser avisado →':'Notify me →',
'E-book gratuito':'Free e-book',
'Lições rápidas para uma mente mais forte no esporte. Um livro de bolso sobre dor, disciplina, fracasso e os pilares da força mental, com um checklist de 8 hábitos para colocar em prática.':'Quick lessons for a stronger mind in sport. A pocket book on pain, discipline, failure and the pillars of mental strength, with a checklist of 8 habits to put into practice. Available in Portuguese.',
'Nome':'Name','Baixar grátis':'Get it free','Baixar o livro (PDF)':'Download the book (PDF)',
'8 hábitos para uma mente forte':'8 habits for a strong mind',
'Comece o dia com clareza, não com pressa':'Start the day with clarity, not rush','Antes de abrir o celular, respire e lembre por que você está treinando.':'Before you open your phone, breathe and remember why you are training.',
'Treine mesmo sem vontade':'Train even when you don’t feel like it','Quando você escolhe a execução, não a emoção, a mente entende quem manda.':'When you choose execution over emotion, your mind learns who is in charge.',
'Corrija a voz interna':'Correct your inner voice','Pegou o “não dá”? Interrompa, respire, troque a frase.':'Caught yourself thinking “I can’t”? Stop, breathe, change the sentence.',
'Execute bem o treino mais simples':'Nail the simplest session','Foco total até no regenerativo. É isso que constrói excelência.':'Full focus even on the recovery run. That is what builds excellence.',
'Aceite os dias ruins':'Accept the bad days','Não se sabote por um treino fraco. Recomece no dia seguinte, sem drama.':'Don’t sabotage yourself over one weak session. Start again tomorrow, no drama.',
'Silêncio ao invés de comparação':'Silence over comparison','Enquanto os outros postam, você trabalha. Sua evolução acontece longe da vitrine.':'While others post, you work. Your progress happens away from the spotlight.',
'Feche o dia com uma pergunta':'End the day with one question','“Hoje eu fui quem eu quero ser?” Se sim, celebre. Se não, aprenda.':'“Was I today who I want to be?” If yes, celebrate. If not, learn.',
'Confie no seu treinador e no processo':'Trust your coach and the process','Seu treinador vê o que você ainda não vê. Ouça, execute, aprenda.':'Your coach sees what you can’t see yet. Listen, execute, learn.',
'Treinos presenciais':'In-person training','Terça':'Tuesday','Corrida 6h00–7h20 · Natação 7h20–8h00':'Run 6:00–7:20am · Swim 7:20–8:00am','Bike 6h00–8h00':'Bike 6:00–8:00am','Quinta':'Thursday','Sábado':'Saturday','Longo de corrida · Natação em águas abertas':'Long run · Open-water swim',
'# Transição':'# Brick','Todo mês tem transição e simulado de prova.':'Every month: brick sessions and race simulations.',
'Uma ou duas vezes por mês, na Tribeach: natação + corrida, bike + corrida ou o triathlon completo. Técnica de execução, ritmo e estratégia de prova, treinados juntos. O treino preferido do time.':'Once or twice a month at Tribeach: swim + run, bike + run or the full triathlon. Technique, pacing and race strategy, trained together. The team’s favorite session.',
'No Instagram':'On Instagram','Acompanhe o time':'Follow the team','CMTeam — o time':'CMTeam — the team','Carla Moreno — treinadora':'Carla Moreno — coach',
'Últimos posts do @cmteam':'Latest posts from @cmteam','Ver tudo no Instagram →':'See all on Instagram →',
'Para quem é':'Who it’s for','A CMTeam faz sentido para quem…':'CMTeam is right for you if you…',
'Não é para quem busca atalhos, fórmulas prontas ou motivação vazia.':'It is not for those looking for shortcuts, ready-made formulas or empty motivation.',
'quer entender o que está fazendo':'want to understand what you are doing','valoriza processo mais do que picos':'value process more than peaks',
'aceita que evolução real exige tempo, consistência e leitura correta do treino':'accept that real progress takes time, consistency and a proper reading of training',
'busca performance sem abrir mão de saúde, equilíbrio e longevidade esportiva':'seek performance without giving up health, balance and longevity in sport',
'Não buscamos a perfeição,':'We don’t chase perfection,','buscamos a':'we chase','constância.':'consistency.','Não corremos pra mostrar,':'We don’t run to show off,','corremos pra':'we run to','ser.':'become.',
'Provavelmente estamos falando a mesma língua.':'We’re probably speaking the same language.',
'Se você procura um trabalho consciente, estruturado e com visão de longo prazo, conte o seu objetivo para a gente.':'If you are looking for mindful, structured coaching with a long-term vision, tell us about your goal.',
'Seguir @cmteam':'Follow @cmteam','Telefone de contato':'Phone','Mensagem':'Message','Enviar mensagem':'Send message',
'Assessoria de triathlon, corrida e esportes de endurance. Carla Moreno Team — Miami e online, em mais de 25 países.':'Triathlon, running and endurance coaching. Carla Moreno Team — Miami and online, in more than 25 countries.',
'Navegação':'Navigation','Treinos em Miami':'Training in Miami','E-book grátis':'Free e-book','Contato':'Contact',
'A cabeça corre primeiro — grátis':'A cabeça corre primeiro — free',
}
ATTR={
'Assessoria de triathlon, corrida e esportes de endurance. Metodologia ECO, acompanhamento próximo e visão de longo prazo — do iniciante ao competitivo. Miami e online.':'Triathlon, running and endurance coaching in Miami and online. The ECO Method, close guidance and a long-term vision — from first-timers to competitive athletes.',
'CMTeam — Aqui, cada treino tem motivo.':'CMTeam — Every session has a reason.',
'Fechar aviso':'Close','CMTeam — início':'CMTeam — home','Principal':'Main','Falar no WhatsApp':'Message us on WhatsApp','Fale conosco':'Contact us',
'Atletas da CMTeam pedalando à noite em Miami':'CMTeam athletes riding at night in Miami','Provas dos nossos atletas':'Our athletes’ races',
'Atletas da CMTeam reunidos após o treino em Miami':'CMTeam athletes together after a session in Miami','Coach da CMTeam orientando atletas antes do treino':'CMTeam coach briefing athletes before a session',
'San Palma, head coach da CMTeam':'San Palma, CMTeam head coach','Carla Moreno comemorando vitória em prova do circuito mundial de triathlon':'Carla Moreno celebrating a win at a world series triathlon',
'Capa do livro Nossa Jornada 2025, de San Palma':'Cover of Nossa Jornada 2025, by San Palma','Capa do livro Nossa Jornada 2026, de San Palma':'Cover of Nossa Jornada 2026, by San Palma','Capa do livro A cabeça corre primeiro, de San Palma':'Cover of A cabeça corre primeiro, by San Palma',
'Site CMTeam — e-book gratuito':'CMTeam website (EN) — free e-book','Seu nome':'Your name','Seu e-mail':'Your email',
'Contato pelo site CMTeam':'Contact from CMTeam website (EN)','Site CMTeam':'CMTeam website (EN)',
'com código do país, ex.: +55 11 99999-9999':'with country code, e.g. +1 305 555 0000','Conte seu objetivo, sua prova-alvo e sua rotina de treinos.':'Tell us your goal, your target race and your training routine.',
'Voltar ao topo':'Back to top','Formulário de contato':'Contact form','Ver no Instagram':'See on Instagram',
}
missing=[]
def txt(m):
    raw=m.group(1); k=raw.strip()
    if k in TEXT: return '>'+raw.replace(k,TEXT[k])+'<'
    return m.group(0)
# split out scripts/styles so we don't touch them in the text pass
parts=re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)',s)
for i,p in enumerate(parts):
    if p.startswith('<script') or p.startswith('<style'): continue
    p=re.sub(r'>([^<>]+)<',txt,p)
    def at(m):
        k=m.group(2)
        return m.group(1)+'="'+ATTR.get(k,k)+'"'
    p=re.sub(r'(alt|aria-label|placeholder|content|value|title)="([^"]*)"',at,p)
    parts[i]=p
s=''.join(parts)
# script / misc strings
REP=[
('ECO <span style="color: #CB333B">|</span> Esforço Contínuo Ondulatório</h2>','ECO <span style="color: #CB333B">|</span> Esforço Contínuo Ondulatório</h2>\n<p style="margin: 0; font-size: 17px; line-height: 1.5; color: #B5B5B5"><em>Continuous Undulating Effort</em> — the methodology keeps its original Portuguese name.</p>'),
('<a href="./" class="on" aria-current="page" lang="pt-BR">PT</a><span aria-hidden="true">|</span><a href="en/" lang="en" hreflang="en">EN</a>','<a href="../" lang="pt-BR" hreflang="pt-BR">PT</a><span aria-hidden="true">|</span><a href="./" class="on" aria-current="page" lang="en">EN</a>'),
('<a href="en/" lang="en" style="color: #B5B5B5">English version</a>','<a href="../" lang="pt-BR" style="color: #B5B5B5">Versão em português</a>'),
('<html lang="pt-BR">','<html lang="en">'),
('<meta property="og:locale" content="pt_BR">','<meta property="og:locale" content="en_US">'),
('<link rel="canonical" href="https://cmteam.us/">','<link rel="canonical" href="https://cmteam.us/en/">'),
('<meta property="og:url" content="https://cmteam.us/">','<meta property="og:url" content="https://cmteam.us/en/">'),
('Preencha seu nome e um e-mail válido.','Please enter your name and a valid email.'),
('Liberando…','Unlocking…'),("btn.textContent='Baixar grátis'","btn.textContent='Get it free'"),
('Preencha todos os campos, com um e-mail válido.','Please fill in all fields with a valid email.'),
('Enviando…','Sending…'),("btn.textContent='Enviar mensagem'","btn.textContent='Send message'"),
('Mensagem enviada! Respondemos em breve.','Message sent! We will get back to you soon.'),
('Não foi possível enviar agora. Tente de novo ou fale com a gente pelo <a href="https://wa.me/13053959104">WhatsApp</a> ou por <a href="mailto:info@cmteam.us">info@cmteam.us</a>.','We could not send it right now. Please try again or reach us on <a href="https://wa.me/13053959104">WhatsApp</a> or at <a href="mailto:info@cmteam.us">info@cmteam.us</a>.'),
('text=Ol%C3%A1!%20Quero%20saber%20mais%20sobre%20a%20CMTeam.','text=Hi!%20I%27d%20like%20to%20know%20more%20about%20CMTeam.'),
('text=Ol%C3%A1!%20Quero%20ser%20avisado%20do%20lan%C3%A7amento%20do%20livro%20Nossa%20Jornada%202026.','text=Hi!%20Please%20let%20me%20know%20when%20Nossa%20Jornada%202026%20is%20released.'),
('src="img/','src="../img/'),('href="img/','href="../img/'),('href="livros/','href="../livros/'),('href="favicon','href="../favicon'),
]
for a,b in REP:
    if a not in s: missing.append(a[:60])
    s=s.replace(a,b)
open(DST,'w',encoding='utf-8').write(s)
print('missing script reps:',missing)
