#!/usr/bin/sh
#Remember, remove the -o to view the fractal in pygame
#Draws Barnsley's Fern
python pyafg.py -s 100 -o fern.png fractals/fern.frct
#Draws it very big. Note how we've used the offsets to zoom in on
#a specific portion of it.
python pyafg.py -s 1000 -o fernbig.png -g 800x600 -x -880 -y -500 -i 2000000 fractals/fern.frct
#Draw the fern using colors from the colors.txt file.
python pyafg.py -s 100 -o fern_colored.png --color-type 1 --color-file colors.txt fractals/fern.frct
#Bonsai
python pyafg.py -s 600 --color-type 2 --color 1 -i 320000 -o bonsai.png fractals/bonsai.frct 
#_Nice_ Fern
python pyafg.py -s 100 --color-type 2 --color 1 -i 1100000 -o fern.png fractals/fern.frct
#Snowflakey hypnosis
python pyafg.py -s 600 --color-type 1 --color-file colors.txt -i 200000 -o snow.png fractals/snowflake-1.frct 
#This shows how to use the gradient option
python pyafg.py -s 800 -i 2050000 --color-type 3 --grad-int 2,2,2 --start-int 20,20,20 --end-int 240,240,240 fractals/pine.frct
#More gradient examples
python pyafg.py -s 1000 -i 2000000 --color-type 3 --grad-int 4,4,4 --start-int 20,20,20 --end-int 240,240,240 fractals/mushroom.frct
#
python pyafg.py -s 800 -i 2000000 --color-type 3 --grad-int 1,4,0 --start-int 100,0,0 --end-int 255,255,0 fractals/crystaledit.frct
#
python pyafg.py -s 1000 -i 2000000 --color-type 3 --grad-int 1,4,0 --start-int 100,0,0 --end-int 255,255,0 fractals/snowflake.frct
