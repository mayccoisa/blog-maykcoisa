> ## Content Index
> Fetch the complete content index at: http://localhost:2368/llms.txt
> Use this file to discover other available public pages before exploring further.

# Palworld Card Game: aprender um jogo de cartas jogando contra o computador
- URL: http://localhost:2368/palworld-card-game/
- Published: 2026-11-16T10:00:00.000Z
- Updated: 2026-11-16T14:40:16.000Z
- Description: Um projeto de estudo em Godot que virou jogo completo: tutorial, 28 duelistas, catálogo com 154 cartas, controle do Xbox e versão para Android.
- Author: Maycon Rocha
- Tags: Tecnologia

O Palworld Card Game nasceu em outubro de 2026 com um objetivo de estudo: entender o Palworld OFFICIAL CARD GAME, o jogo de cartas físico da Bushiroad, jogando partidas no computador. Eu queria ver custos, ataques e combinações acontecendo, com as regras aplicadas na hora e a explicação de cada resultado.

Cinco semanas depois, ele está na versão 0.14.0, roda no Windows e no Android e tem um modo para cada momento de quem está aprendendo.

![Menu inicial com o botão Jogar, o botão Baralhos e um Pal em destaque](http://localhost:2368/content/images/projetos/palworld-card-game/menu.jpg)

O menu da versão 0.14.0: Jogar, Baralhos e um Pal em destaque que troca sozinho.

## O que é

É um jogo digital feito em Godot. Você monta um baralho com as cartas do jogo oficial e enfrenta um bot. O motor aplica as regras sozinho: impede a jogada ilegal e diz o motivo. A interface é em português ou inglês, e o efeito de cada carta pode ser lido nas duas línguas.

É um jogo de fã, sem ligação com a Pocketpair ou a Bushiroad. Não tem loja, moeda nem desbloqueio: todas as cartas ficam disponíveis desde o começo.

## Três jeitos de jogar

- Tutorial: uma batalha guiada que passa por todas as fases e mecânicas e termina com a sua vitória.
- Treino de combate: abre direto uma partida com baralhos prontos, para quem quer jogar sem preparar nada.
- Duelo Livre: 28 duelistas, entre decks oficiais, campeões de torneio e listas da comunidade, com placar salvo.

![Tela Escolha como jogar com os cartões Tutorial, Treino de combate e Duelo Livre](http://localhost:2368/content/images/projetos/palworld-card-game/seletor-modos.jpg)

Todos os modos são contra o bot, na própria máquina.

## A mesa

A partida segue as regras oficiais: baralho de 50 cartas, Souls que entram duas por turno e as fases Preparar, Comprar, Souls, Principal e Encerrar. Quem começa é decidido no pedra, papel e tesoura. Os painéis mostram a vida, as Souls disponíveis e o que dá para fazer naquele momento.

![Mesa de duelo com Pals em campo, a mão do jogador embaixo e a barra de fases no centro](http://localhost:2368/content/images/projetos/palworld-card-game/mesa-principal.jpg)

A barra do centro mostra a fase atual e leva ao fim do turno.

Na 0.14.0 entraram as animações no estilo dos jogos de cartas de console: invocação em três tempos, corte de ativação quando alguém joga um Evento, ataque com rastro e zoom e um letreiro no golpe final. Todas pulam com um clique, e a opção reduzir movimento troca cada uma por um fade curto.

![Tela de apresentação do duelo com o jogador à esquerda, o adversário Azarys à direita e VS no centro](http://localhost:2368/content/images/projetos/palworld-card-game/mesa-vs.jpg)

Antes de cada duelo, a apresentação dos dois lados.

## Baralhos e catálogo

O catálogo reúne as 154 cartas, com busca e filtros por cor, tipo e custo. O construtor confere as regras do baralho enquanto você monta, e os decks prontos podem ser copiados para editar.

![Catálogo com a grade de cartas e os filtros por cor no topo](http://localhost:2368/content/images/projetos/palworld-card-game/catalogo.jpg)

154 cartas, 96 Pals, 9 elementos e 289 artes.

## No PC, no controle e no celular

O jogo funciona inteiro no controle do Xbox, com uma faixa no rodapé que mostra os botões válidos em cada tela. No Android, a interface se ajusta a tablet e celular e o toque longo numa carta abre os detalhes.

![Tela do Duelo Livre no formato de celular, com a grade de duelistas e o botão Duelar](http://localhost:2368/content/images/projetos/palworld-card-game/duelo-livre-mobile.jpg)

Duelo Livre no celular: toque e segure para ver as cartas de cada duelista.

## Como cada versão sai

Antes de publicar, um script roda as baterias de regras e de combate, joga uma partida pelo mouse conferindo o que está sob o cursor e captura 15 telas no PC e no celular para comparar com a versão anterior. Só depois os pacotes de Windows e Android são gerados. Dentro do jogo, o botão Atualizar avisa quando existe versão nova.

## Onde baixar

O instalador para Windows, a versão portátil e o APK para Android ficam na [página de downloads no GitHub](https://github.com/mayccoisa/palworld-card-game-releases/releases/latest?ref=localhost). O código do jogo fica num repositório privado. Os outros projetos estão na [página de projetos](http://localhost:2368/projetos/).