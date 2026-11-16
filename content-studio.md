> ## Content Index
> Fetch the complete content index at: http://localhost:2368/llms.txt
> Use this file to discover other available public pages before exploring further.

# Content Studio: uma ideia, uma peça para cada canal
- URL: http://localhost:2368/content-studio/
- Published: 2026-11-16T09:00:00.000Z
- Updated: 2026-11-16T14:40:16.000Z
- Description: O estúdio editorial que montei para transformar uma ideia em artigo, post, carrossel e roteiro, com revisão e histórico de versões.
- Author: Maycon Rocha
- Tags: Tecnologia

Quando decidi escrever com frequência, percebi que cada canal pedia uma coisa diferente. O blog é onde mostro meus experimentos e converso sobre produto, IA, rotina e produtividade. O LinkedIn apresenta o meu trabalho e leva leitores até aqui. A mesma ideia precisava virar textos diferentes, e eu precisava saber o que estava escrito, o que estava em revisão e o que já podia sair.

O Content Studio é a ferramenta que montei para isso. Comecei em outubro de 2026, e ele roda só no meu computador.

## Uma ideia, várias peças

Tudo começa numa ideia: um título e o que eu quero dizer. Na mesma tela marco os formatos, e cada formato vira uma peça: artigo para o blog, post ou carrossel para o LinkedIn, carrossel e Reels para o Instagram, vídeo longo e Shorts para o YouTube, vídeo curto para o TikTok.

![Lista de conteúdos com uma ideia e duas peças em revisão, cada uma com o canal e o formato](http://localhost:2368/content/images/projetos/content-studio/conteudos.jpg)

A lista separa o que ainda é ideia do que está em revisão. As telas deste artigo usam um conteúdo de exemplo.

## Quem escreve e quem decide

O texto de cada peça é escrito pelo Otavio, um agente de IA que roda fora do aplicativo. Ele lê a ideia, o perfil do canal, as referências e o template escolhido, escreve uma versão e grava pela linha de comando do estúdio. O aplicativo não chama nenhuma IA: ele guarda os registros, as versões e o estado de cada peça.

A decisão continua comigo. Na tela de revisão, o texto fica à esquerda e as decisões à direita: aprovar, devolver com uma nota para o Otavio ou rejeitar. Cada gravação vira uma versão nova, e a anterior continua no histórico.

![Detalhe de uma peça de artigo em revisão, com os botões Aprovar peça, Devolver com nota e Rejeitar peça](http://localhost:2368/content/images/projetos/content-studio/artigo.jpg)

Texto, aprovação, devolução e histórico no mesmo espaço.

## Um perfil para cada canal

Cada canal tem um perfil com finalidade, formatos e identidade próprios. O Maykcoisa é o perfil de criador de conteúdo, com os formatos de vídeo, carrossel e blog. O LinkedIn é o perfil para comunicar meu trabalho, com tom formal, post e carrossel. A seção Voz guarda quem sou, para quem escrevo, o tom e o que evitar, e isso orienta toda peça do perfil.

![Tela de perfis com os cartões Maykcoisa e LinkedIn, cada um com seus formatos e cores](http://localhost:2368/content/images/projetos/content-studio/perfis.jpg)

Perfis separam finalidade, formatos e identidade de cada canal.

## Um design system para a interface

A primeira versão da tela de revisão mudou antes de eu comparar alternativas. Pedi três protótipos com o mesmo conteúdo: Leitura, Revisão e Contexto. Escolhi o Contexto, com o texto à esquerda e as decisões à direita. Depois veio um protótipo navegável de 15 telas e um design system com os componentes usados de verdade no produto.

![Catálogo do design system com cores, canais, campos editoriais e estados das peças](http://localhost:2368/content/images/projetos/content-studio/design-system.jpg)

O catálogo vivo mostra os mesmos componentes das telas.

O código do Content Studio fica num repositório privado. Os outros projetos que estou construindo estão na [página de projetos](http://localhost:2368/projetos/).