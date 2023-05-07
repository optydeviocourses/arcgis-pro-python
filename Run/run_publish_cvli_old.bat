@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
set MVI=c:/Users/inteligencia/Documents/Projetos/Publish/Rasters/Run_Publish_Mvi.py
set PYTHON=C:/Progra~1/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe

start %PYTHON% %MVI% %1
IF ERRORLEVEL 1 goto erroMvi
goto end

:erroMvi
start erroMvi.vbs

rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on
:end

