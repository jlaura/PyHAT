@echo off
:top
for /r %USERPROFILE% %%I in (*git.exe) do (

	%%I config remote.origin.url git@github.com:tisaconundrum2/PySAT.git
	%%I pull origin master
	%%I add -A
	%%I commit -m "Auto Generated Update:_
	%%I push -u origin master
	timeout /t 600
)
goto :top