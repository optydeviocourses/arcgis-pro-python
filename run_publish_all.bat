@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%
echo Publicando Todos os Rasters

rem publicando as camadas de recursos e hotspots
call run_publish_recursos.bat
call run_publish_hotspots.bat

rem preparando o processamento dos rasters
call run_publish_hasters.bat

rem Fim do procedimento.
set ENDTIME=%TIME%
set /A DURATION=%ENDTIME%-%STARTTIME%

echo Processo iniciado às %STARTTIME%  finalizado às %ENDTIME%
echo Processamentos finalizados !
echo Tempo total de processamento %DURATION% seg.
@echo on
