@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 iniciar_teste.py
  goto fim
)
where python >nul 2>&1
if %errorlevel%==0 (
  python iniciar_teste.py
  goto fim
)
echo Python 3 nao encontrado. Instale Python 3 em https://www.python.org/downloads/
echo Marque "Add Python to PATH" durante a instalacao.
:fim
echo.
echo Se ocorreu algum erro, confira as instrucoes no README.md.
pause
