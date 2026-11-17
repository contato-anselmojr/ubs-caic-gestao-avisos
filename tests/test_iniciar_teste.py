"""Testes do iniciador local para avaliação acadêmica."""
import unittest
from unittest.mock import MagicMock, patch

import iniciar_teste


class IniciadorLocalTests(unittest.TestCase):
    @patch("iniciar_teste.webbrowser.open_new_tab")
    @patch("iniciar_teste.HTTPServer")
    def test_inicia_localhost_e_fecha_ao_interromper(self, criar_servidor, abrir_aba):
        servidor = MagicMock()
        criar_servidor.return_value = servidor
        servidor.serve_forever.side_effect = KeyboardInterrupt
        iniciar_teste.main()
        criar_servidor.assert_called_once_with(("127.0.0.1", 5000), iniciar_teste.UBSHandler)
        abrir_aba.assert_called_once_with("http://127.0.0.1:5000")
        servidor.server_close.assert_called_once()

    @patch("iniciar_teste.webbrowser.open_new_tab")
    @patch("iniciar_teste.HTTPServer", side_effect=OSError("endereco ocupado"))
    def test_porta_em_uso_sai_sem_abrir_navegador(self, criar_servidor, abrir_aba):
        with self.assertRaises(SystemExit) as erro:
            iniciar_teste.main()
        self.assertEqual(erro.exception.code, 1)
        abrir_aba.assert_not_called()


if __name__ == "__main__":
    unittest.main()
