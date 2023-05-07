@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%

set Contador=1
:Loop_rasters
echo Tentativa %Contador% Publicando Todos os Rasters

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Droga.py
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Arma.py
C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\Rasters\Run_Publish_Mvi.py

if not %errorlevel% EQU 0 if %Contador% LSS 3 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_rasters
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)

rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on


