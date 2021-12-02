@echo off

echo Making sure the necessary python packages are installed

python -m pip install requests
python -m pip install netifaces 

echo.
echo Installing Server Connect...
set "UserPath="
for /F "skip=2 tokens=1,2*" %%G in ('%SystemRoot%\System32\reg.exe query "HKCU\Environment" /v "Path" 2^>nul') do if /I "%%G" == "Path" (
    if /I "%%H" == "REG_EXPAND_SZ" (call set "UserPath=%%I") else if /I "%%H" == "REG_SZ" set "UserPath=%%I"
    if defined UserPath goto UserPathValid
)

REG ADD HKEY_CURRENT_USER\Environment /v Path /d "%userprofile%\.ssh\;" /f
echo Registry Path Updated
goto install

:UserPathValid
set ServerConnectDirectory=%userprofile%\.ssh\;

call set Replaced=%%UserPath:%ServerConnectDirectory%=%%

If NOT "%UserPath%"=="%Replaced%" (
	goto update
) else (
	REG ADD HKEY_CURRENT_USER\Environment /v Path /d "%UserPath%%userprofile%\.ssh\;" /f
	echo Registry Path Updated
	goto install
)

:install
echo.
echo Copying Files...
if not exist "%userprofile%\.ssh\" mkdir "%userprofile%\.ssh\"
copy "%~dp0\connect.*" "%userprofile%\.ssh\connect.*"

::Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
	setx OS "%OS%" /M
	echo Install Complete
	echo Close any running command prompt windows for this change to take effect
) else (
	echo Install Complete
	echo.
	echo NOTICE: You did not run the installer with Administrative Privileges
	echo Your installation was successful, however you need to do one of the following for your changes to take effect:
	echo 1. Log out and log back in
	echo 2. Open 'Advanced System Settings' -^> Environment Variables, then select 'OK' and 'OK' again
	echo 3. Restart your device
)
goto end

:update
echo.
echo Copying Files...
if not exist "%userprofile%\.ssh\" mkdir "%userprofile%\.ssh\"
copy "%~dp0\connect.*" "%userprofile%\.ssh\connect.*"
echo Update Complete
goto end

:end
pause