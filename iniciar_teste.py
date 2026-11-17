"""Inicializador da demonstração local da UBS CAIC.

Não requer pacotes externos e não acessa o Supabase. Usa somente dados fictícios
armazenados em memória no navegador. Pressione Ctrl+C para encerrar o servidor.
"""
from http.server import HTTPServer
import webbrowser

from app import UBSHandler


def main():
    endereco = "http://127.0.0.1:5000"
    try:
        servidor = HTTPServer(("127.0.0.1", 5000), UBSHandler)
    except OSError as exc:
        print("Não foi possível iniciar a demonstração na porta 5000.")
        print("Feche outra execução do protótipo, ou verifique se a porta está em uso.")
        raise SystemExit(1) from exc

    print("UBS CAIC — demonstração local (sem Supabase e sem login)")
    print(f"Endereço no navegador: {endereco}")
    print("Caso o navegador não abra sozinho, copie o endereço acima.")
    print("Para encerrar, pressione Ctrl+C neste terminal.")
    try:
        webbrowser.open_new_tab(endereco)
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nDemonstração encerrada.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
