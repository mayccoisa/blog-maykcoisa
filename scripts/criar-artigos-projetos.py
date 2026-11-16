"""Cria no Ghost local os artigos que contam a história de cada projeto.

Uso:
    python scripts/criar-artigos-projetos.py              # cria os que ainda não existem
    python scripts/criar-artigos-projetos.py --atualizar  # recria os que já existem
    python scripts/criar-artigos-projetos.py --remover    # apaga os artigos daqui

O texto de cada artigo vive em conteudo/artigos/<slug>/artigo.py e as imagens
na mesma pasta. O script copia as imagens para ghost/content/images/projetos/<slug>/
e grava o artigo como rascunho, a menos que o arquivo diga status = "published".

O Ghost precisa estar parado (docker compose stop) porque o SQLite não aceita
dois escritores. O script guarda uma cópia do banco antes de alterar.
"""

import argparse
import datetime
import html as html_lib
import importlib.util
import json
import math
import os
import re
import secrets
import shutil
import sqlite3
import sys
import uuid

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(RAIZ, "ghost", "content", "data", "ghost.db")
CONTEUDO = os.path.join(RAIZ, "conteudo", "artigos")
IMAGENS_GHOST = os.path.join(RAIZ, "ghost", "content", "images", "projetos")
AUTOR_EMAIL = "ghost@example.com"
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def atual():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")


def carregar_artigos():
    artigos = []
    for slug in sorted(os.listdir(CONTEUDO)):
        arquivo = os.path.join(CONTEUDO, slug, "artigo.py")
        if not os.path.exists(arquivo):
            continue
        spec = importlib.util.spec_from_file_location(f"artigo_{slug}", arquivo)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        artigos.append({**modulo.ARTIGO, "slug": slug, "pasta": os.path.dirname(arquivo)})
    return artigos


# ------------------------------------------------------------ lexical e html --

def no_texto(texto, formato=0):
    return {"detail": 0, "format": formato, "mode": "normal", "style": "",
            "text": texto, "type": "text", "version": 1}


def inline(texto):
    """Quebra o texto em nós, trocando [rótulo](url) por link."""
    nos, pos = [], 0
    for m in LINK.finditer(texto):
        if m.start() > pos:
            nos.append(no_texto(texto[pos:m.start()]))
        nos.append({"children": [no_texto(m.group(1))], "direction": "ltr", "format": "",
                    "indent": 0, "type": "link", "version": 1, "rel": "noreferrer",
                    "target": None, "title": None, "url": m.group(2)})
        pos = m.end()
    if pos < len(texto):
        nos.append(no_texto(texto[pos:]))
    return nos


def inline_html(texto):
    partes, pos = [], 0
    for m in LINK.finditer(texto):
        partes.append(html_lib.escape(texto[pos:m.start()], quote=False))
        partes.append(f'<a href="{html_lib.escape(m.group(2))}" rel="noreferrer">'
                      f"{html_lib.escape(m.group(1), quote=False)}</a>")
        pos = m.end()
    partes.append(html_lib.escape(texto[pos:], quote=False))
    return "".join(partes)


def sem_link(texto):
    return LINK.sub(lambda m: m.group(1), texto)


def bloco_lexical(tipo, valor, url_imagem):
    base = {"direction": "ltr", "format": "", "indent": 0, "version": 1}
    if tipo == "p":
        return {**base, "children": inline(valor), "type": "paragraph"}
    if tipo == "h2":
        return {**base, "children": inline(valor), "type": "heading", "tag": "h2"}
    if tipo == "ul":
        itens = [{**base, "children": inline(item), "type": "listitem", "value": i + 1}
                 for i, item in enumerate(valor)]
        return {**base, "children": itens, "type": "list", "listType": "bullet",
                "start": 1, "tag": "ul"}
    if tipo == "img":
        largura, altura = valor["tamanho"]
        return {"type": "image", "version": 1, "src": url_imagem(valor["arquivo"]),
                "width": largura, "height": altura, "title": "", "alt": valor["alt"],
                "caption": html_lib.escape(valor.get("legenda", ""), quote=False),
                "cardWidth": valor.get("largura", "regular"), "href": ""}
    raise ValueError(f"bloco desconhecido: {tipo}")


def bloco_html(tipo, valor, url_imagem):
    if tipo == "p":
        return f"<p>{inline_html(valor)}</p>"
    if tipo == "h2":
        return f"<h2>{inline_html(valor)}</h2>"
    if tipo == "ul":
        return "<ul>" + "".join(f"<li>{inline_html(i)}</li>" for i in valor) + "</ul>"
    if tipo == "img":
        largura, altura = valor["tamanho"]
        legenda = valor.get("legenda", "")
        classe = "kg-card kg-image-card" + (" kg-width-wide" if valor.get("largura") == "wide" else "")
        if legenda:
            classe += " kg-card-hascaption"
        figura = (f'<figure class="{classe}"><img src="{url_imagem(valor["arquivo"])}" '
                  f'class="kg-image" alt="{html_lib.escape(valor["alt"])}" loading="lazy" '
                  f'width="{largura}" height="{altura}">')
        if legenda:
            figura += f"<figcaption>{html_lib.escape(legenda, quote=False)}</figcaption>"
        return figura + "</figure>"
    raise ValueError(f"bloco desconhecido: {tipo}")


