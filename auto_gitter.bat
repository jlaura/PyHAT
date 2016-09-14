@echo off
:top
for /r %USERPROFILE% %%I in (*git.exe) do (

	%%I config remote.origin.url git@github.com:tisaconundrum2/PySAT.git
	For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
	For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
	%%I pull origin master
	%%I add -A
	%%I commit -m "Update: %mydate%_%mytime%"
	%%I push -u origin master
	timeout /t 600
)
goto :top