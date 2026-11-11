// Animação da seta no Hero Section

document.addEventListener('DOMContentLoaded', () => {

    const scrollCue = document.querySelector('.scroll-cue');

    if (!scrollCue) return;

    let lastScrollY = window.scrollY;

    window.addEventListener('scroll', () => {

        const currentScrollY = window.scrollY;

        // Ao subir ou estar no topo
        if (currentScrollY < lastScrollY || currentScrollY <= 10) {
            scrollCue.classList.remove('hidden');
        }

        // Ao descer
        else {
            scrollCue.classList.add('hidden');
        }

        lastScrollY = currentScrollY;

    }, { passive: true });

});