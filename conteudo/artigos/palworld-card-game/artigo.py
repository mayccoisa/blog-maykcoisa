ARTIGO = {'titulo': 'Palworld Card Game: aprender um jogo de cartas jogando contra o computador',
 'resumo': 'Como construí, sem saber desenvolver jogos, um jogo de cartas de fã do Palworld organizando o '
           'trabalho dos agentes de IA.',
 'assunto': 'tecnologia',
 'status': 'published',
 'publicado': '2026-11-16 10:00:00',
 'capa': 'mesa-principal.jpg',
 'capa_alt': 'Mesa de duelo do Palworld Card Game no terceiro turno, com as cartas do jogador e do bot em '
             'campo',
 'blocos': [('p',
             'Palworld foi o jogo que mais joguei neste ano, daqueles que me davam vontade de ligar o PC só '
             'para desbravar o mundo e descobrir o que havia de novo. Os monstros, os itens, os biomas e as '
             'dungeons me faziam querer continuar naquele universo, e essa vontade também me levou ao jogo '
             'de cartas.'),
            ('p',
             'Como as cartas físicas não estavam ao meu alcance aqui no Brasil, resolvi construir uma versão '
             'para jogar contra o computador e aprender as regras na prática. Eu ainda não sabia desenvolver '
             'jogos, então parti do que já sabia fazer: montar um bom harness para organizar o trabalho dos '
             'agentes de IA e aprender durante a construção.'),
            ('p',
             'Esse é o Palworld Card Game que construí como fã, um projeto independente, sem ligação com a '
             'Pocketpair ou a Bushiroad.'),
            ('h2', 'Aprender as regras jogando'),
            ('p',
             'A proposta é montar um baralho e jogar uma partida contra o computador, com o próprio jogo '
             'aplicando as regras. O tutorial e o modo de treino ajudam a começar; depois dá para '
             'experimentar no duelo livre e voltar ao construtor de baralhos para ajustar as escolhas.'),
            ('p',
             'Feito em Godot, o projeto tem português e inglês, versões para PC e Android e suporte a '
             'controle.'),
            ('h2', 'Como organizei o desenvolvimento com IA'),
            ('p',
             'Harness é a estrutura em volta dos agentes de IA: as instruções que eles recebem, a descrição '
             'das tarefas, os limites do que podem alterar e a maneira de conferir a entrega. No meu '
             'projeto, essa organização começa na pasta do jogo, com o escopo escrito e um plano de '
             'implementação que serve de referência para as tarefas.'),
            ('img',
             {'arquivo': 'game-hub-tarefas.jpg',
              'alt': 'Projeto Palworld aberto no Game Hub, com tarefas organizadas por etapa e progresso.',
              'legenda': 'O quadro do Palworld no Game Hub reúne os pedidos, o andamento da execução e as '
                         'tarefas que aguardam meu teste.'}),
            ('p',
             'No GDD, documento que descreve o jogo, defini o recorte inicial: rodar em Windows, ter '
             'partidas contra um bot e usar as cartas disponíveis, com regras automáticas e português, sem '
             'uma economia para administrar. Assim, havia um escopo para consultar quando surgissem novas '
             'ideias ou problemas.'),
            ('img',
             {'arquivo': 'game-hub-escopo.jpg',
              'alt': 'Documento de escopo do Palworld aberto no Game Hub, com a visão do jogo e o objetivo '
                     'da experiência.',
              'legenda': 'O escopo fica dentro do projeto e descreve o jogo que quero construir antes de '
                         'detalhar a implementação.'}),
            ('p',
             'O plano de implementação divide esse escopo em etapas, cada uma com critérios para verificar a '
             'entrega. As tarefas detalham o que precisa ser feito e guardam o plano de execução, o relato '
             'da implementação e as verificações, de modo que eu consigo acompanhar o que o agente alterou e '
             'o que ainda precisa de revisão.'),
            ('p',
             'Meu papel é definir o que quero e observar o jogo funcionar para apontar o que precisa mudar, '
             'inclusive quando um problema só aparece durante uma partida.'),
            ('h2', 'Quando comprar uma carta parecia comprar várias'),
            ('p',
             'Durante uma partida, percebi que a animação da compra parecia puxar cartas várias vezes e '
             'relatei o problema na tarefa PAL-0016. O diagnóstico registrado nela encontrou uma causa '
             'específica: os eventos de compra estavam animando as últimas cartas do estado final da mão.'),
            ('img',
             {'arquivo': 'game-hub-tarefa-plano.jpg',
              'alt': 'Tarefa PAL-0016 aberta no Game Hub, com o diagnóstico da animação e os quatro passos '
                     'do plano marcados.',
              'legenda': 'O problema que percebi jogando virou uma tarefa com diagnóstico e passos de '
                         'execução registrados.'}),
            ('p',
             'A correção organizou as animações em uma fila por lote de compra, e o relatório de verificação '
             'registrou oito voos de cartas para oito cartas compradas em uma partida. A tarefa segue em '
             'revisão, portanto esse resultado é o registro da verificação feita, ainda sem aprovação '
             'final.'),
            ('img',
             {'arquivo': 'game-hub-tarefa-verificacao.jpg',
              'alt': 'Relatório da tarefa PAL-0016 no Game Hub com instruções de teste e a verificação de '
                     'oito cartas compradas para oito animações.',
              'legenda': 'O relatório explica como testar e registra a verificação realizada. A tarefa '
                         'continua aguardando minha revisão.'}),
            ('p',
             'Continuo aprendendo a desenvolver jogos com IA enquanto construo uma forma de jogar cartas '
             'naquele universo que tanto gostei de explorar. Para quem quiser experimentar também, as '
             'versões estão na [página de downloads do '
             'projeto](https://github.com/mayccoisa/palworld-card-game-releases/releases/latest).')]}
