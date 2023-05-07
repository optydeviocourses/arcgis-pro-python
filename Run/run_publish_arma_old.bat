@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
set ARMA=c:/Users/inteligencia/Documents/Projetos/Publish/Rasters/Run_Publish_Arma.py

start C:/Progra~1/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe %ARMA% %1
IF ERRORLEVEL 1 goto erroArma
goto end

:erroArma
start erroArma.vbs

rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on

:end



