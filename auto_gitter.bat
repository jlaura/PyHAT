@echo off
Setlocal EnableDelayedExpansion
:top
for /f "delims=" %%I in ('dir %USERPROFILE% /b/o/w/s ^| find /i "cmd\git.exe"') do (
	set /p "commit= commit -m: "
	%%I config remote.origin.url git@github.com:tisaconundrum2/PySAT.git
	%%I pull origin master
	%%I add -A
	%%I commit -m "!commit!"
	%%I push -u origin master
)
goto :top