def texto_puro(blocos):
    partes = []
    for tipo, valor in blocos:
        if tipo in ("p", "h2"):
            partes.append(sem_link(valor))
        elif tipo == "ul":
            partes.extend(sem_link(i) for i in valor)
    return "\n".join(partes)


# --------------------------------------------------------------------- banco --

def abrir():
    if not os.path.exists(DB):
        sys.exit(f"Banco não encontrado em {DB}")
    copia = os.path.join(os.path.dirname(DB),
                         f"ghost-backup-artigos-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.db")
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


def id_tag(conn, slug):
    linha = conn.execute("select id from tags where slug = ?", (slug,)).fetchone()
    if not linha:
        sys.exit(f"Assunto '{slug}' não existe no Ghost.")
    return linha[0]


def apagar(conn, slug):
    linha = conn.execute("select id from posts where slug = ?", (slug,)).fetchone()
    if not linha:
        return False
    for tabela in ("posts_tags", "posts_authors", "posts_meta"):
        conn.execute(f"delete from {tabela} where post_id = ?", (linha[0],))
    conn.execute("delete from posts where id = ?", (linha[0],))
    return True


def copiar_imagens(artigo):
    destino = os.path.join(IMAGENS_GHOST, artigo["slug"])
    os.makedirs(destino, exist_ok=True)
    for _, valor in artigo["blocos"]:
        if isinstance(valor, dict):
            origem = os.path.join(artigo["pasta"], valor["arquivo"])
            with Image.open(origem) as im:
                valor["tamanho"] = im.size
            shutil.copy2(origem, os.path.join(destino, valor["arquivo"]))
    capa = artigo["capa"]
    shutil.copy2(os.path.join(artigo["pasta"], capa), os.path.join(destino, capa))


def gravar(conn, autor, artigo):
    slug = artigo["slug"]
    copiar_imagens(artigo)

    def url_imagem(arquivo):
        return f"__GHOST_URL__/content/images/projetos/{slug}/{arquivo}"

    blocos = artigo["blocos"]
    lexical = json.dumps({"root": {"children": [bloco_lexical(t, v, url_imagem) for t, v in blocos],
                                   "direction": "ltr", "format": "", "indent": 0,
                                   "type": "root", "version": 1}}, ensure_ascii=False)
    corpo = "\n".join(bloco_html(t, v, url_imagem) for t, v in blocos)
    texto = texto_puro(blocos)
    leitura = max(1, math.ceil(len(texto.split()) / 230))
    status = artigo.get("status", "draft")
    publicado = artigo["publicado"] if status == "published" else None
    post_id = secrets.token_hex(12)

    conn.execute(
        """
        insert into posts (
            id, uuid, title, slug, mobiledoc, lexical, html, comment_id, plaintext,
            feature_image, featured, type, status, locale, visibility,
            email_recipient_filter, created_at, updated_at, published_at, published_by,
            custom_excerpt, auto_excerpt, reading_time, show_title_and_feature_image
        ) values (?,?,?,?,NULL,?,?,?,?,?,0,'post',?,NULL,'public','all',?,?,?,?,?,?,?,1)
        """,
        (post_id, str(uuid.uuid4()), artigo["titulo"], slug, lexical, corpo, post_id, texto,
         url_imagem(artigo["capa"]), status, atual(), atual(), publicado,
         autor if publicado else None, artigo["resumo"], texto[:300], leitura),
    )
    conn.execute(
        "insert into posts_meta (id, post_id, feature_image_alt, feature_image_caption) values (?,?,?,NULL)",
        (secrets.token_hex(12), post_id, artigo["capa_alt"]),
    )
    conn.execute("insert into posts_tags (id, post_id, tag_id, sort_order) values (?,?,?,0)",
                 (secrets.token_hex(12), post_id, id_tag(conn, artigo["assunto"])))
    conn.execute("insert into posts_authors (id, post_id, author_id, sort_order) values (?,?,?,0)",
                 (secrets.token_hex(12), post_id, autor))
    print(f"gravado: {slug} ({status}, {leitura} min de leitura)")


def main():
    parser = argparse.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--atualizar", action="store_true")
    grupo.add_argument("--remover", action="store_true")
    args = parser.parse_args()

    artigos = carregar_artigos()
    conn = abrir()
    autor = id_autor(conn)
    for artigo in artigos:
        existia = conn.execute("select 1 from posts where slug = ?", (artigo["slug"],)).fetchone()
        if args.remover:
            if apagar(conn, artigo["slug"]):
                print(f"removido: {artigo['slug']}")
            continue
        if existia and not args.atualizar:
            print(f"já existe: {artigo['slug']} (use --atualizar para recriar)")
            continue
        if existia:
            apagar(conn, artigo["slug"])
        gravar(conn, autor, artigo)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
