/*
 * Imagens dos artigos em tela cheia, com carrossel.
 * Clicar numa imagem do artigo (ou na capa) abre o visualizador; as setas do
 * teclado, os botões e o gesto de deslizar no celular passam para a anterior e a
 * próxima. Esc, o botão Fechar ou um clique fora da imagem fecham.
 */
(function () {
    const seletor = '.post-cover img, .post-content img';
    const imagens = [...document.querySelectorAll(seletor)].filter(
        (img) => !img.closest('a, .kg-bookmark-card')
    );
    if (!imagens.length) return;

    let atual = 0;
    let ultimoFoco = null;

    const janela = document.createElement('dialog');
    janela.className = 'lightbox';
    janela.setAttribute('aria-label', 'Imagens do artigo');
    janela.innerHTML = `
        <div class="lightbox-topo">
            <span class="lightbox-contador" aria-live="polite"></span>
            <button type="button" class="lightbox-fechar" aria-label="Fechar imagem">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>
            </button>
        </div>
        <button type="button" class="lightbox-seta lightbox-anterior" aria-label="Imagem anterior">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m15 5-7 7 7 7"/></svg>
        </button>
        <figure class="lightbox-palco">
            <img alt="" />
            <figcaption></figcaption>
        </figure>
        <button type="button" class="lightbox-seta lightbox-proxima" aria-label="Próxima imagem">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 5 7 7-7 7"/></svg>
        </button>`;
    document.body.appendChild(janela);

    const foto = janela.querySelector('.lightbox-palco img');
    const legenda = janela.querySelector('figcaption');
    const contador = janela.querySelector('.lightbox-contador');
    const anterior = janela.querySelector('.lightbox-anterior');
    const proxima = janela.querySelector('.lightbox-proxima');
    const varias = imagens.length > 1;

    function fonte(img) {
        return img.currentSrc || img.src;
    }

    function pre(indice) {
        const img = imagens[(indice + imagens.length) % imagens.length];
        new Image().src = fonte(img);
    }

    function mostrar(indice) {
        atual = (indice + imagens.length) % imagens.length;
        const img = imagens[atual];
        foto.src = fonte(img);
        foto.alt = img.alt || '';
        const texto = img.closest('figure')?.querySelector('figcaption')?.textContent.trim() || img.alt || '';
        legenda.textContent = texto;
        legenda.hidden = !texto;
        contador.textContent = varias ? `${atual + 1} de ${imagens.length}` : '';
        anterior.hidden = proxima.hidden = !varias;
        if (varias) {
            pre(atual + 1);
            pre(atual - 1);
        }
    }

    function abrir(indice) {
        ultimoFoco = document.activeElement;
        mostrar(indice);
        janela.showModal();
        janela.querySelector('.lightbox-fechar').focus();
    }

    function fechar() {
        janela.close();
    }

    imagens.forEach((img, indice) => {
        img.classList.add('zoomavel');
        img.tabIndex = 0;
        img.setAttribute('role', 'button');
        img.setAttribute('aria-label', `Ampliar imagem: ${img.alt || 'sem descrição'}`);
        img.addEventListener('click', () => abrir(indice));
        img.addEventListener('keydown', (evento) => {
            if (evento.key === 'Enter' || evento.key === ' ') {
                evento.preventDefault();
                abrir(indice);
            }
        });
    });

    anterior.addEventListener('click', () => mostrar(atual - 1));
    proxima.addEventListener('click', () => mostrar(atual + 1));
    janela.querySelector('.lightbox-fechar').addEventListener('click', fechar);
    janela.addEventListener('close', () => {
        if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
    });

    // Clique no fundo (fora da imagem e dos botões) fecha
    janela.addEventListener('click', (evento) => {
        if (evento.target === janela || evento.target.classList.contains('lightbox-palco')) fechar();
    });

    janela.addEventListener('keydown', (evento) => {
        if (!varias) return;
        if (evento.key === 'ArrowLeft') {
            evento.preventDefault();
            mostrar(atual - 1);
        } else if (evento.key === 'ArrowRight') {
            evento.preventDefault();
            mostrar(atual + 1);
        }
    });

    // Deslizar no celular
    let inicioX = null;
    janela.addEventListener(
        'touchstart',
        (evento) => {
            inicioX = evento.touches.length === 1 ? evento.touches[0].clientX : null;
        },
        { passive: true }
    );
    janela.addEventListener(
        'touchend',
        (evento) => {
            if (inicioX === null || !varias) return;
            const delta = evento.changedTouches[0].clientX - inicioX;
            inicioX = null;
            if (Math.abs(delta) < 50) return;
            mostrar(delta < 0 ? atual + 1 : atual - 1);
        },
        { passive: true }
    );
})();
