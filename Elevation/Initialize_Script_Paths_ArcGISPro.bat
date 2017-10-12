@echo off
set var=%cd%

rem This batch file will initialize the ArcGIS version number to be used by the Elevation Batch files.
rem It will also set the current folder as the working folder in the batch files and script files. 

IF EXIST "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" (

goto :RunReplace
) 

goto :ShowError

:RunReplace
rem "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\batchFiles arcgisVer arcgis%id% *.bat
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\batchFiles\ArcGISPro  currFolder %var% *.bat
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config currFolder %var% *.xml
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config\sample0 currFolder %var% *.xml
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config\sample1 currFolder %var% *.xml
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config\sample2 currFolder %var% *.xml
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\RasterFunctionTemplates currFolder %var% *.xml
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Rastertype currFolder %var% *.xml

copy /y nul Reset_Script_Paths_ArcGISPro.bat
echo @echo off
echo @echo This batch file was automatically created after successfully executing Intialize_Script_Paths.bat. >Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo @echo This batch file will reset the ArcGIS version number and current folder location to be used by the Elevation Batch files. >>Reset_Script_Paths_ArcGISPro.bat
echo @echo The batch files will be reset to the state when you first downloaded the batch file. >>Reset_Script_Paths_ArcGISPro.bat
echo @echo Type Ctrl + C to cancel execution. >>Reset_Script_Paths_ArcGISPro.bat  
echo pause >>Reset_Script_Paths_ArcGISPro.bat  
echo. >>Reset_Script_Paths_ArcGISPro.bat  
rem echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\batchFiles arcgis%id% arcgisVer *.bat >>Reset_Script_Paths_ArcGISPro.bat
rem echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\batchFiles\ArcGISPro %var% currFolder *.bat >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config %var% currFolder *.xml >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config\sample0 %var% currFolder *.xml >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config\sample1 %var% currFolder *.xml >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Config\sample2 %var% currFolder *.xml >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\RasterFunctionTemplates %var% currFolder *.xml >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo "c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" %var%\scripts\search_replace.py %var%\Parameter\Rastertype %var% currFolder *.xml >>Reset_Script_Paths_ArcGISPro.bat
echo. >>Reset_Script_Paths_ArcGISPro.bat
echo pause >>Reset_Script_Paths_ArcGISPro.bat


rem ECHO "Successfully set ArcGIS version number to %id%."
ECHO "Successfully set sample paths to %var%."
goto :endofbatch 

:ShowError
ECHO "ERROR: Could not find Python Install Location in c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\"

:endofbatch
pause
