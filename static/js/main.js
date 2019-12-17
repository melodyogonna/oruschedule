
const $ = window.jQuery;
const anime = window.anime;
const handlemenu = () => {
    'use strict';
    $('.responsive-menu .mobile-hamburger i.icon').click(() => {
        $('div.admin-navbar-responsive').show();
        // $('div.admin-navbar-responsive div.menu').animate({
        //     translateX: '18rem'
        // });
        anime({
            targets: 'div.admin-navbar-responsive div.menu',
            translateX: '0%',
            easing: 'linear'
        });
    });
    $('div.admin-navbar-responsive').click(() => {
        $('div.admin-navbar-responsive').hide(() => {
            anime({
                targets: 'div.admin-navbar-responsive div.menu',
                translateX: '-100%',
                easing: 'linear'
            });
        });
    });
};

handlemenu();