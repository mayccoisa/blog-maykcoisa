"""Cria artigos ficticios no Ghost local para testar o tema e a navegacao.

Uso:
    python scripts/criar-exemplos.py            # cria os artigos
    python scripts/criar-exemplos.py --remover  # apaga os artigos de exemplo

O Ghost precisa estar parado (docker compose stop) porque o SQLite fica travado
com mais de um escritor. O script faz uma copia de seguranca do banco antes de
qualquer alteracao.
"""

import argparse
import datetime
import json
import os
import secrets
import shutil
import sqlite3
import sys
import uuid

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(RAIZ, "ghost", "content", "data", "ghost.db")
AUTOR_EMAIL = "ghost@example.com"


def atual():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")


def no_texto(texto):
    return {
        "detail": 0,
        "format": 0,
        "mode": "normal",
        "style": "",
        "text": texto,
        "type": "text",
        "version": 1,
    }


def lexical(blocos):
    filhos = []
    for tipo, valor in blocos:
        if tipo == "p":
            filhos.append({
                "children": [no_texto(valor)],
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "type": "paragraph",
                "version": 1,
            })
        elif tipo == "h2":
            filhos.append({
                "children": [no_texto(valor)],
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "tag": "h2",
                "type": "heading",
                "version": 1,
            })
        elif tipo == "quote":
            filhos.append({
                "children": [no_texto(valor)],
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "type": "quote",
                "version": 1,
            })
        elif tipo == "ul":
            itens = []
            for item in valor:
                itens.append({
                    "children": [no_texto(item)],
                    "direction": "ltr",
                    "format": "",
                    "indent": 0,
                    "type": "listitem",
                    "value": 1,
                    "version": 1,
                })
            filhos.append({
                "children": itens,
                "direction": "ltr",
                "format": "",
                "indent": 0,
                "listType": "bullet",
                "start": 1,
                "tag": "ul",
                "type": "list",
                "version": 1,
            })

    return json.dumps({
        "root": {
            "children": filhos,
            "direction": "ltr",
            "format": "",
            "indent": 0,
            "type": "root",
            "version": 1,
        }
    })


def html(blocos):
    partes = []
    for tipo, valor in blocos:
        if tipo == "p":
            partes.append(f"<p>{valor}</p>")
        elif tipo == "h2":
            partes.append(f"<h2>{valor}</h2>")
        elif tipo == "quote":
            partes.append(f"<blockquote><p>{valor}</p></blockquote>")
        elif tipo == "ul":
            itens = "".join(f"<li>{item}</li>" for item in valor)
            partes.append(f"<ul>{itens}</ul>")
    return "\n".join(partes)


