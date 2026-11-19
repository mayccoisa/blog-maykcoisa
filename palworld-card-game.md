> ## Content Index
> Fetch the complete content index at: http://localhost:2368/llms.txt
> Use this file to discover other available public pages before exploring further.

# Quando construir fica fácil, o que você tira do papel?
- URL: http://localhost:2368/palworld-card-game/
- Published: 2026-11-16T10:00:00.000Z
- Updated: 2026-11-19T00:46:48.000Z
- Description: Como construí, sem saber desenvolver jogos, um jogo de cartas de fã do Palworld organizando o trabalho dos agentes de IA.
- Author: Maycon Rocha
- Tags: Tecnologia

Palworld foi o jogo que mais joguei neste ano. Eu ligava o PC com vontade de voltar àquele mundo, explorar os biomas e descobrir monstros, itens e dungeons. Queria continuar aquela experiência, e essa vontade também me levou ao jogo de cartas.

As cartas físicas não estavam ao meu alcance aqui no Brasil. Resolvi, então, construir uma versão em que pudesse jogar contra o computador e aprender as regras durante as partidas. Eu ainda não sabia desenvolver jogos, mas já vinha aprendendo a organizar o trabalho de agentes de IA e quis usar essa experiência para tentar.

O Palworld Card Game é uma das ideias pessoais que consegui tirar do papel dessa forma. A maior parte dos meus projetos está ligada a produto e à maneira como trabalho; este começou pela vontade de jogar. Para construí-lo, precisei explicar o que queria, definir o recorte e acompanhar o que os agentes entregavam.

É um projeto independente de fã, sem ligação com a Pocketpair ou a Bushiroad.

## Um jogo para aprender jogando

A proposta é montar um baralho e disputar uma partida contra o computador, com o próprio jogo aplicando as regras. O tutorial e o modo de treino ajudam a começar. Depois, dá para experimentar no duelo livre e voltar ao construtor de baralhos para ajustar as escolhas.

Construí o projeto em Godot. Ele tem português e inglês, versões para PC e Android e suporte a controle. O recorte inicial era menor: rodar em Windows, ter partidas contra um bot e usar as cartas disponíveis, com regras automáticas e português, sem uma economia para administrar.

Esse recorte ficou registrado no GDD, o documento que descreve o jogo. Era uma referência para consultar quando surgissem novas ideias ou problemas, em vez de decidir tudo de novo a cada pedido.

![Documento de escopo do Palworld aberto no Game Hub, com a visão do jogo e o objetivo da experiência.](https://blog.maykcoisa.com.br/content/images/projetos/palworld-card-game/game-hub-escopo.jpg)

O escopo descreve o jogo que quero construir antes de detalhar a implementação.

## Como passei a ideia para os agentes

Parti de algo que já sabia fazer: montar um harness. Esse nome reúne a estrutura em volta dos agentes de IA, como as instruções, as tarefas que recebem, os limites do que podem alterar e a maneira de conferir a entrega.

No projeto, essa organização começa na pasta do jogo, com o escopo escrito e um plano de implementação. O plano divide o trabalho em etapas e define critérios para verificar cada entrega. As tarefas guardam os pedidos, o relato da implementação e as verificações realizadas.

![Projeto Palworld aberto no Game Hub, com tarefas organizadas por etapa e progresso.](https://blog.maykcoisa.com.br/content/images/projetos/palworld-card-game/game-hub-tarefas.jpg)

O quadro do Palworld no Game Hub reúne o andamento da execução e as tarefas que aguardam meu teste.

Assim consigo acompanhar o que o agente alterou e o que ainda precisa de revisão. Meu papel inclui observar o jogo funcionando e apontar o que precisa mudar, inclusive quando um problema só aparece durante uma partida.

## Uma compra de carta que parecia acontecer várias vezes

Durante uma partida, percebi que a animação de compra parecia puxar cartas várias vezes. Registrei o problema na tarefa PAL-0016\. O diagnóstico encontrou uma causa específica: os eventos de compra estavam animando as últimas cartas do estado final da mão.

![Tarefa PAL-0016 aberta no Game Hub, com o diagnóstico da animação e os quatro passos do plano marcados.](https://blog.maykcoisa.com.br/content/images/projetos/palworld-card-game/game-hub-tarefa-plano.jpg)

A observação feita durante a partida virou uma tarefa com diagnóstico e passos de execução registrados.

A correção organizou as animações em uma fila por lote de compra. O relatório de verificação registrou oito voos de cartas para oito cartas compradas em uma partida; a tarefa continua em revisão, portanto esse é o resultado registrado na verificação, ainda sem minha aprovação final.

![Relatório da tarefa PAL-0016 no Game Hub com instruções de teste e a verificação de oito cartas compradas para oito animações.](https://blog.maykcoisa.com.br/content/images/projetos/palworld-card-game/game-hub-tarefa-verificacao.jpg)

O relatório explica como testar a correção e o que foi conferido antes da minha revisão.

## Dar continuidade à vontade de criar

Estou aprendendo a desenvolver jogos enquanto construo uma forma de continuar naquele universo. A IA tornou essa tentativa possível para mim, e o trabalho de explicar a ideia, organizar as etapas e conferir o resultado foi ganhando forma junto com o jogo.

Para quem quiser jogar também, as versões estão na [página de downloads do projeto](https://github.com/mayccoisa/palworld-card-game-releases/releases/latest?ref=localhost).

Quando construir fica fácil, o que você tira do papel? Se uma vontade antiga já virou projeto com ajuda de IA, vou gostar de conhecer o que você fez.