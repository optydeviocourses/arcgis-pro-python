@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
echo Publicando Todos os Rasters

rem preparando o processamento dos rasters
call run_publish_local.bat

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Droga.py
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Mvi.py

rem publicando as camadas de recursos e hotspots
call run_publish_recursos.bat
call run publish_hotspots.bat

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%

echo Processo iniciado às %STARTTIME%  finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on
