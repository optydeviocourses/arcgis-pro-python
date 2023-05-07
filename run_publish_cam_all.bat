@echo off
rem PUBLICAÇÕES DAS LAYERS

cls
set STARTTIME=%TIME%

echo Publicando Layers de Recursos ... (%TIME%)
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Feature\Run_Publish_Recursos.py

echo Publicando Layers de Hotspots de CVP ... (%TIME%)
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\HotSpotsAnalysis\Run_Publish_Ha_Cvp.py

rem PUBLIÇÕES DOS RASTERS

echo Publicando Rasters de Drogas ... (%TIME%)
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Droga.py

echo Publicando Rasters de Armas ... (%TIME%)
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py

echo Publicando Rasters de MVI\CVLI ... (%TIME%)
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Mvi.py

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%
cls
echo Processo iniciado às %STARTTIME%  finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on