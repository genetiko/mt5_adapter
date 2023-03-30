@echo off
set client_url=https://download.fxclub.by/Metatrader/fcmt5setup_bd.exe
set client_path=%TEMP%\fcmt5setup_bd.exe

@echo on
curl --output %client_path% --url %client_url%

%client_path% /auto

del %client_path%