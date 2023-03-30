@echo off
set client_url=https://mtbank.cdn.online-trading-solutions.com/installer4/mtbank/MTBankFX_windows-x64.exe
set client_path=%TEMP%\MTBankFX_windows-x64.exe

@echo on
curl --output %client_path% --url %client_url%

%client_path% -q

del %client_path%