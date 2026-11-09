"""Cria a pagina "Sobre" no Ghost local.

Uso:
    python scripts/criar-paginas.py            # cria a pagina
    python scripts/criar-paginas.py --remover  # apaga a pagina

O Ghost precisa estar parado (docker compose stop) porque o SQLite nao aceita
dois escritores. O script guarda uma copia do banco antes de alterar.
"""

import argparse
import datetime
import io
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

BLOCOS = [
    ("p", "Oi, eu sou o Maycon. Trabalho com produto, gosto de tecnologia e passo boa parte do tempo livre entre jogos e projetos que começam como curiosidade."),
    ("p", "Este blog é onde essas coisas se encontram. Não é portfólio, nem canal de notícias: é um caderno aberto sobre o que vale a pena testar, entender e dividir."),
    ("h2", "O que você encontra aqui"),
    ("ul", [
        "Tecnologia: ferramentas, fluxos de trabalho e o que realmente vale adotar.",
        "Lifestyle: rotina, foco e o espaço entre uma coisa e outra.",
        "Tudo mais: assuntos que não cabem numa caixinha só.",
    ]),
    ("h2", "Como eu penso"),
    ("p", "Gosto de ideias que saem do papel. Prefiro uma versão feia que funciona a um plano bonito que nunca começou, e continuo achando que a melhor forma de aprender é tentar."),
    ("quote", "Feito de curiosidade."),
    ("h2", "Sobre este site"),
    ("p", "O Maykcoisa é feito para leitura confortável: uma coluna estreita, tipografia grande e pouco ruído em volta. Sem pop-up, sem contador de visitas, sem pressa."),
    ("p", "Se quiser acompanhar, o RSS é o caminho mais direto. Se preferir navegar, os assuntos estão no menu."),
]


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
            filhos.append({"children": [no_texto(valor)], "direction": "ltr", "format": "",
                           "indent": 0, "type": "paragraph", "version": 1})
        elif tipo == "h2":
            filhos.append({"children": [no_texto(valor)], "direction": "ltr", "format": "",
                           "indent": 0, "tag": "h2", "type": "heading", "version": 1})
        elif tipo == "quote":
            filhos.append({"children": [no_texto(valor)], "direction": "ltr", "format": "",
                           "indent": 0, "type": "quote", "version": 1})
        elif tipo == "ul":
            itens = [{"children": [no_texto(item)], "direction": "ltr", "format": "",
                      "indent": 0, "type": "listitem", "value": 1, "version": 1}
                     for item in valor]
            filhos.append({"children": itens, "direction": "ltr", "format": "", "indent": 0,
                           "listType": "bullet", "start": 1, "tag": "ul", "type": "list",
                           "version": 1})
    return json.dumps({"root": {"children": filhos, "direction": "ltr", "format": "",
                                "indent": 0, "type": "root", "version": 1}})


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
            partes.append("<ul>" + "".join(f"<li>{i}</li>" for i in valor) + "</ul>")
    return "\n".join(partes)


def abrir():
    if not os.path.exists(DB):
        sys.exit(f"Banco nao encontrado em {DB}")
    copia = os.path.join(
        os.path.dirname(DB),
        f"ghost-backup-paginas-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.db",
    )
    shutil.copy2(DB, copia)
    print(f"Backup: {copia}")
    return sqlite3.connect(DB)


def id_autor(conn):
    linha = conn.execute("select id from users where email = ?", (AUTOR_EMAIL,)).fetchone()
    if not linha:
        linha = conn.execute("select id from users order by created_at limit 1").fetchone()
    if not linha:
        sys.exit("Nenhum autor cadastrado no Ghost.")
    return linha[0]


def criar(conn):
    if conn.execute("select id from posts where slug = 'sobre'").fetchone():
        print("pagina /sobre/ ja existe")
        return

    autor = id_autor(conn)
    post_id = secrets.token_hex(12)
    agora = atual()
    texto = "\n\n".join(v if isinstance(v, str) else " ".join(v) for _, v in BLOCOS)

    conn.execute(
        """
        insert into posts (
            id, uuid, title, slug, mobiledoc, lexical, html, comment_id, plaintext,
            feature_image, featured, type, status, locale, visibility,
            email_recipient_filter, created_at, updated_at, published_at, published_by,
            custom_excerpt, auto_excerpt, reading_time, show_title_and_feature_image
        ) values (?,?,?,?,NULL,?,?,?,?,NULL,0,'page','published',NULL,'public',
                  'all',?,?,?,?,NULL,?,NULL,1)
        """,
        (post_id, str(uuid.uuid4()), "Sobre o Maycon", "sobre",
         lexical(BLOCOS), html(BLOCOS), post_id, texto,
         agora, agora, agora, autor, texto[:300]),
    )
    conn.execute(
        "insert into posts_authors (id, post_id, author_id, sort_order) values (?,?,?,0)",
        (secrets.token_hex(12), post_id, autor),
    )
    conn.commit()
    print("pagina /sobre/ criada")


def remover(conn):
    linha = conn.execute("select id from posts where slug = 'sobre'").fetchone()
    if not linha:
        print("pagina /sobre/ nao existe")
        return
    conn.execute("delete from posts_authors where post_id = ?", (linha[0],))
    conn.execute("delete from posts_tags where post_id = ?", (linha[0],))
    conn.execute("delete from posts where id = ?", (linha[0],))
    conn.commit()
    print("pagina /sobre/ removida")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remover", action="store_true")
    args = parser.parse_args()

    conn = abrir()
    if args.remover:
        remover(conn)
    else:
        criar(conn)
    conn.close()


if __name__ == "__main__":
    main()
