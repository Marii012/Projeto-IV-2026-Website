document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-password-toggle]').forEach(function (button) {
        button.addEventListener('click', function () {
            const passwordInput = button.parentElement.querySelector('input');
            const passwordVisible = passwordInput.type === 'text';

            passwordInput.type = passwordVisible ? 'password' : 'text';
            button.setAttribute('aria-pressed', String(!passwordVisible));
            button.setAttribute(
                'aria-label',
                passwordVisible ? 'Mostrar palavra-passe' : 'Ocultar palavra-passe'
            );
        });
    });

    const addButton = document.getElementById('add-morada');
    const moradasContainer = document.getElementById('moradas-container');

    // Permitir apenas números no NIF e telefone
    const nifInput = document.getElementById('nif');
    const telefoneInput = document.getElementById('telefone');

    [nifInput, telefoneInput].forEach(function (input) {
        if (input) {
            input.addEventListener('input', function () {
                this.value = this.value.replace(/\D/g, '');
            });
        }
    });

    // Limitar o NIF a 9 algarismos
    if (nifInput) {
        nifInput.setAttribute('maxlength', '9');
    }

    // Verificar se os elementos das moradas existem
    if (!addButton || !moradasContainer) {
        return;
    }

    const LIMITE_MORADAS = 4;

    function atualizarMoradas() {
        const moradas = moradasContainer.querySelectorAll('.morada-item');

        moradas.forEach(function (morada, index) {
            const input = morada.querySelector('input');

            input.placeholder = `Morada ${index + 1} — rua, código postal, localidade`;
        });

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
