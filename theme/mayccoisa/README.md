# Tema Mayccoisa

Tema próprio do blog, construído a partir da prévia em `visual/` e adaptado para a
identidade do canal (violeta, coral e marfim).

## Como instalar

O tema vive fora de `ghost/content/` porque essa pasta é ignorada pelo Git. O
script copia `theme/mayccoisa` para `ghost/content/themes/mayccoisa` e reinicia o
Ghost:

```powershell
.\scripts\instalar-tema.ps1              # copia e reinicia
.\scripts\instalar-tema.ps1 -SemReiniciar  # só copia
```

A ativação é feita em **Ghost › Settings › Design › Change theme**, ou pelo campo
`active_theme` nas configurações da publicação.

## Estrutura

```
default.hbs               Layout: head, {{ghost_head}}, header, main, footer
index.hbs                 Home: abertura editorial, destaque, grade, coluna lateral
post.hbs                  Artigo: capa, conteúdo, assuntos, autor, relacionados
page.hbs                  Página estática (Sobre, Contato)
tag.hbs                   Assunto: cabeçalho do assunto + grade
author.hbs                Autor: apresentação + grade
error.hbs                 404
partials/
  header.hbs              Cabeçalho, menu e botão de busca
  footer.hbs              Rodapé
  featured.hbs            Bloco "leitura em destaque" (primeiro artigo da página)
  card.hbs                Card da grade
  sidebar.hbs             Busca, assuntos, lista de leitura e bloco sobre
  pagination.hbs          Paginação da grade
assets/css/main.css       Tokens, componentes e responsivo
assets/js/main.js         Menu mobile
```

## Decisões de layout

- **Dobra da home:** a abertura é um bloco de duas colunas (título à esquerda,
  apresentação à direita) para o destaque e a primeira fileira de notícias
  caberem na tela. Em 1920×912 aparecem o destaque e a primeira fileira com
  imagem, assunto, título e resumo.
- **Destaque automático:** o primeiro artigo da página vira o bloco de destaque
  quando há mais de um artigo; com um único artigo ele aparece como card.
- **Sem imagem de capa:** o card usa um painel tipográfico com o nome do assunto,
  alternando entre três tons da paleta a cada três cards.
- **Busca:** o botão usa `data-ghost-search`, então quem responde é a busca nativa
  do Ghost (Sodo), injetada por `{{ghost_head}}`.
- **Assuntos vazios:** o bloco lateral só aparece quando existe algum assunto com
  artigo publicado, porque o Ghost não cria rota para assunto sem conteúdo.
- **Página Sobre:** `page.hbs` mostra o avatar da marca e o rótulo "Quem escreve"
  quando o slug é `sobre`; nas outras páginas fica só o título e o conteúdo.
- **Capas largas:** `.kg-width-wide` e `.kg-width-full` funcionam dentro da coluna
  de leitura.

## Configurações do tema

`package.json` declara `posts_per_page: 9` e dois textos editáveis em
**Design › Customize**: o título do bloco de assuntos (`topics_label`) e o da
lista de leitura (`reading_list_label`).

## Marca

Imagens vindas do kit oficial `C:\proj\maykcoisa\identidade-visual\kit-violeta-coral`:

| Arquivo do tema | Origem | Uso |
| --- | --- | --- |
| `assets/images/marca.png` | `assets/simbolo.png`, recortado e centralizado em 256×256 | Símbolo no cabeçalho e no rodapé, dentro de um círculo marfim |
| `assets/images/avatar.png` | `assets/avatar.png` em 512×512 | Bloco "Sobre", autor do artigo e página de autor |

O favicon e a imagem de compartilhamento ficam em `ghost/content/` (fora do Git),
porque são configurações da publicação, não do tema:

- `ghost/content/images/maykcoisa/icone.png` — favicon, 256×256, a partir do
  `avatar.png`.
- `ghost/content/images/maykcoisa/compartilhamento.png` — capa do YouTube
  (2560×1440), usada em `og_image` e `twitter_image`.

O símbolo sobre fundo escuro segue a regra do kit: fica dentro de um círculo
marfim (`--paper`), como em `identidade.css` (`.dark .hero-symbol`).


