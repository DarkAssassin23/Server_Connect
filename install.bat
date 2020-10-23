@echo off

:menu
echo Which option would you like to do?
echo 1. Install for the first time
echo 2. Update/Re-Install
set /p input=">> "

if %input%==2 (
	goto update
)
if %input%==1 (
	goto main
) else (
	echo Invalid Selection
	goto menu
)
)

:main
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

:update
if not exist "%systemdrive%%homepath%\.ssh\" mkdir "%systemdrive%%homepath%\.ssh\"
copy "%cd%\connect.*" "%systemdrive%%homepath%\.ssh\connect.*"
echo Install Complete
echo You're all set!
goto end

:end
pause