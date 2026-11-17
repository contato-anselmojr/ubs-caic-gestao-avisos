"""Cabecalhos HTTP do prototipo UBS CAIC.

Defesa em profundidade para uma demonstracao local; nao substitui
autenticacao, autorizacao nem controles exigidos em producao.
"""

from http.server import BaseHTTPRequestHandler

SECURITY_HEADERS = (
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("Referrer-Policy", "no-referrer"),
    ("Permissions-Policy", "camera=(), microphone=(), geolocation=()"),
)


def send_html_headers(handler: BaseHTTPRequestHandler, body_length: int) -> None:
    """Envia cabecalhos apos send_response e antes de end_headers."""
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(body_length))
    handler.send_header("Cache-Control", "no-store")
    for name, value in SECURITY_HEADERS:
        handler.send_header(name, value)
