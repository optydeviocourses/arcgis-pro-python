@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
echo Tentativa %Contador% Publicando Todos os Rasters

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Droga.py
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Mvi.py

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%

echo Processo iniciado às %STARTTIME%  finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on
