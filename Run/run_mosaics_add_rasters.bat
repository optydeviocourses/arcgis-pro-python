@echo off
rem Inicio do procedimento.
set STARTTIME=%TIME%

python.exe c:/Users/inteligencia/Documents/Projetos/Process/Mosaics/Add_Rasters/Add_Mosaic_Droga.py &
python.exe c:/Users/inteligencia/Documents/Projetos/Process/Mosaics/Add_Rasters/Add_Mosaic_Arma.py &
python.exe c:/Users/inteligencia/Documents/Projetos/Process/Mosaics/Add_Rasters/Add_Mosaic_Mvi.py


rem Fim do procedimento.
set ENDTIME=%TIME%
@echo on