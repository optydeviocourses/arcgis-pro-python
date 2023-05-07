@echo off
rem PUBLICAÇÕES DAS LAYERS

set STARTTIME=%TIME%
set Contador=1
:Loop_layers
echo Tentativa %Contador% Publicando Layers de Recursos e  Hotspots

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Feature\Run_Publish_Recursos.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\HotSpotsAnalysis\Run_Publish_Ha_Cvp.py

if not %errorlevel% EQU 0 if %Contador% LSS 2 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_layers
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

::
rem PUBLIÇÕES DOS RASTERS

set Contador=1
:Loop_drogas
echo Tentativa %Contador% Publicando Rasters de Drogas

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Droga.py

if not %errorlevel% EQU 0 if %Contador% LSS 3 (
    set \a Contador+=1
    timeout \t 10 2>&1>nul
    goto :Loop_drogas
) else (
    echo Infelizmente o comando falhou
    timeout \t 10 2>&1>nul
)

::

set Contador=1
:Loop_armas
echo Tentativa %Contador% Publicando Rasters de Armas

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py

if not %errorlevel% EQU 0 if %Contador% LSS 3 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_armas
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

::

set Contador=1
:Loop_mvi
echo Tentativa %Contador% Publicando Rasters de MVI\CVLI

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Mvi.py

if not %errorlevel% EQU 0 if %Contador% LSS 3 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_mvi
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%
@echo on
echo Tempo de processamento %DURATION% seg.