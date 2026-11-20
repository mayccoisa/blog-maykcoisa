/*
 * Busca de artigos e projetos que funciona sem servidor.
 * O site publicado é estático (GitHub Pages), então a busca do Ghost não existe lá.
 * Os artigos vêm do RSS (rss.xml no site estático, /rss/ no Ghost local) e os
 * projetos vêm da própria página /projetos/. Tudo é lido uma vez, na primeira busca.
 */
(function () {
    const gatilhos = document.querySelectorAll('[data-busca]');
    if (!gatilhos.length) return;

    const marca = document.querySelector('.brand');
    // Usa só o caminho do link da marca: os dados vêm sempre da mesma origem da página
    const caminhoRaiz = new URL(marca ? marca.getAttribute('href') : '/', location.href).pathname;
    const raiz = location.origin + caminhoRaiz.replace(/\/?$/, '/');

    let indice = null;
    let carregando = null;

    const normalizar = (texto) =>
        (texto || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

    async function texto(url) {
        const resposta = await fetch(url);
        if (!resposta.ok) throw new Error(String(resposta.status));
        return resposta.text();
    }

    async function lerArtigos() {
        let xml = null;
        for (const caminho of ['rss.xml', 'rss/']) {
            try {
                xml = await texto(raiz + caminho);
                break;
            } catch {
                /* tenta o próximo endereço */
            }
        }
        if (!xml) return [];
        const doc = new DOMParser().parseFromString(xml, 'application/xml');
        return [...doc.querySelectorAll('item')].map((item) => {
            const resumo = new DOMParser()
                .parseFromString(item.querySelector('description')?.textContent || '', 'text/html')
                .body.textContent.trim();
            return {
                tipo: 'Artigo',
                rotulo: item.querySelector('category')?.textContent || 'Artigo',
                titulo: item.querySelector('title')?.textContent || '',
                resumo,
                url: item.querySelector('link')?.textContent || raiz,
            };
        });
    }

    async function lerProjetos() {
        let html;
        try {
            html = await texto(raiz + 'projetos/');
        } catch {
            return [];
        }
        const doc = new DOMParser().parseFromString(html, 'text/html');
        return [...doc.querySelectorAll('.proj-featured, .proj-card')].map((card) => {
            const link =
                card.querySelector('.proj-titulo-link') || card.querySelector('a.proj-link');
            const rotulo = card.querySelector('.proj-type, .tag')?.textContent || 'Projeto';
            return {
                tipo: 'Projeto',
                rotulo: rotulo.replace(/\s*·\s*em destaque/i, '').trim(),
                titulo: card.querySelector('h2, h3')?.textContent.trim() || '',
                resumo: card.querySelector('p')?.textContent.trim() || '',
                url: link ? new URL(link.getAttribute('href'), raiz + 'projetos/').href : raiz + 'projetos/',
            };
        });
    }

    function carregar() {
        if (!carregando) {
            carregando = Promise.all([lerArtigos(), lerProjetos()]).then(([artigos, projetos]) => {
                indice = [...artigos, ...projetos].map((item) => ({
                    ...item,
                    chave: normalizar(`${item.titulo} ${item.resumo} ${item.rotulo}`),
                    chaveTitulo: normalizar(item.titulo),
                }));
                return indice;
            });
        }
        return carregando;
    }

    // ---- janela ------------------------------------------------------------

    const janela = document.createElement('dialog');
    janela.className = 'busca';
    janela.setAttribute('aria-label', 'Buscar artigos e projetos');
    janela.innerHTML = `
        <div class="busca-caixa">
            <div class="busca-campo">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M14.95 14.95a1 1 0 0 1 1.41 0l6.34 6.34a1 1 0 0 1-1.41 1.41l-6.34-6.34a1 1 0 0 1 0-1.41Z" fill="currentColor"/>
                    <path d="M10 3a7 7 0 1 0 0 14 7 7 0 0 0 0-14Zm-9 7a9 9 0 1 1 18 0 9 9 0 0 1-18 0Z" fill="currentColor"/>
                </svg>
                <label class="busca-rotulo" for="busca-termo">Buscar artigos e projetos</label>
                <input id="busca-termo" type="search" placeholder="Kcoisa você quer procurar?" autocomplete="off" />
                <button type="button" class="busca-fechar" aria-label="Fechar a busca">Esc</button>
            </div>
            <div class="busca-filtros" role="group" aria-label="Filtrar resultados">
                <button type="button" data-filtro="todos" aria-pressed="true">Tudo</button>
                <button type="button" data-filtro="Artigo" aria-pressed="false">Artigos</button>
                <button type="button" data-filtro="Projeto" aria-pressed="false">Projetos</button>
            </div>
            <p class="busca-status" role="status" aria-live="polite"></p>
            <ul class="busca-lista"></ul>
        </div>`;
    document.body.appendChild(janela);

    const campo = janela.querySelector('input');
    const lista = janela.querySelector('.busca-lista');
    const status = janela.querySelector('.busca-status');
    let filtro = 'todos';

    const escapar = (valor) =>
        valor.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

    function mostrar() {
        if (!indice) {
            status.textContent = 'Carregando…';
            return;
        }
        const termos = normalizar(campo.value).split(/\s+/).filter(Boolean);
        let itens = indice.filter((item) => filtro === 'todos' || item.tipo === filtro);
        if (termos.length) {
            itens = itens
                .filter((item) => termos.every((t) => item.chave.includes(t)))
                .map((item) => ({
                    item,
                    peso: termos.reduce((soma, t) => soma + (item.chaveTitulo.includes(t) ? 2 : 1), 0),
                }))
                .sort((a, b) => b.peso - a.peso)
                .map((r) => r.item);
        }
        itens = itens.slice(0, 12);

        lista.innerHTML = itens
            .map(
                (item) => `
            <li>
                <a href="${escapar(item.url)}">
                    <span class="busca-tipo">${item.tipo} · ${escapar(item.rotulo)}</span>
                    <b>${escapar(item.titulo)}</b>
                    ${item.resumo ? `<span class="busca-resumo">${escapar(item.resumo)}</span>` : ''}
                </a>
            </li>`
            )
            .join('');

        if (!itens.length) {
            status.textContent = termos.length
                ? 'Nada encontrado. Tente outra palavra.'
                : 'Nenhum item para mostrar.';
        } else {
            status.textContent = termos.length
                ? `${itens.length} ${itens.length === 1 ? 'resultado' : 'resultados'}`
                : 'Comece a digitar ou navegue pelos mais recentes';
        }
    }

    function abrir() {
        if (!janela.open) janela.showModal();
        campo.focus();
        carregar()
            .then(mostrar)
            .catch(() => {
                status.textContent = 'Não foi possível carregar a busca agora.';
            });
        mostrar();
    }

    gatilhos.forEach((botao) => botao.addEventListener('click', abrir));
    campo.addEventListener('input', mostrar);
    // O Esc fecha a busca sem acionar atalhos da página ou limpar o campo.
    janela.addEventListener('keydown', (evento) => {
        if (evento.key === 'Escape') {
            evento.preventDefault();
            evento.stopPropagation();
            janela.close();
        }
    });
    janela.querySelector('.busca-fechar').addEventListener('click', () => janela.close());
    janela.addEventListener('click', (evento) => {
        if (evento.target === janela) janela.close();
    });
    janela.querySelectorAll('[data-filtro]').forEach((botao) => {
        botao.addEventListener('click', () => {
            filtro = botao.dataset.filtro;
            janela
                .querySelectorAll('[data-filtro]')
                .forEach((b) => b.setAttribute('aria-pressed', String(b === botao)));
            mostrar();
            campo.focus();
        });
    });

    // Atalhos: "/" ou Ctrl+K abrem a busca
    document.addEventListener('keydown', (evento) => {
        const digitando = /^(input|textarea|select)$/i.test(evento.target.tagName) || evento.target.isContentEditable;
        if ((evento.key === '/' && !digitando) || ((evento.ctrlKey || evento.metaKey) && evento.key.toLowerCase() === 'k')) {
            evento.preventDefault();
            abrir();
        }
    });
})();
