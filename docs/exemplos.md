# Artigos de exemplo

Seis artigos fictícios para testar o tema, a navegação e a leitura. Todos podem
ser apagados sem prejuízo: nenhum dado real depende deles.

| Artigo | Assunto | Data | Destaque |
| --- | --- | --- | --- |
| Da ideia ao primeiro projeto: por onde começar com IA | Tecnologia | 08/11/2026 | não |
| Um setup que trabalha a seu favor | Tecnologia | 05/11/2026 | sim |
| Desligar também faz parte do processo | Lifestyle | 02/11/2026 | não |
| O prazer de aprender uma coisa só por curiosidade | Tudo mais | 29/10/2026 | sim |
| As ferramentas certas são as que você realmente usa | Tecnologia | 24/10/2026 | não |
| Pequenos rituais para um dia com mais respiro | Lifestyle | 20/10/2026 | sim |

Os três marcados como destaque aparecem em **Na lista de leitura**, na coluna
lateral.

## Como recriar ou remover

O Ghost precisa estar parado, porque o SQLite não aceita dois escritores:

```powershell
docker compose -f ghost/compose.yaml stop
python scripts/criar-exemplos.py            # cria (ignora os que já existem)
python scripts/criar-exemplos.py --remover  # apaga os seis
docker compose -f ghost/compose.yaml start
```

O script faz uma cópia de segurança do banco em `ghost/content/data/` antes de
qualquer alteração e usa os assuntos já cadastrados (tecnologia, lifestyle,
tudo-mais).

## Imagens

As capas estão em `ghost/content/images/exemplos/`, em 1600 × 1000. São fotos do
Unsplash escolhidas para ilustrar cada assunto — não são material do canal e não
devem ir para produção. Ao publicar conteúdo real, troque as capas pelo material
próprio.

## O que ainda não é exercitado

- **Paginação:** são 6 artigos e o tema mostra 9 por página, então a paginação não
  aparece. Para testar, publique mais de 9 ou reduza `posts_per_page` em
  `theme/mayccoisa/package.json`.
- **Busca:** o botão abre a busca nativa do Ghost (Sodo). Funciona com o conteúdo
  publicado, inclusive os exemplos.
