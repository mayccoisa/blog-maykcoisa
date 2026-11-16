# Publicação no GitHub Pages

O blog publicado está em **https://blog.maykcoisa.com.br/** (GitHub Pages com domínio próprio). O endereço antigo `mayccoisa.github.io/blog-maykcoisa` redireciona para ele.

## Como funciona

O Ghost precisa de Node e SQLite, então **não roda no GitHub Pages**, que serve
apenas arquivos estáticos. A publicação é um retrato do site:

1. O Ghost local renderiza as páginas em `http://localhost:2368`.
2. `scripts/exportar-estatico.mjs` percorre o site, baixa páginas e imagens,
   reescreve as URLs e grava tudo em `dist-pages/`.
3. `dist-pages/` é enviado para a branch `gh-pages` do repositório público.

```
Ghost local  →  scripts/exportar-estatico.mjs  →  dist-pages/  →  branch gh-pages  →  Pages
```

## Repositórios

| Repositório | Visibilidade | Conteúdo |
| --- | --- | --- |
| `mayccoisa/Blog-Mayccoisa` | privado | projeto completo, incluindo a base Nuxt antiga |
| `mayccoisa/blog-maykcoisa` | público | tema, scripts e documentação (`main`) + site publicado (`gh-pages`) |

## Publicando uma atualização

```powershell
# 1. Ghost rodando
.\scripts\Iniciar-Blog.ps1 -SemAbrir

# 2. Gerar o site
node scripts/exportar-estatico.mjs

# 3. Enviar
cd dist-pages
git add -A
git commit -m "Atualiza o site"
git push origin gh-pages
```

O Pages reconstrói em cerca de um minuto.

## Publicação pelo MCP

O MCP editorial em `mcp/` altera o Ghost pela Admin API. Rascunhos, publicações e agendamentos do MCP não disparam o exportador nem o deploy do GitHub Pages. O Ghost precisa estar ativo no horário agendado. Para refletir a publicação no site público estático ainda é necessário o fluxo de exportação e deploy descrito acima.

## O que muda no site estático

- **Busca:** a do Ghost (Sodo) depende do servidor e não existe no Pages. O tema tem
  busca própria em `assets/js/busca.js`, que lê os artigos do `rss.xml` e os projetos
  da página `/projetos/`, sem servidor. Abre pelo ícone de lupa, por `/` ou Ctrl+K.
- **Painel `/ghost/`:** não é publicado. A edição continua só no Ghost local.
- **RSS:** vira um arquivo único em `rss.xml`.
- **Formulários e comentários:** não existem no tema, então nada quebra.

## Domínio

O domínio `maykcoisa.com.br` está no registro.br, com os servidores DNS do próprio
registro.br em modo avançado (zona editável). Cada produto ganha um subdomínio.

| Subdomínio | Registro | Destino |
| --- | --- | --- |
| `blog.maykcoisa.com.br` | CNAME | `mayccoisa.github.io` |

No GitHub, o repositório `mayccoisa/blog-maykcoisa` tem o domínio personalizado
configurado em Settings > Pages, com HTTPS obrigatório. O exportador grava o arquivo
`CNAME` em `dist-pages/` a cada exportação, então o domínio não se perde no push.

O exportador já usa o domínio por padrão (`SITE_URL=https://blog.maykcoisa.com.br`,
`BASE_PATH` vazio). Para gerar de novo numa subpasta do github.io:

```powershell
$env:SITE_URL = "https://mayccoisa.github.io"; $env:BASE_PATH = "/blog-maykcoisa"
node scripts/exportar-estatico.mjs
```

A exportação limpa `dist-pages/` mas preserva o `.git` da branch `gh-pages`.
