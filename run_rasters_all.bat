@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
echo Tentativa %Contador% Processando Rasters

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Rasters_Sde\Run_Raster_Droga.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Rasters_Sde\Run_Raster_Arma.py &
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Process\Rasters\Rasters_Sde\Run_Raster_Mvi.py

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%

cls
echo Processo iniciado às %STARTTIME%  finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on