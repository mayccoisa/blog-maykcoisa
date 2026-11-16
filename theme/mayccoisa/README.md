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
index.hbs                 Home: abertura editorial, destaque, projetos, grade, coluna lateral
post.hbs                  Artigo: capa, conteúdo, assuntos, autor, relacionados
page.hbs                  Página estática (Sobre, Contato)
page-projetos.hbs         Página /projetos/: abertura, filtros, destaque, grade, bastidores
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
  projetos/dados.hbs      Lista curada dos projetos (uma chamada por projeto)
  projetos/item.hbs       Card do projeto nos modos destaque, grade e home
  projetos/selo.hbs       Selo Público, Privado ou Código privado
  projetos/link.hbs       Link do card ou "Sem link público"
  projetos/total.hbs      Número total de projetos
assets/css/main.css       Tokens, componentes e responsivo
assets/js/main.js         Filtros e "Mostrar mais" dos projetos, menu mobile
```

## Projetos

A vitrine é uma lista curada à mão, sem API do GitHub. O Ghost não deixa o template
ler um JSON do tema, então os dados ficam em `partials/projetos/dados.hbs`: cada
projeto é uma chamada ao partial `projetos/item` com os campos descritos no topo do
arquivo. Tudo é renderizado no servidor, por isso a lista completa aparece sem JS e
entra inteira no export estático. O JS só liga os filtros (com as contagens) e, no
celular, recolhe a grade em três cards com o botão "Mostrar mais".

- **Página:** `/projetos/` é uma página do Ghost de slug `projetos`, que usa
  `page-projetos.hbs` sozinha. `scripts/criar-projetos.py` cria a página e põe
  "Projetos" no menu, logo depois de "Blog" (Ghost parado).
- **Home:** o bloco "Projetos em andamento" mostra os projetos com `home="sim"`, na
  ordem da lista.
- **Destaque:** o projeto com `destaque="sim"` vira o bloco grande da página e sai da
  grade.
- **Regras do card:** `acesso="publico"` mostra "Público" e o link do repositório;
  `"privado"` mostra o cadeado e "Sem link público"; `"entrega"` mostra "Código
  privado" e o link da entrega (downloads ou site).
- **Capas:** `partials/projetos/capa.hbs` desenha a capa de cada projeto em SVG, com
  fundo e motivo pelo tipo (cartas, biblioteca, terminal ou quadro) e a `sigla` em
  destaque, sempre em 16:9. Para usar uma imagem real, preencha `capa` com o
  endereço; ela entra com o mesmo duotom das capas dos artigos.
- **Primeira dobra:** a capa do destaque da home acompanha a altura da tela
  (`clamp(240px, 100vh - 440px, 420px)`), para o começo dos projetos aparecer em
  1280×720, 1366×768 e 390×844. No celular a capa do destaque fica em 2:1, o resumo
  some e a data divide a linha com "Ler o artigo", para o topo da primeira capa de
  projeto aparecer também em 375×812.
- **Ao incluir ou tirar um projeto,** atualize também `partials/projetos/total.hbs`.
- Evite campos com nome de helper do Ghost (`link`, `date`, `url`): o Handlebars
  chama o helper no lugar do valor.

## Decisões de layout

- **Dobra da home:** a abertura é um bloco de duas colunas (título à esquerda,
  apresentação à direita) para o destaque e a primeira fileira de notícias
  caberem na tela. Em 1920×912 aparecem o destaque e a primeira fileira com
  imagem, assunto, título e resumo.
- **Destaque automático:** o primeiro artigo da página vira o bloco de destaque
  quando há mais de um artigo; com um único artigo ele aparece como card.
- **Sem imagem de capa:** o card usa um painel tipográfico com o nome do assunto,
  alternando entre três tons da paleta a cada três cards.
- **Capas em duotom:** toda foto de capa (card, destaque e artigo) passa pela classe
  `.duo`, que converte a imagem para violeta escuro e lavanda. Fotos de origens
  diferentes ficam com cara de série. Sem foto, o destaque mostra a janela de código.
- **Refino de 16/11/2026:** menos molduras (seções separadas por espaço e linhas
  finas), rótulos sem caixa alta, texto mínimo de 13 px, títulos em peso 700,
  cabeçalho sem botão de chamada e citação entre duas linhas, sem barra lateral.
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


