"""Testes da camada HTTP do prototipo demonstrativo UBS CAIC.

Nao utilizam rede externa, dados reais ou servicos de notificacao.
"""

import threading
import unittest
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from app import UBSHandler


class TestServidorUBS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), UBSHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_raiz_retorna_html_http_200(self):
        with urlopen(self.base_url + '/', timeout=5) as response:
            body = response.read().decode('utf-8')
            self.assertEqual(response.status, 200)
            self.assertIn('text/html', response.headers['Content-Type'])
            self.assertIn('UBS Sueli Dutra Alves', body)

    def test_index_html_retorna_http_200(self):
        with urlopen(self.base_url + '/index.html', timeout=5) as response:
            self.assertEqual(response.status, 200)

    def test_rota_desconhecida_retorna_http_404(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base_url + '/rota-inexistente', timeout=5)
        self.assertEqual(error.exception.code, 404)

    def test_paginas_principais_estao_no_prototipo(self):
        with urlopen(self.base_url + '/', timeout=5) as response:
            body = response.read().decode('utf-8')
        for section_id in ('inicio', 'cadastro', 'fila'):
            with self.subTest(secao=section_id):
                self.assertIn(f'id="{section_id}"', body)

    def test_contador_consultas_nao_usa_valor_fixo(self):
        with urlopen(self.base_url + '/', timeout=5) as response:
            body = response.read().decode('utf-8')
        self.assertIn("'countConsultas').textContent = appointments.length;", body)


if __name__ == '__main__':
    unittest.main()
