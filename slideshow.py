import sys, os, random



commands = ["-s 1000 -i 1000000 --color-type 2 --color 0 fractals/bonsai.frct",\
"-s 1000 -i 1000000 --color-type 1 --color-file colors.txt fractals/snowflake.frct",\
"-s 1400 -i 1000000 --color-type 2 --color 0 fractals/mushroom.frct",\
"-s 600 -i 1000000 --color-type 2 --color 2 fractals/crystaledit.frct",\
"-s 150 -i 1000000 --color-type 2 --color 1 fractals/fern2.frct",\
"-s 100 -i 1000000 --color-type 2 --color 1 fractals/fern.frct",\
"-s 1000 -i 1000000 --color-type 2 --color 0 fractals/crystal.frct",\
"-s 1000 -i 1000000 --color-type 1 --color-file colors.txt fractals\island.frct",\
"-s 700 -i 1000000 --color-type 1 --color-file colors.txt fractals/new.frct",\
"-s 1000 -i 1000000 --color-type 2 --color 0 fractals/pine.frct",\
"-s 800 -i 2050000 --color-type 3 --grad-int 2,2,2 --start-int 20,20,20 --end-int 240,240,240 fractals/pine.frct",\
"-s 800 -i 2000000 --color-type 3 --grad-int -2,2,0 --start-int 240,20,0 --end-int 20,240,0 fractals/pine.frct",\
"-s 100 -i 2000000 --color-type 3 --grad-int 4,4,4 --start-int 20,20,20 --end-int 250,250,250 fractals/fern.frct",\
"-s 1000 -i 2000000 --color-type 3 --grad-int 4,4,4 --start-int 20,20,20 --end-int 240,240,240 fractals/mushroom.frct",\
"-s 1000 -i 2000000 --color-type 3 --grad-int 1,4,0 --start-int 100,0,0 --end-int 255,255,0 fractals/mushroom.frct",\
"-s 1000 -i 2000000 --color-type 3 --grad-int 1,4,0 --start-int 100,0,0 --end-int 255,255,0 fractals/snowflake.frct",\
"-s 1000 -i 2000000 --color-type 3 --grad-int 1,4,0 --start-int 100,0,0 --end-int 255,255,0 fractals/crystaledit.frct",\
"-s 1000 -i 2000000 --color-type 3 --grad-int 4,0,1 --start-int 0,0,120 --end-int 240,0,240 fractals/pine.frct",\
"-s 1000 -i 2000000 --color-type 3 --grad-int 0,4,1 --start-int 0,0,120 --end-int 0,255,255 fractals/bonsai.frct",\
"-s 800 -i 2000000 --color-type 3 --grad-int 0,4,1 --start-int 0,0,120 --end-int 0,240,240 fractals/tree.frct"]

while 1:
    os.system("./pyafg.py %s"%random.choice(commands))
