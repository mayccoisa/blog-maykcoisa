# Blog Mayccoisa

## Direção confirmada pelo dono

Blog pessoal sobre tecnologia, lifestyle e outros assuntos. Referência principal: [Hora de Codar](https://horadecodar.com.br/). O objetivo é uma experiência muito parecida na organização editorial e no visual, com identidade e conteúdo próprios. Formações e venda de cursos ficam fora do escopo.

Ordem combinada: preparar o projeto local, mapear a base existente, trabalhar o visual e depois implementar a adaptação.

## Referência editorial

Consulta da página inicial em 05/11/2026. Elementos observados para avaliar na etapa visual:

* Apresentação do site e acesso ao blog.
* Artigos recentes e conteúdos populares.
* Agrupamento de conteúdo por assunto.
* Cards com categoria, título, resumo e metadados de leitura.
* Busca, categorias e rodapé editorial.

Newsletter, materiais gratuitos e integração com YouTube existem na referência, mas sua inclusão no Mayccoisa ainda não foi definida. A referência não autoriza copiar textos, marca ou imagens de terceiros.

## Base recebida

Repositório: https://github.com/mayccoisa/Blog-Mayccoisa

Pasta local: `C:\proj\producthub\produtos\blog-mayccoisa`.

A branch `main`, no commit `409911f`, contém um site institucional WeON. Stack: Nuxt 3, Vue 3, TypeScript, Tailwind CSS, VueUse e GSAP. O repositório remoto apresenta apenas a branch `main` na consulta inicial.

Há páginas institucionais, produtos, soluções, casos, contato e páginas legais. Existem componentes de navegação, rodapé, identidade, animações e seções reutilizáveis.

Não foram encontradas rotas de blog, listagem de artigos, página de artigo ou CMS implementado. O README original lista CMS para blog e casos como pendência. Isso diverge da expectativa de receber um fork com blog pronto e precisa ser esclarecido antes de definir o reaproveitamento.

O projeto também herda identidade, metadados, Google Tag Manager e integração de atendimento da WeON. Esses pontos precisam entrar no mapeamento da adaptação. Não usar os formulários e o atendimento herdados como ambiente de teste do Mayccoisa.

## Validação da instalação

Dependências instaladas com `npm ci`, preservando o lockfile. `npm run build` concluído com sucesso. Servidor de produção iniciado temporariamente em `127.0.0.1:49381`, com resposta HTTP 200 e HTML na página inicial, e encerrado após a verificação. Nenhuma publicação realizada. A instalação apresentou avisos de dependências obsoletas, sem impedir o build.

## Continuidade

Confrontar esta base com o escopo já existente do Mayccoisa, que não foi localizado nos documentos locais consultados. A conexão MCP do Product Hub não estava disponível nesta sessão, portanto este registro é local e não representa atualização do escopo no Hub.

A base escolhida pelo dono é o Ghost. O ambiente local está configurado em `ghost/compose.yaml`, com conteúdo persistente em `ghost/content/`, ignorado pelo Git. Site em http://localhost:2368 e painel em http://localhost:2368/ghost/, ambos verificados com HTTP 200. A conta administrativa deve ser criada pelo dono no primeiro acesso. A base Nuxt recebida permanece preservada.

Depois mapear páginas, componentes, conteúdo e lacunas do Ghost antes de elaborar o visual. Este documento registra o pedido e a inspeção inicial, sem substituir o escopo anterior ou um PRD.

## Implementação do tema (09/11/2026)

Decisões do dono nesta etapa: adotar a **paleta do canal** (violeta `#7518FF`,
coral `#FF684F`, marfim `#FFFDF6`) em vez do verde escuro da prévia, e implementar
um **tema Ghost próprio** construído a partir de `visual/`, sem partir do Source.

Entregue:

- Tema em `theme/mayccoisa` (default, index, post, page, tag, author, 404 e
  partials de cabeçalho, rodapé, destaque, card, coluna lateral e paginação).
- `scripts/instalar-tema.ps1` copia o tema e reinicia o Ghost.
- Publicação configurada: título, descrição, locale `pt-BR`, fuso
  `America/Sao_Paulo`, cor de destaque, favicon, menu e assuntos Tecnologia,
  Lifestyle e Tudo mais.
- Conteúdo de exemplo do Ghost ("Coming soon" e "About this site") retirado do ar
  como rascunho, para o dono publicar conteúdo próprio.

Pendente: conta de administrador (criada pelo dono), primeiros artigos e a página
Sobre. Enquanto não existe a página, o menu "Sobre o Maycon" aponta para o bloco
`#sobre` da home.

Observações técnicas do Ghost 6 registradas na implementação: cada template
precisa declarar `{{!< default}}`; tag e autor só existem dentro de `{{#tag}}` e
`{{#author}}`; assunto sem artigo publicado não gera rota (404).

## Marca aplicada (09/11/2026)

O kit `C:\proj\maykcoisa\identidade-visual\kit-violeta-coral` trazia a identidade
vigente: símbolo "M" orgânico em violeta com cunha coral, avatar sobre marfim e a
capa do YouTube com o wordmark. O kit confirma a paleta usada no tema
(`#FFFDF6`, `#171322`, `#7518FF`, `#FF684F`, `#6E657A`) e define a regra do
símbolo sobre fundo escuro (dentro de um círculo marfim).

Grafia confirmada pelo dono: **Maykcoisa**, com K, como no logotipo. O nome
"Mayccoisa" do protótipo e do repositório ficou apenas como identificador técnico.

Aplicado: símbolo no cabeçalho e rodapé, avatar no bloco Sobre, autor do artigo e
página de autor, favicon e imagem de compartilhamento a partir da capa do canal.
O kit `logo/` (M geométrico grafite) é a identidade anterior e não foi usada.


