@echo off
for /f "delims=" %%I in ('dir %USERPROFILE% /b/o/w/s ^| find /i "cmd\git.exe"') do (
	%%I config remote.origin.url git@github.com:tisaconundrum2/PySAT.git
	%%I pull origin master
	%%I add -A
	%%I commit -m "Auto Generated Update:_
	%%I push -u origin master
	timeout /t 600
)
