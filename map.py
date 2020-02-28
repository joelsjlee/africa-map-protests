import shapefile
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure
import itertools


#importing shp and dbf
shp = open("World-Provinces/ne_10m_admin_1_states_provinces.shp", "rb")
dbf = open("World-Provinces/ne_10m_admin_1_states_provinces.dbf", "rb")
sf = shapefile.Reader(shp=shp, dbf=dbf)

#initializing arrays for data for Bokeh
lats = []
lons = []
names = []

#For each shape in the shapefile (each province)
for shprec in sf.shapeRecords():
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


color_mapper = LogColorMapper(palette=palette)

#Loading data into Bokeh
data=dict(
    x=lats,
    y=lons,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

#Plot
p = figure(
    title="Protests", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,)
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data,
          # fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

show(p)
