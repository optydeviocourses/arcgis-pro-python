@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%

set Contador=1
:Loop_layers
echo Tentativa %Contador% Publicando Layers de Recursos e  Hotspots

C:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe C:\Users\inteligencia\Documents\Projetos\Publish\HotSpotsAnalysis\Run_Publish_Ha_Cvp.py

if not %errorlevel% EQU 0 if %Contador% LSS 2 (
    set \a Contador+=1
    timeout \t 5 2>&1>nul
    goto :Loop_layers
) else (
    echo Infelizmente o comando falhou
    timeout \t 5 2>&1>nul
)
rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on
