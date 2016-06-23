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

def algo (region,output, word):
    reg = [0 for i in range(0,23)]
    total = 0
    for line in region: #reg_num number
        items = line.rstrip('\n').split('\t')
        reg[int(items[0])]=int(items[1])
        total = total+int(items[1])
    reg=np.array(reg)
    max_percent=np.max(reg)
    plt.figure(figsize=(15,15))
    ax = plt.subplot(111)
    m = Basemap(projection='merc', lat_0=45, lon_0=0,
                resolution = 'h', area_thresh = 10.0,
                llcrnrlat=41.33, llcrnrlon=-5,   
                urcrnrlat=51.5, urcrnrlon=9.7) 
    m.drawcoastlines()
    #m.drawcountries()  # french border does not fit with region ones
    m.fillcontinents(color='lightgrey',lake_color='white')
    m.drawmapboundary(fill_color='white')

    sf = shapefile.Reader("./geodata/FRA_adm1")
    shapes = sf.shapes()
    records = sf.records()
    for record, shape in zip(records,shapes):
        lons,lats = zip(*shape.points)
        data = np.array(m(lons, lats)).T
        if len(shape.parts) == 1:
            segs = [data,]
        else:
            segs = []
            for i in range(1,len(shape.parts)):
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])
        
        lines = LineCollection(segs,antialiaseds=(1,))
        lines.set_edgecolors('k')
        lines.set_linewidth(0.5)
        lines.set_facecolors('brown')
        lines.set_alpha(float(reg[record[3]])/max_percent) #record[3] est le numero de region
        ax.add_collection(lines)   

    plt.savefig(word+'-'+str(total)+'.png',dpi=300)

    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region",
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="input file name")
    parser.add_argument("-o", "--output",
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="output")
    parser.add_argument("word", 
                        help="display a square of a given number")
    args = parser.parse_args()
    ids_dumped = algo (args.region,args.output, args.word)
    
    args.region.close()
    args.output.close()

if __name__ == "__main__":
    main()
