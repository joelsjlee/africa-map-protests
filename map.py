import shapefile
from bokeh.io import show, output_file
from bokeh.models import LogColorMapper, Circle, ColumnDataSource
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
import itertools
import statistics
import math
import csv

#This is the function for making the map of africa graph
def shp():
    #importing shp and dbf
    shp = open("World-Provinces/africa.shp", "rb")
    dbf = open("World-Provinces/africa.dbf", "rb")
    sf = shapefile.Reader(shp=shp, dbf=dbf)

    #initializing arrays for data for Bokeh
    lats = []
    lons = []
    rates = []
    names = []
    midx = 22
    midy = 5
    points = 0

    #For each shape in the shapefile (each province)
    for shprec in sf.shapeRecords():
        names.append(shprec.record[9])
        #Not quite sure what's going on here but copied code that fixed the strange lines issues
        lat, lon = map(list, zip(*shprec.shape.points))
        indices = shprec.shape.parts.tolist()
        lat = [lat[i:j] + [float('NaN')] for i, j in zip(indices, indices[1:]+[None])]
        lon = [lon[i:j] + [float('NaN')] for i, j in zip(indices, indices[1:]+[None])]
        lat = list(itertools.chain.from_iterable(lat))
        lon = list(itertools.chain.from_iterable(lon))
        #Eventually adding the list of lats for the shape to global lats list,
        #and list of lons for the shape to global lons list
        lats.append(lat)
        lons.append(lon)
        rates.append(math.sqrt((lat[0]-midx)**2 + (lon[0]-midy)**2))

    max = 0
    for i in rates:
        if i > max:
            max = i
    onerate = [i/max for i in rates]
    color_mapper = LogColorMapper(palette=palette)

    #Loading data into Bokeh
    data=dict(
        x=lats,
        y=lons,
        rate=onerate,
        name=names
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    #Plot
    p = figure(
        title="Protests", tools=TOOLS,
        x_axis_location=None, y_axis_location=None,tooltips=[
            ("Name", "@name"), ("% Distance from Mid", "@rate%"), ("(Long, Lat)", "($x, $y)")
        ])

    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=data,
              fill_color={'field': 'rate', 'transform': color_mapper},
              fill_alpha=0.7, line_color="white", line_width=0.5)
    # show(p)
    return p

def points(plot):
    lats = []
    lons = []
    with open("protests.csv", "r", encoding="utf-8") as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            try:
                if row["LONG"] == "checked":
                    lats.append(float(row["Unique Key"]))
                    lons.append(float(row["LAT"]))
                else:
                    lats.append(float(row["LAT"]))
                    lons.append(float(row["LONG"]))
            except Exception as e:
                print("(" + str(row["LONG"]) + ", " +  str(row["LAT"]) + ")")

    # for i in range(len(lats)):
    #     print("(" + str(lats[i]) + ", " +  str(lons[i]) + ")")
    # print(lats[:5])
    # print(lons[:5])


    data=ColumnDataSource(dict(lons=lons,
              lats=lats))

    glyph = Circle(x="lons", y="lats", fill_color="red", fill_alpha=0.8)

    plot.add_glyph(data, glyph)
    output_file("index.html")
    show(plot)


if __name__ == "__main__":
    plot = shp()
    points(plot)