ARTIGOS = [
    {
        "slug": "da-ideia-ao-primeiro-projeto-com-ia",
        "titulo": "Da ideia ao primeiro projeto: por onde começar com IA",
        "assunto": "tecnologia",
        "publicado": "2026-11-08 09:00:00",
        "destaque": 0,
        "resumo": "Um olhar prático sobre ferramentas, escolhas e o primeiro passo para construir algo seu.",
        "blocos": [
            ("p", "Toda ideia começa meio torta. A diferença entre quem tira do papel e quem só guarda mais uma aba aberta raramente é talento — é o tamanho do primeiro passo."),
            ("h2", "Comece pelo problema, não pela ferramenta"),
            ("p", "É tentador abrir a lista de novidades da semana e escolher uma pela promessa. Só que nenhuma ferramenta sabe qual é o seu problema. Antes de instalar qualquer coisa, escreva em uma frase o que você quer resolver. Se a frase não couber em uma linha, o problema ainda está grande demais."),
            ("p", "Esse exercício parece bobo e economiza semanas. A maior parte dos projetos que morrem no rascunho morreu tentando resolver três coisas ao mesmo tempo."),
            ("h2", "Três perguntas antes de começar"),
            ("ul", [
                "O que eu quero que exista quando terminar?",
                "Qual é a menor versão disso que já me serve?",
                "O que eu já tenho e posso reaproveitar?",
            ]),
            ("quote", "Curiosidade é um ótimo ponto de partida e um péssimo plano de execução."),
            ("h2", "Um passo do tamanho de uma tarde"),
            ("p", "O primeiro passo bom é aquele que cabe em uma tarde e termina com algo que você consegue mostrar para alguém. Não precisa ser bonito, nem completo, nem escalável. Precisa existir."),
            ("p", "Depois que existe, tudo fica mais fácil: você para de discutir possibilidades e passa a corrigir algo concreto. É a diferença entre planejar uma viagem e finalmente sair de casa."),
            ("p", "Se o resultado da tarde for feio, ótimo — significa que você aprendeu algo que nenhum vídeo ensinaria. Guarde o que funcionou e siga na próxima."),
            ("h2", "Onde a IA realmente ajuda"),
            ("p", "Existe uma diferença grande entre pedir para a IA resolver o projeto e pedir para ela resolver o pedaço chato dele. A segunda opção é onde o ganho aparece."),
            ("p", "Renomear arquivos, escrever o script de conversão, explicar um erro de biblioteca, montar a primeira versão de uma tela: tarefas com começo e fim claros, que você sabe avaliar quando terminam. Delegar essas partes libera o tempo para o que exige julgamento."),
            ("p", "O contrário também vale: pedir uma arquitetura inteira para uma ferramenta que não conhece o seu contexto costuma produzir algo que parece certo e quebra na primeira semana."),
            ("h2", "O que ninguém conta sobre a primeira versão"),
            ("p", "A primeira versão de qualquer projeto é constrangedora. Não porque você fez errado, mas porque é assim que funciona. Quem mostra o resultado bonito no vídeo já passou por três versões que ninguém viu."),
            ("p", "O erro mais comum de quem está começando não é técnico: é esperar que a versão inicial já sirva para mostrar. Ela não serve. Ela serve para você entender o problema, e isso não tem atalho."),
            ("p", "Depois da primeira versão, o trabalho muda de natureza. Você para de perguntar \"como faço isso?\" e começa a perguntar \"o que está atrapalhando?\". A segunda pergunta é muito mais produtiva."),
            ("h2", "Um roteiro de uma semana"),
            ("ul", [
                "Dia 1: escrever o problema em uma frase e listar o que você já tem.",
                "Dia 2: montar a versão mais feia possível que já funciona.",
                "Dia 3: usar a sua própria versão como se fosse de outra pessoa.",
                "Dia 4: consertar só o que atrapalhou de verdade.",
                "Dia 5: mostrar para alguém e anotar as perguntas que aparecerem.",
            ]),
            ("p", "Cinco dias não é prazo de mercado, é prazo de curiosidade. Se a coisa empolgar, a semana seguinte se organiza sozinha. Se não empolgar, você gastou cinco dias e descobriu algo sobre o que gosta."),
            ("h2", "O que fica depois do projeto"),
            ("p", "Projeto terminado ensina menos do que projeto abandonado no meio. Quando você para algo, precisa nomear o motivo — e o motivo quase nunca é falta de tempo, é falta de interesse ou de clareza."),
            ("p", "Anote o motivo antes de fechar a pasta. Daqui a seis meses, essa anotação vale mais do que o código que você escreveu."),
            ("p", "O primeiro projeto não precisa ser o projeto da vida. Ele precisa ser o primeiro. Todo o resto é consequência de ter começado."),
        ],
    },
    {
        "slug": "um-setup-que-trabalha-a-seu-favor",
        "titulo": "Um setup que trabalha a seu favor",
        "assunto": "tecnologia",
        "publicado": "2026-11-05 09:00:00",
        "destaque": 1,
        "resumo": "Um espaço com menos distrações e mais lugar para o que você quer fazer.",
        "blocos": [
            ("p", "Setup não é coleção de periféricos caros. É o conjunto de decisões que faz o ambiente parar de competir com você."),
            ("h2", "O que atrapalha mora na tela"),
            ("p", "A maior parte das distrações não vem da mesa, vem da quantidade de janelas. Um monitor a mais resolve muita coisa quando o problema é espaço, e nenhuma quando o problema é falta de foco."),
            ("p", "Vale medir: quantas abas você mantém abertas por hábito? Quantos aplicativos abrem sozinhos ao ligar a máquina? Cada um deles cobra um pedágio pequeno, diário e invisível."),
            ("h2", "Três ajustes que custam nada"),
            ("ul", [
                "Uma função por tela: trabalho em um espaço, conversa em outro.",
                "Barra de tarefas com o que você usa todo dia, nada mais.",
                "Um atalho único para voltar ao que importa.",
            ]),
            ("quote", "O melhor setup é o que você esquece que existe."),
            ("p", "Depois de organizar, a tentação é continuar organizando. Resista. Ajuste fino é útil até virar entretenimento, e aí o setup passa a ser o próprio trabalho."),
            ("p", "Um espaço que trabalha a seu favor tem menos coisas visíveis e mais coisas prontas. Se você precisa pensar onde clicar, ainda tem ajuste a fazer."),
        ],
    },
    {
        "slug": "desligar-tambem-faz-parte-do-processo",
        "titulo": "Desligar também faz parte do processo",
        "assunto": "lifestyle",
        "publicado": "2026-11-02 09:00:00",
        "destaque": 0,
        "resumo": "Sobre caminhar sem pressa e abrir espaço para outras ideias aparecerem.",
        "blocos": [
            ("p", "Tem uma armadilha silenciosa em trabalhar com o que se gosta: a sensação de que parar é desperdício. Não é."),
            ("h2", "O intervalo não é o oposto do trabalho"),
            ("p", "As melhores ideias que tive sobre um problema apareceram longe dele — numa caminhada, no meio de uma conversa sem assunto, lavando louça. O cérebro continua trabalhando quando a gente solta o volante."),
            ("p", "Isso não é conselho motivacional, é mecânica. Alternar entre foco intenso e descanso de verdade é o que sustenta a qualidade do foco."),
            ("quote", "Descansar não é recompensa pelo trabalho feito: é parte de como ele é feito."),
            ("h2", "Um teste simples"),
            ("p", "Escolha um dia da semana e não abra o editor. Nem para responder rápido. Anote o que vier à cabeça em um papel e deixe ali."),
            ("p", "No dia seguinte, olhe a lista. Boa parte vai parecer urgente e não era. Uma ou duas coisas vão continuar fazendo sentido — essas eram as que importavam."),
            ("p", "Desligar é uma habilidade, e como toda habilidade fica ruim no começo. Insista por três semanas antes de concluir que não funciona."),
        ],
    },
    {
        "slug": "aprender-so-por-curiosidade",
        "titulo": "O prazer de aprender uma coisa só por curiosidade",
        "assunto": "tudo-mais",
        "publicado": "2026-10-29 09:00:00",
        "destaque": 1,
        "resumo": "Nem todo interesse precisa virar trabalho. Alguns podem ser só seus.",
        "blocos": [
            ("p", "Existe uma pressão estranha de transformar todo interesse em competência útil, em portfólio, em post. Às vezes a gente só quer entender como funciona uma coisa."),
            ("h2", "O interesse não precisa se justificar"),
            ("p", "Passei um fim de semana aprendendo como um relógio mecânico conta o tempo. Não tem nenhuma aplicação no meu trabalho. Foi bom de um jeito que é difícil de explicar e fácil de reconhecer."),
            ("p", "Curiosidade sem objetivo prático é o que mantém a cabeça flexível. Quem só aprende o que dá retorno imediato vai ficando com um repertório cada vez mais estreito."),
            ("quote", "Aprender por prazer é o único jeito de aprender algo que ninguém pediu."),
            ("h2", "Como começar sem virar projeto"),
            ("ul", [
                "Escolha um assunto que não tem nada a ver com seu trabalho.",
                "Dê a ele uma tarde, não um trimestre.",
                "Não publique nada. Não precisa virar conteúdo.",
            ]),
            ("p", "Se depois da tarde a curiosidade continuar, ótimo — ela mesma vai cobrar o próximo passo. Se acabar, você gastou uma tarde e ganhou uma história."),
        ],
    },
    {
        "slug": "as-ferramentas-que-voce-realmente-usa",
        "titulo": "As ferramentas certas são as que você realmente usa",
        "assunto": "tecnologia",
        "publicado": "2026-10-24 09:00:00",
        "destaque": 0,
        "resumo": "Um convite para escolher melhor antes de instalar mais um aplicativo.",
        "blocos": [
            ("p", "Instalar é fácil. O difícil é admitir, seis meses depois, que aquela ferramenta maravilhosa nunca passou da primeira semana."),
            ("h2", "A conta que ninguém faz"),
            ("p", "Cada app novo custa mais do que o preço da assinatura: custa o tempo de aprender, o hábito de abrir, a decisão de em qual lugar guardar o quê. Ferramenta demais espalha a informação e cansa quem deveria ser ajudado."),
            ("p", "Uma regra que tenho usado: só troco o que já funciona se o problema atual doer de verdade. Novidade não é problema."),
            ("quote", "A melhor ferramenta é a que você abre sem pensar e fecha sem culpa."),
            ("h2", "Como cortar"),
            ("ul", [
                "Liste o que você abriu nos últimos sete dias.",
                "O que não abriu, sai. Sem negociação.",
                "O que sobrou, aprende melhor em vez de trocar.",
            ]),
            ("p", "Menos ferramentas, mais profundidade em cada uma. Parece menos moderno e funciona melhor."),
        ],
    },
    {
        "slug": "pequenos-rituais-para-um-dia-com-mais-respiro",
        "titulo": "Pequenos rituais para um dia com mais respiro",
        "assunto": "lifestyle",
        "publicado": "2026-10-20 09:00:00",
        "destaque": 1,
        "resumo": "Um café, algumas páginas e um começo de dia longe das notificações.",
        "blocos": [
            ("p", "Não é sobre acordar às cinco da manhã. É sobre não entregar os primeiros minutos do dia para a caixa de entrada."),
            ("h2", "O começo define o resto"),
            ("p", "A primeira hora costuma decidir o tom das outras. Se ela começa com reação, o dia inteiro vira reação. Se começa com escolha, sobra um pouco de espaço para o que importa."),
            ("p", "Meu ritual é pequeno e sem glamour: café, uma página de livro, nenhum aplicativo. Quinze minutos. Muda pouco e muda o dia."),
            ("quote", "Ritual não é performance. É o que você faz mesmo quando ninguém está olhando."),
            ("h2", "Três que funcionaram aqui"),
            ("ul", [
                "Café antes do celular, sempre nessa ordem.",
                "Uma página lida, não um capítulo.",
                "Cinco minutos de janela aberta, sem nada na mão.",
            ]),
            ("p", "O ponto não é a atividade, é a repetição. O cérebro aprende o sinal de que o dia começou de um jeito escolhido."),
            ("p", "Comece com um. Um ritual só, por duas semanas. Depois veja se cabe outro."),
        ],
    },
]


