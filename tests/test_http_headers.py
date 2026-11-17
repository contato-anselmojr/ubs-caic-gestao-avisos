"""Testes unitarios da politica de cabecalhos HTTP."""

import unittest
from unittest.mock import Mock, call

from http_headers import SECURITY_HEADERS, send_html_headers


class TestCabecalhosHTTP(unittest.TestCase):
    def test_configuracao_de_cabecalhos_sem_servidor(self):
        handler = Mock()
        send_html_headers(handler, 123)

        expected = [
            call("Content-Type", "text/html; charset=utf-8"),
            call("Content-Length", "123"),
            call("Cache-Control", "no-store"),
            *(call(name, value) for name, value in SECURITY_HEADERS),
        ]
        self.assertEqual(handler.send_header.call_args_list, expected)

    def test_tamanho_de_resposta_vazia(self):
        handler = Mock()
        send_html_headers(handler, 0)
        handler.send_header.assert_any_call("Content-Length", "0")


if __name__ == "__main__":
    unittest.main()
