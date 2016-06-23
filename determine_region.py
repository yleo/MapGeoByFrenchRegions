from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib import cm
import shapefile
import matplotlib.path as mplPath
import numpy as np
import sys
import shapefile, csv
import sys
import argparse
import datetime
import time
import random

def algo (tweets,grid165,  output):
    reg = {}
    coords=(0,0)
    m = Basemap(projection='merc', lat_0=45, lon_0=0,
                resolution = 'h', area_thresh = 10.0,
                llcrnrlat=41.33, llcrnrlon=-5,   
                urcrnrlat=51.5, urcrnrlon=9.7) 

    for line in grid165:
        items = line.rstrip('\n').split(' ')
        reg[(int(items[0])/10000,int(items[1])/10000)]=int(items[2])
        
    for line in tweets:
        items = line.rstrip('\n').split('\t')
        coords = m(float(items[1]),float(items[0])) #lat,lon
        coords_grid = (int(coords[0]/10000), int(coords[1]/10000))
        if (coords_grid in reg):
            output.write(str(items[0])+"\t"+str(items[1])+"\t"+str(reg[coords_grid])+"\n")

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tweets",
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="input file name")
    parser.add_argument("-g", "--grid",
                        type=argparse.FileType('r'),
                        help="input file name")
    parser.add_argument("-o", "--output",
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="output")
       
    args = parser.parse_args()
    ids_dumped = algo (args.tweets,args.grid,args.output)
    
    args.tweets.close()
    args.grid.close()
    args.output.close()

if __name__ == "__main__":
    main()