def abrir_banco():
    if not os.path.exists(DB):
        sys.exit(f"Banco nao encontrado em {DB}")

    copia = os.path.join(
        os.path.dirname(DB),
        f"ghost-backup-exemplos-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.db",
    )
    shutil.copy2(DB, copia)
    print(f"Backup: {copia}")
    return sqlite3.connect(DB)


def id_tag(conn, slug):
    linha = conn.execute("select id from tags where slug = ?", (slug,)).fetchone()
    if not linha:
        sys.exit(f"Tag '{slug}' nao existe. Crie os assuntos antes de rodar.")
    return linha[0]


def id_autor(conn):
    linha = conn.execute("select id from users where email = ?", (AUTOR_EMAIL,)).fetchone()
    if not linha:
        linha = conn.execute("select id from users order by created_at limit 1").fetchone()
    if not linha:
        sys.exit("Nenhum autor cadastrado no Ghost.")
    return linha[0]


def remover(conn, autor):
    slugs = [artigo["slug"] for artigo in ARTIGOS]
    marcadores = ",".join("?" for _ in slugs)
    ids = [linha[0] for linha in conn.execute(
        f"select id from posts where slug in ({marcadores})", slugs
    )]
    for post_id in ids:
        conn.execute("delete from posts_tags where post_id = ?", (post_id,))
        conn.execute("delete from posts_authors where post_id = ?", (post_id,))
        conn.execute("delete from posts where id = ?", (post_id,))
    conn.commit()
    print(f"Removidos {len(ids)} artigo(s) de exemplo.")


