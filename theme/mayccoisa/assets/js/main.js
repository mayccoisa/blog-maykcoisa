/* Página de projetos: filtros por tipo e "Mostrar mais" no celular.
   Sem JS, a lista completa aparece e os filtros ficam escondidos. */
(function () {
    'use strict';

    var area = document.querySelector('[data-projetos]');
    if (!area) {
        return;
    }

    var filtros = area.querySelector('.proj-filters');
    var botoes = Array.prototype.slice.call(area.querySelectorAll('.proj-filter'));
    var destaque = area.querySelector('.proj-featured');
    var cards = Array.prototype.slice.call(area.querySelectorAll('.proj-card'));
    var vazio = area.querySelector('.proj-empty');
    var mais = area.querySelector('.proj-more');
    var celular = window.matchMedia('(max-width: 620px)');
    var LIMITE = 3;
    var filtroAtual = 'todos';
    var expandido = false;

    var todos = (destaque ? [destaque] : []).concat(cards);

    var contar = function (tipo) {
        return todos.filter(function (item) {
            return tipo === 'todos' || item.getAttribute('data-tipo') === tipo;
        }).length;
    };

    botoes.forEach(function (botao) {
        var tipo = botao.getAttribute('data-filtro');
        var total = contar(tipo);
        botao.textContent = botao.textContent + ' · ' + total;
        if (total === 0) {
            botao.hidden = true;
        }
    });

    var aplicar = function () {
        var noFiltro = function (item) {
            return filtroAtual === 'todos' || item.getAttribute('data-tipo') === filtroAtual;
        };

        if (destaque) {
            destaque.hidden = !noFiltro(destaque);
        }

        var visiveis = cards.filter(noFiltro);
        var recolher = celular.matches && !expandido && visiveis.length > LIMITE;

        cards.forEach(function (card) {
            card.hidden = true;
        });
        visiveis.forEach(function (card, indice) {
            card.hidden = recolher && indice >= LIMITE;
        });

        vazio.hidden = visiveis.length > 0;

        if (recolher) {
            var resto = visiveis.length - LIMITE;
            mais.textContent = 'Mostrar mais ' + resto + (resto === 1 ? ' projeto' : ' projetos');
            mais.hidden = false;
        } else {
            mais.hidden = true;
        }
    };

    botoes.forEach(function (botao) {
        botao.addEventListener('click', function () {
            filtroAtual = botao.getAttribute('data-filtro');
            botoes.forEach(function (outro) {
                outro.setAttribute('aria-pressed', outro === botao ? 'true' : 'false');
            });
            aplicar();
        });
    });

    mais.addEventListener('click', function () {
        var primeiroEscondido = cards.filter(function (card) {
            return card.hidden && (filtroAtual === 'todos' || card.getAttribute('data-tipo') === filtroAtual);
        })[0];
        expandido = true;
        aplicar();
        // O foco vai para o primeiro card revelado, para o teclado seguir dali
        if (primeiroEscondido) {
            var alvo = primeiroEscondido.querySelector('a');
            if (!alvo) {
                primeiroEscondido.setAttribute('tabindex', '-1');
                alvo = primeiroEscondido;
            }
            alvo.focus({ preventScroll: true });
        }
    });

    if (celular.addEventListener) {
        celular.addEventListener('change', aplicar);
    }

    filtros.hidden = false;
    aplicar();
})();

(function () {
    'use strict';

    var toggle = document.querySelector('.menu-toggle');
    var menu = document.getElementById('menu-principal');

    if (!toggle || !menu) {
        return;
    }

    var setOpen = function (open) {
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        document.body.classList.toggle('menu-open', open);
    };

    toggle.addEventListener('click', function () {
        setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    menu.addEventListener('click', function (event) {
        if (event.target.closest('a')) {
            setOpen(false);
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
            setOpen(false);
            toggle.focus();
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 900) {
            setOpen(false);
        }
    });
})();
