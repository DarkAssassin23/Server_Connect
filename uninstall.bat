@echo off

net session >nul 2>&1
if %errorLevel% == 0 (
	echo Uninstalling Server Connect...
	set "UserPath="
	for /F "skip=2 tokens=1,2*" %%G in ('%SystemRoot%\System32\reg.exe query "HKCU\Environment" /v "Path" 2^>nul') do if /I "%%G" == "Path" (
    		if /I "%%H" == "REG_EXPAND_SZ" (call set "UserPath=%%I") else if /I "%%H" == "REG_SZ" set "UserPath=%%I"
    		if defined UserPath goto UserPathValid
	)

	goto end
) else (
	echo Error: You need Administrator Privileges to uninstall this program
	goto end
)

:UserPathValid
set ServerConnectDirectory=%userprofile%\.ssh\;

call set Replaced=%%UserPath:%ServerConnectDirectory%=%%

If NOT "%UserPath%"=="%Replaced%" (
	REG ADD HKEY_CURRENT_USER\Environment /v Path /d "%Replaced%" /f
	echo Server Connect successfully removed from registry
	goto uninstall
) else (
	goto uninstall
)

:uninstall
echo Removing Files...
if exist "%userprofile%\.ssh\connect.*" del /q "%userprofile%\.ssh\connect.*"
echo Server Connect was successfully uninstalled
goto end

:end
pause