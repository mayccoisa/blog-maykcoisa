"""Cria a pagina "Referencias" no Ghost local e poe o item no menu.

Uso:
    python scripts/criar-referencias.py            # cria a pagina e o item de menu
    python scripts/criar-referencias.py --remover  # desfaz as duas coisas

A pagina fica vazia de proposito: quem desenha tudo e o template
theme/mayccoisa/page-referencias.hbs, que o Ghost usa sozinho para o slug
"referencias". A lista vive em theme/mayccoisa/partials/referencias/dados.hbs.

O Ghost precisa estar parado (docker compose stop) porque o SQLite nao aceita
dois escritores. O script guarda uma copia do banco antes de alterar.
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

SLUG = "referencias"
TITULO = "Referências"
RESUMO = "Repositórios que o Maycon já usou e recomenda, com onde usou e por que vale a pena."
MENU = {"label": "Referências", "url": "/referencias/"}
LEXICAL_VAZIO = json.dumps({"root": {"children": [], "direction": None, "format": "",
                                     "indent": 0, "type": "root", "version": 1}})


def atual():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")


def abrir():
    if not os.path.exists(DB):
        sys.exit(f"Banco nao encontrado em {DB}")
    copia = os.path.join(
        os.path.dirname(DB),
        f"ghost-backup-referencias-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.db",
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


def ler_menu(conn):
    linha = conn.execute("select value from settings where key = 'navigation'").fetchone()
    return json.loads(linha[0]) if linha and linha[0] else []


def gravar_menu(conn, itens):
    conn.execute("update settings set value = ?, updated_at = ? where key = 'navigation'",
                 (json.dumps(itens, ensure_ascii=False), atual()))


def criar(conn):
    if conn.execute("select id from posts where slug = ?", (SLUG,)).fetchone():
        print(f"pagina /{SLUG}/ ja existe")
    else:
        autor = id_autor(conn)
        post_id = secrets.token_hex(12)
        agora = atual()
        conn.execute(
            """
            insert into posts (
                id, uuid, title, slug, mobiledoc, lexical, html, comment_id, plaintext,
                feature_image, featured, type, status, locale, visibility,
                email_recipient_filter, created_at, updated_at, published_at, published_by,
                custom_excerpt, auto_excerpt, reading_time, show_title_and_feature_image
            ) values (?,?,?,?,NULL,?,'',?,'',NULL,0,'page','published',NULL,'public',
                      'all',?,?,?,?,?,NULL,NULL,1)
            """,
            (post_id, str(uuid.uuid4()), TITULO, SLUG, LEXICAL_VAZIO, post_id,
             agora, agora, agora, autor, RESUMO),
        )
        conn.execute(
            "insert into posts_authors (id, post_id, author_id, sort_order) values (?,?,?,0)",
            (secrets.token_hex(12), post_id, autor),
        )
        print(f"pagina /{SLUG}/ criada")

    itens = ler_menu(conn)
    if any(item.get("url") == MENU["url"] for item in itens):
        print("item Referencias ja esta no menu")
    else:
        # Logo depois de "Projetos"
        posicao = next((i + 1 for i, item in enumerate(itens) if item.get("url") == "/projetos/"), len(itens))
        itens.insert(posicao, MENU)
        gravar_menu(conn, itens)
        print("item Referencias adicionado ao menu")

    conn.commit()


def remover(conn):
    linha = conn.execute("select id from posts where slug = ?", (SLUG,)).fetchone()
    if linha:
        conn.execute("delete from posts_authors where post_id = ?", (linha[0],))
        conn.execute("delete from posts_tags where post_id = ?", (linha[0],))
        conn.execute("delete from posts where id = ?", (linha[0],))
        print(f"pagina /{SLUG}/ removida")
    else:
        print(f"pagina /{SLUG}/ nao existe")

    itens = ler_menu(conn)
    restantes = [item for item in itens if item.get("url") != MENU["url"]]
    if len(restantes) != len(itens):
        gravar_menu(conn, restantes)
        print("item Referencias removido do menu")

    conn.commit()


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
