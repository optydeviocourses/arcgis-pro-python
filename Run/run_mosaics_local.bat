@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%

python.exe c:/Users/inteligencia/Documents/Projetos/Process/Mosaics/Mosaic_Local/Create_Mosaic_Mvi.py &
python.exe c:/Users/inteligencia/Documents/Projetos/Process/Rasters/Mosaic_Local/Create_Mosaic_Arma &
python.exe c:/Users/inteligencia/Documents/Projetos/Process/Rasters/Mosaic_Local/Create_Mosaic_Droga

rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on