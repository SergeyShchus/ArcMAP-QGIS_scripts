@echo off
IF EXIST c:\python27\arcgis10.1\python.exe (

set id=10.1
goto :RunReplace
) 

IF EXIST c:\python27\arcgis10.2\python.exe (

set id=10.2
goto :RunReplace

)
IF EXIST c:\python27\arcgis10.3\python.exe (

set id=10.3
goto :RunReplace

)
IF EXIST c:\python27\arcgis10.4\python.exe (

set id=10.4
goto :RunReplace

)
IF EXIST c:\python27\arcgis10.5\python.exe (

set id=10.5
goto :RunReplace

)
goto :ShowError

:RunReplace
c:\PYTHON27\ArcGIS%id%\python.exe ..\scripts\MDCS.py -i:..\Parameter\Config\S_TiledOrthos.xml 
c:\PYTHON27\ArcGIS%id%\python.exe ..\scripts\MDCS.py -i:..\Parameter\Config\S_CCMs.xml
goto :Endscript

:ShowError
@echo "Error: Could not find ArcGIS."
pause

:Endscript
pause


