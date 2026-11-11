document.addEventListener('DOMContentLoaded', () => {

    const menu = document.querySelector('.site-nav .navbar-collapse');
    const toggler = document.querySelector('.site-nav .navbar-toggler');

    // Fechar ao clicar nos links
    document.querySelectorAll('.site-nav .nav-link').forEach(link => {

        link.addEventListener('click', () => {

            if (menu.classList.contains('show')) {
                bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }

        });

    });

    // Fechar ao clicar fora do menu
    document.addEventListener('click', event => {

        if (
            menu.classList.contains('show') &&
            !menu.contains(event.target) &&
            !toggler.contains(event.target)
        ) {
            bootstrap.Collapse.getOrCreateInstance(menu).hide();
        }

    });

});
