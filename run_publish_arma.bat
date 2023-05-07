@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%

echo Publicando Rasters de Armas ...

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%

cls
echo Processo iniciado às %STARTTIME%  finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on

