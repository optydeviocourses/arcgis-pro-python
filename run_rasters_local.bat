@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%

set Contador=1

:Loop_process
cls
echo Tentativa %Contador% Processando Rasters Local

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Local\Run_Raster_Droga.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Local\Run_Raster_Arma.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Local\Run_Raster_Mvi.py

if not %errorlevel% EQU 0 if %Contador% LSS 3 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_process
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
    rem goto :end_process
)
echo Processamento de Rasters Local realizado com sucesso !!!

rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on