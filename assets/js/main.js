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
