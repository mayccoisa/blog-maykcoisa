# Blog Maykcoisa

Codigo-fonte do blog: tema Ghost, scripts locais e documentacao.

O site publicado vive em <https://mayccoisa.github.io/blog-maykcoisa/> e e gerado a
partir do Ghost local com `node scripts/exportar-estatico.mjs`.

> O Ghost roda somente na maquina local (Docker + SQLite). GitHub Pages serve
> arquivos estaticos, entao o site publicado e um retrato do conteudo no momento
> do export. Para publicar um artigo novo: rode o export e envie a branch
> `gh-pages`.

## Estrutura

```
theme/mayccoisa/     Tema do Ghost (fonte)
scripts/             Inicializador local, instalador do tema, export estatico
ghost/compose.yaml   Ghost 6 em Docker
docs/                Direcao do blog, artigos de exemplo e capturas
visual/              Previa visual estatica da direcao aprovada
```

## Rodando localmente

```powershell
.\scripts\Iniciar-Blog.ps1     # sobe o Ghost em http://localhost:2368
```

## Publicando

```powershell
node scripts/exportar-estatico.mjs
```

Gera `dist-pages/` com o site pronto. Depois, envie essa pasta para a branch
`gh-pages` deste repositorio.
