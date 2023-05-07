@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
set DROGA=c:/Users/inteligencia/Documents/Projetos/Publish/Rasters/Run_Publish_Droga.py

start C:/Progra~1/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe %DROGA% %1
IF ERRORLEVEL 1 goto erroDroga
goto end

:erroDroga
start erroDroga.vbs

rem Fim do procedimento.
set ENDTIME=%TIME%

@echo on
:end

