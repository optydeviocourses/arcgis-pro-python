@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
echo Publicando Hotspots de CVP ...

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\HotSpotsAnalysis\Run_Publish_Ha_Cvp.py

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%

echo Processo iniciado às %STARTTIME% finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on
