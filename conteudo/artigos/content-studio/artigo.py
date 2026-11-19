ARTIGO = {'titulo': 'Como o Content Studio organiza a produção de artigos do Maykcoisa',
 'resumo': 'O estúdio editorial que montei para transformar uma ideia em artigo, post, carrossel e '
           'roteiro, com revisão e histórico de versões.',
 'assunto': 'tecnologia',
 'status': 'published',
 'publicado': '2026-11-16 09:00:00',
 'capa': 'artigo.jpg',
 'capa_alt': 'Tela de revisão do Content Studio com o texto de um artigo à esquerda e as decisões '
             'de aprovação à direita',
 'blocos': [('p',
             'Sempre tive vontade de ter um blog. Agora que estou tirando essa ideia do papel, '
             'quero encontrar uma forma de mantê-lo que caiba junto da minha rotina de trabalho '
             'CLT, com tempo para preparar os assuntos e voltar aos textos quando puder dar '
             'atenção a eles.'),
            ('p',
             'O Maykcoisa é onde quero mostrar os projetos que estou construindo e um pouco de '
             'como trabalho com produto, além das experiências pessoais que surgem pelo caminho. '
             'Para alimentar esse espaço, preciso organizar as ideias e saber quais textos estão '
             'prontos, quais precisam de ajustes e quais ainda quero desenvolver.'),
            ('p',
             'Comecei a construir o Content Studio em outubro de 2026 para cuidar desse trabalho. '
             'Ele roda no meu computador e reúne a preparação dos conteúdos, as versões dos textos '
             'e as decisões de revisão. É um dos produtos que estou criando com ajuda de IA para '
             'dar continuidade a outras ideias, neste caso, o próprio blog.'),
            ('h2', 'Voltar ao texto sem perder o contexto'),
            ('p',
             'Quando abro o Studio, encontro o estado de cada peça e posso continuar de onde '
             'parei. Uma ideia pode virar um artigo para o blog e um post para o LinkedIn, cada um '
             'com sua função: no artigo há espaço para desenvolver uma experiência; no post posso '
             'apresentar o assunto e convidar para a leitura.'),
            ('p',
             'A mesma organização também atende carrosséis e roteiros de vídeo. Escolho os '
             'formatos na ideia, e cada um vira uma peça que pode ser escrita e revisada '
             'separadamente. Isso me permite acompanhar o conteúdo sem depender da última resposta '
             'de uma conversa para lembrar o que ainda falta fazer.'),
            ('img',
             {'arquivo': 'conteudos.jpg',
              'alt': 'Lista de conteúdos com uma ideia e duas peças em revisão, cada uma com o '
                     'canal e o formato.'}),
            ('p',
             'A lista separa o que ainda é ideia do que está em revisão. As telas deste artigo '
             'usam um conteúdo de exemplo.'),
            ('p',
             'Na revisão, leio o texto à esquerda e encontro as decisões à direita. Posso editar, '
             'aprovar, rejeitar ou devolver com uma nota explicando o que precisa mudar. Cada '
             'gravação cria uma versão nova, enquanto a anterior permanece no histórico.'),
            ('img',
             {'arquivo': 'artigo.jpg',
              'alt': 'Detalhe de uma peça de artigo em revisão, com os botões Aprovar peça, '
                     'Devolver com nota e Rejeitar peça.',
              'largura': 'wide'}),
            ('p',
             'O histórico e as informações de apoio ficam junto do texto. Posso deixá-lo '
             'aguardando e voltar para revisar em outro momento; aprovar no Studio continua sendo '
             'uma etapa diferente de publicar no blog.'),
            ('h2', 'Como o agente participa da escrita'),
            ('p',
             'O agente que me ajuda a escrever se chama Otavio e trabalha fora do aplicativo. Ele '
             'consulta o pedido, considera minha voz, as referências e o template escolhido, '
             'quando houver, e grava uma versão para revisão pela linha de comando do Studio.'),
            ('p',
             'Cada canal tem um perfil com finalidade e formatos próprios. O LinkedIn comunica meu '
             'trabalho com um tom mais formal, enquanto o Maykcoisa reúne os conteúdos de criador, '
             'incluindo o blog. A seção Voz guarda quem sou, para quem escrevo e as orientações de '
             'tom e do que evitar.'),
            ('img',
             {'arquivo': 'perfis.jpg',
              'alt': 'Tela de perfis com os cartões Maykcoisa e LinkedIn, cada um com seus '
                     'formatos e cores.'}),
            ('p',
             'Os perfis ajudam o agente a preparar cada peça para o canal em que será usada, sem '
             'tratar um artigo como se fosse um roteiro de vídeo.'),
            ('p',
             'Para escrever artigos, o Otavio consulta a skill `escrever-blog`. Quando chego com '
             'um assunto ainda pouco desenvolvido, ela orienta uma conversa para aproveitar o que '
             'já contei e aprofundar as partes vagas. Antes de redigir, o agente apresenta sua '
             'interpretação e uma proposta de estrutura para eu confirmar. Se já forneci o '
             'material ou pedi uma revisão específica, ele segue a partir desse contexto.'),
            ('p',
             'Depois da redação, entra a `humanizer`. Adaptei para o projeto a [Humanizer, de '
             'blader](https://github.com/blader/humanizer), com orientações de português e de '
             'ritmo para os meus textos. Quero mais continuidade entre as ideias e menos frases '
             'picadas, preservando os fatos e o que estou tentando dizer.'),
            ('p',
             'O arquivo de instruções do Otavio e essas skills ficam junto do projeto, nas pastas '
             '`.claude/agents/` e `.claude/skills/`. Quando identifico um problema recorrente na '
             'escrita, posso ajustar a orientação correspondente e acompanhar a alteração pelo '
             'Git. O texto resultante volta para minha leitura antes de eu decidir o que fazer com '
             'ele.'),
            ('h2', 'Construir a ferramenta e ajustar o uso'),
            ('p',
             'A aplicação usa Next.js e guarda os dados localmente em SQLite. As regras de negócio '
             'ficam em uma camada de serviços usada pela interface, pelo CLI e pelo servidor MCP '
             'local, que permite o acesso editorial de clientes compatíveis. O aplicativo organiza '
             'o contexto, valida os conteúdos recebidos e mantém as versões; a chamada ao modelo '
             'de IA acontece no agente que trabalha fora dele.'),
            ('p',
             'Essa divisão permite ajustar as orientações de escrita sem precisar alterar a '
             'interface. Também deixa claro onde tomo as decisões: quando devolvo um artigo com a '
             'observação de que ficou técnico demais, por exemplo, o Otavio prepara outra versão e '
             'eu posso comparar o resultado com o que pedi.'),
            ('p',
             'A interface também passou por revisão. Pedi três protótipos com o mesmo conteúdo, '
             'chamados Leitura, Revisão e Contexto, e escolhi o Contexto, com a leitura à esquerda '
             'e as decisões à direita. Depois vieram um protótipo navegável de 15 telas e um '
             'design system com os componentes usados no produto.'),
            ('img',
             {'arquivo': 'design-system.jpg',
              'alt': 'Catálogo do design system com cores, canais, campos editoriais e estados das '
                     'peças.'}),
            ('p',
             'O catálogo mostra os mesmos componentes das telas, o que ajuda a manter as escolhas '
             'de interface conforme o aplicativo muda.'),
            ('h2', 'Um blog que eu consiga continuar mantendo'),
            ('p',
             'Quero usar o Content Studio no dia a dia para perceber o que está faltando e o que '
             'ficou mais complicado do que precisava. Isso inclui tanto a ferramenta quanto as '
             'instruções de escrita. A intenção é conseguir desenvolver os assuntos, revisar com '
             'calma e manter o blog enquanto concilio os projetos pessoais com o trabalho.'),
            ('p',
             'Construir um jogo de fã de Palworld e construir uma ferramenta para cuidar do blog '
             'atendem a vontades diferentes. São dois exemplos do que estou conseguindo '
             'experimentar com IA, levando para os projetos o trabalho de definir o que quero e '
             'conferir o que foi entregue.'),
            ('p',
             'O código do Studio está em um repositório privado. Os outros projetos estão na '
             '[página de projetos do Maykcoisa](https://blog.maykcoisa.com.br/projetos/), onde '
             'também quero compartilhar as decisões e os ajustes que forem surgindo.'),
            ('p',
             'Quando construir fica fácil, o que você tira do papel? Se você criou alguma '
             'ferramenta para manter uma ideia funcionando na sua rotina, conte como ela entrou no '
             'seu dia a dia.')]}
