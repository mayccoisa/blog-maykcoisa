# Proposta visual do Mayccoisa

Prévia local em http://localhost:4318, servida por `node visual/server.mjs` a partir da raiz do repositório. Ainda não é o tema ativo do Ghost. Conteúdo, datas e tempos de leitura são exemplos para avaliação visual.

## Direção proposta

Referência: https://horadecodar.com.br/. Preserva a ideia de cabeçalho escuro, abertura editorial, artigos e coluna com busca e assuntos. Propõe verde escuro, superfície clara, títulos Manrope e texto DM Sans. Não inclui cursos, formações, captação de newsletter ou venda de produtos. O nome usa uma composição tipográfica provisória, sem substituir uma marca definitiva.

## Componentes e correspondência prevista com o Ghost

| Região visual | Conteúdo previsto |
| --- | --- |
| Cabeçalho | Nome do site e navegação |
| Destaque | Um artigo selecionado editorialmente |
| Últimas descobertas | Artigos recentes |
| Assuntos | Tags editoriais |
| Busca | Busca do site, a integrar na implementação |
| Lista de leitura | Curadoria editorial, sem inventar métricas de popularidade |
| Sobre | Apresentação do autor |
| Prévia de leitura | Direção tipográfica; a implementação terá página própria de artigo |

Fotos ilustrativas remotas do Unsplash. Fontes remotas do Google Fonts. Na implementação do tema, definir os arquivos finais e a estratégia de hospedagem desses recursos.

## Verificação realizada

JavaScript validado com `node --check`. Filtro Lifestyle retornou dois artigos. Prévia de leitura abriu com foco no botão de fechar e foi fechada por Escape. Versão móvel verificada com viewport de 390 × 844, sem transbordamento horizontal; ambas as fotos carregaram. Versão desktop inspecionada no navegador. Captura em `previa-desktop.png`.

## Próxima entrega

Refinar esta direção com o dono e implementar o tema do Ghost com os dados reais. Definir as páginas Sobre e Contato e a navegação final nessa etapa. A apresentação e os assuntos desta prévia são propostas, não decisões editoriais definitivas.
