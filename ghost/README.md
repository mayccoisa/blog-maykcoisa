# Ghost local do Mayccoisa

Ambiente de desenvolvimento com Docker Compose e Ghost 6. O site fica em http://localhost:2368 e o painel em http://localhost:2368/ghost/.

Os artigos, imagens, temas instalados e banco SQLite persistem em `content/`, fora do Git. Essa pasta precisa de backup para preservar o conteúdo. Não remover volumes ou conteúdo para reiniciar o blog.

O ambiente usa modo de desenvolvimento. A arquitetura e a hospedagem de produção serão definidas em etapa própria.

Para iniciar, executar `docker compose up -d` nesta pasta. Para parar, executar `docker compose stop`. Para verificar, executar `docker compose ps`.

O dono cria a conta administrativa no primeiro acesso ao painel. O cadastro local não publica o site na internet.

## Atalho de teste

Na pasta Apps pessoais da área de trabalho, o atalho **Blog Mayccoisa** inicia o Docker quando necessário, sobe este Ghost e abre a prévia visual em http://localhost:4318. O painel permanece disponível em http://localhost:2368/ghost/.

O inicializador está em `scripts/Iniciar-Blog.ps1`, na raiz do repositório, e aceita `-SemAbrir` para verificar a prontidão sem abrir o navegador. Ele reutiliza o servidor visual quando já está respondendo. Os logs ficam em `%LOCALAPPDATA%\AppsPessoais\logs\blog-mayccoisa`.

O cadastro usa o catálogo `C:\proj\apps-pessoais\apps.json`, como os demais aplicativos pessoais. `scripts/Registrar-Atalhos.ps1` recria os dois atalhos dos blogs sem remover outros. O botão geral Parar apps abertos não gerencia esses contêineres; para interromper o Ghost, usar `docker compose stop` nesta pasta.