def criar(conn, autor):
    criados = 0
    for artigo in ARTIGOS:
        existente = conn.execute(
            "select id from posts where slug = ?", (artigo["slug"],)
        ).fetchone()
        if existente:
            print(f"ja existe: {artigo['slug']}")
            continue

        post_id = secrets.token_hex(12)
        texto = "\n\n".join(
            valor if isinstance(valor, str) else " ".join(valor)
            for _, valor in artigo["blocos"]
        )
        publicado = artigo["publicado"]

        conn.execute(
            """
            insert into posts (
                id, uuid, title, slug, mobiledoc, lexical, html, comment_id, plaintext,
                feature_image, featured, type, status, locale, visibility,
                email_recipient_filter, created_at, updated_at, published_at, published_by,
                custom_excerpt, auto_excerpt, reading_time, show_title_and_feature_image
            ) values (?,?,?,?,NULL,?,?,?,?,?,?,?,?,NULL,?,?,?,?,?,?,?,?,?,1)
            """,
            (
                post_id,
                str(uuid.uuid4()),
                artigo["titulo"],
                artigo["slug"],
                lexical(artigo["blocos"]),
                html(artigo["blocos"]),
                post_id,
                texto.replace("\n\n", "\n"),
                f"/content/images/exemplos/{artigo['slug']}.jpg",
                artigo["destaque"],
                "post",
                "published",
                "public",
                "all",
                publicado,
                publicado,
                publicado,
                autor,
                artigo["resumo"],
                texto[:300],
                None,
            ),
        )

        conn.execute(
            "insert into posts_tags (id, post_id, tag_id, sort_order) values (?,?,?,0)",
            (secrets.token_hex(12), post_id, id_tag(conn, artigo["assunto"])),
        )
        conn.execute(
            "insert into posts_authors (id, post_id, author_id, sort_order) values (?,?,?,0)",
            (secrets.token_hex(12), post_id, autor),
        )
        criados += 1
        print(f"criado: {artigo['slug']}")

    conn.commit()
    print(f"Total criado: {criados}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remover", action="store_true")
    args = parser.parse_args()

    conn = abrir_banco()
    autor = id_autor(conn)
    if args.remover:
        remover(conn, autor)
    else:
        criar(conn, autor)
    conn.close()


if __name__ == "__main__":
    main()
