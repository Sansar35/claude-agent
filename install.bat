@echo off
REM ============================================================
REM  Claude Agent — Windows Kurulum
REM  claude-config/ icerigini %USERPROFILE%\.claude\ altina kopyalar
REM ============================================================

setlocal enabledelayedexpansion
chcp 65001 >nul

set "SRC=%~dp0claude-config"
set "DST=%USERPROFILE%\.claude"

echo.
echo ============================================================
echo   CLAUDE AGENT KURULUM
echo ============================================================
echo.
echo   Kaynak    : %SRC%
echo   Hedef     : %DST%
echo.

REM Hedef klasor varlik kontrolu
if not exist "%DST%" (
    echo   [INFO] %DST% yok, olusturuluyor...
    mkdir "%DST%"
)

REM Kopyalama (her klasor icin xcopy)
for %%D in (skills agents commands awesome-claude-skills hooks-templates mcps-templates settings-templates hooks) do (
    if exist "%SRC%\%%D" (
        echo   [COPY] %%D ...
        xcopy /E /I /Y /Q "%SRC%\%%D" "%DST%\%%D" >nul
        if errorlevel 1 (
            echo   [HATA] %%D kopyalanamadi
        ) else (
            echo   [OK]   %%D
        )
    )
)

REM Ornek dosyalar
if exist "%SRC%\CLAUDE.md.example" (
    copy /Y "%SRC%\CLAUDE.md.example" "%DST%\CLAUDE.md.example" >nul
    echo   [OK]   CLAUDE.md.example
)
if exist "%SRC%\settings.example.json" (
    copy /Y "%SRC%\settings.example.json" "%DST%\settings.example.json" >nul
    echo   [OK]   settings.example.json
)

echo.
echo ============================================================
echo   KURULUM TAMAMLANDI
echo ============================================================
echo.
echo   Dosyalar %DST% altina yerlestirildi.
echo.
echo   Sonraki adimlar:
echo   1) team/ klasorunde python -m pip install -r team\requirements.txt
echo   2) team/.env.example -^> team/.env kopyala, key'leri yaz
echo   3) python team\team.py "Test projesi yaz"
echo.
echo   Detay: README.md
echo.
pause
endlocal
