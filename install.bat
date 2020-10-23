@echo off

FOR /F "tokens=*" %%a in ('REG QUERY "HKEY_CURRENT_USER\Environment" /v "Path"') do SET preoutput=%%a

REG ADD HKEY_CURRENT_USER\Environment /v Path /d "%PATH%%systemdrive%%homepath%\.ssh\\" 

FOR /F "tokens=*" %%a in ('REG QUERY "HKEY_CURRENT_USER\Environment" /v "Path"') do SET output=%%a

if "%preoutput%" == "%output%" (goto abort) else (goto install)

:abort
echo Install Aborted
goto end

:install
if not exist "%systemdrive%%homepath%\.ssh\" mkdir "%systemdrive%%homepath%\.ssh\"
copy "%cd%\connect.*" "%systemdrive%%homepath%\.ssh\connect.*"
echo Install Complete
echo Restart your machine for the changes to take effect
goto end

:end
pause