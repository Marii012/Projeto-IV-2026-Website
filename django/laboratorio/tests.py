from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.test import SimpleTestCase


class LoginTests(SimpleTestCase):
    @patch('laboratorio.views.obter_utilizador_por_email')
    def test_login_uses_django_session(self, obter_utilizador):
        obter_utilizador.return_value = (
            7, 'Ana', 'ana@example.com', make_password('senha-segura'),
            None, None, 1, 12,
        )

        resposta = self.client.post(
            '/entrar/',
            {'username': 'ana@example.com', 'password': 'senha-segura'},
        )

        self.assertRedirects(resposta, '/dashboard/admin/', fetch_redirect_response=False)
        self.assertEqual(self.client.session['utilizador_id'], 7)
        self.assertEqual(self.client.session['tipo_utilizador_id'], 1)

    @patch('laboratorio.views.obter_utilizador_por_email')
    def test_login_rejects_invalid_password(self, obter_utilizador):
        obter_utilizador.return_value = (
            7, 'Ana', 'ana@example.com', make_password('senha-segura'),
            None, None, 1, 12,
        )

        resposta = self.client.post(
            '/entrar/',
            {'username': 'ana@example.com', 'password': 'incorreta'},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn('utilizador_id', self.client.session)
