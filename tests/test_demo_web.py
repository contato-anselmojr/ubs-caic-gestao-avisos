"""Verificações estruturais da versão Vercel (não substituem teste E2E)."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class DemoWebStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.sql = (ROOT / "db" / "limite_conta_demo.sql").read_text(encoding="utf-8")

    def test_frontend_exibe_limite_e_permite_exclusao(self):
        for token in ("DEMO_LIMIT = 10", 'id="demoQuota"', "data-delete-consult", "data-delete-exam", 'method="DELETE"'):
            if token == 'method="DELETE"':
                self.assertIn('"DELETE"', self.html)
            else:
                self.assertIn(token, self.html)

    def test_limite_aplicado_nas_duas_tabelas(self):
        for token in ("limite_demo_consultas", "limite_demo_exames", "pg_advisory_xact_lock", "total >= 10", "security invoker"):
            self.assertIn(token, self.sql)

    def test_cadastro_publico_oculto(self):
        self.assertIn('id="signupButton" type="button" class="btn btn-outline hidden" disabled', self.html)


if __name__ == "__main__":
    unittest.main()
