
document.addEventListener('DOMContentLoaded', function () {
    const addButton = document.getElementById('add-morada');
    const moradasContainer = document.getElementById('moradas-container');

    const LIMITE_MORADAS = 4;

    function atualizarMoradas() {
        const moradas = moradasContainer.querySelectorAll('.morada-item');

        moradas.forEach(function (morada, index) {
            const input = morada.querySelector('input');

            input.placeholder = `Morada ${index + 1} — rua, código postal, localidade`;
        });

        // Desativar o botão quando atingir o limite
        addButton.disabled = moradas.length >= LIMITE_MORADAS;

        addButton.textContent = moradas.length >= LIMITE_MORADAS
            ? 'Limite de 4 moradas atingido'
            : '+ Adicionar morada';
    }

    addButton.addEventListener('click', function () {
        const quantidadeMoradas = moradasContainer.querySelectorAll('.morada-item').length;

        if (quantidadeMoradas >= LIMITE_MORADAS) {
            return;
        }

        const novaMorada = document.createElement('div');
        novaMorada.classList.add('login-field', 'morada-item');

        novaMorada.innerHTML = `
            <input
                type="text"
                name="morada[]"
                placeholder="Morada"
                required
            >

            <button type="button" class="remove-morada" aria-label="Remover morada">
                ×
            </button>
        `;

        moradasContainer.appendChild(novaMorada);

        atualizarMoradas();
    });

    moradasContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-morada')) {
            event.target.closest('.morada-item').remove();

            atualizarMoradas();
        }
    });

    atualizarMoradas();
});
