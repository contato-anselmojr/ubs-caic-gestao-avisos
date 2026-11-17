"""Testes estruturais do fluxo demonstrativo de notificações (não enviam SMS)."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class NotificationsDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/"index.html").read_text(encoding="utf-8")
        cls.sql=(ROOT/"db"/"notificacoes_demo.sql").read_text(encoding="utf-8")

    def test_central_manual_e_historico(self):
        for term in ('data-view="notificacoes"','id="patientSearch"','id="manualExamSelect"',
                     'id="sendManualNotice"','id="notificationTableBody"','sendManualNotice()'):
            self.assertIn(term,self.html)

    def test_lembretes_programados_e_processados_no_banco(self):
        for term in ("array[48,24]","trg_programar_lembretes_demo",
                     "processar_lembretes_demo","'* * * * *'","status='simulada'"):
            self.assertIn(term,self.sql)

    def test_politica_rls_e_simulacao_sem_sms_real(self):
        self.assertIn("enable row level security",self.sql)
        self.assertIn("id_operador=(select auth.uid())",self.sql)
        self.assertIn("Nenhum SMS ou WhatsApp é enviado",self.html)

if __name__=="__main__":
    unittest.main()
