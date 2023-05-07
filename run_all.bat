@echo off
set STARTTIME=%TIME%

rem Processamentos

set Contador=1
:Loop_process
cls
echo Tentativa %Contador% Processando Rasters

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Rasters_Sde\Run_Raster_Droga.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Rasters_Sde\Run_Raster_Arma.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Rasters_Sde\Run_Raster_Mvi.py

if not %errorlevel% EQU 0 if %Contador% LSS 3 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_process
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
    rem goto :end_process
)
echo Processamento de Rasters realizado com sucesso !!!
echo Iniciando as Publicações ...
::

rem Publicações

set Contador=1
:Loop_rasters
echo Tentativa %Contador% Publicando Rasters de Drogas

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Droga.py

if not %errorlevel% EQU 0 if %Contador% LSS 2 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_rasters
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

::
set Contador=1
:Loop_rasters
echo Tentativa %Contador% Publicando Rasters de Armas

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py

if not %errorlevel% EQU 0 if %Contador% LSS 2 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_rasters
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

::
set Contador=1
:Loop_rasters
echo Tentativa %Contador% Publicando Rasters de MVI\CVLI

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Mvi.py

if not %errorlevel% EQU 0 if %Contador% LSS 2 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_rasters
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

::
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

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%
@echo on
echo Tempo de processamento %DURATION% seg.