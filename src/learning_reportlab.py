import urllib
import urllib.request

from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label

def printlist(a):
    for i in a:
        if type(i) is list:
            printlist(i)
        else:
            print (i)


# notice 1 :urllib is move to sub-module request
# notice 2:the url to retrive data is changed, the noaa web site is rebuild.
#noticce 3: zipped object should be converted to list type,

data = []

response = urllib.request.urlopen('http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt')

print('http header:\n', response.info())
print('http statues:', response.getcode())
print('url:', response.geturl())

print('-------------------------------------------------------------------')

for raw_data in response.readlines():
    str = bytes.decode(raw_data, "utf-8")
    if str[0] not in ("#", ":"):
        data.append(str.split())
    else:
        pass   #print (str)

response.close()

"""
data = [
    #    Year  Month  Predicted  High  Low
        (2007,  8,    113.2,     114.2, 112.2),
        (2007,  9,    112.8,     115.8, 109.8),
        (2007, 10,    111.0,     116.0, 106.0),
        (2007, 11,    109.8,     116.8, 102.8),
        (2007, 12,    107.3,     115.3,  99.3),
        (2008,  1,    105.2,     114.2,  96.2),
        (2008,  2,    104.1,     114.1,  94.1),
        (2008,  3,     99.9,     110.9,  88.9),
        (2008,  4,     94.8,     106.8,  82.8),
        (2008,  5,     91.2,     104.2,  78.2),
        ]
"""


pred = [float( row[2]) - 40 for row in data]
high = [float( row[3]) - 40 for row in data]
low  = [float( row[4]) - 40 for row in data]
times = [200 * ((float(row[0]) + float(row[1]) / 12.0) - 2007) - 110 for row in data]

drawing = Drawing(400, 200)

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300

# notice, type convert
lp.data = [list(zip(times, pred)), list(zip(times, high)), list(zip(times, low))]


lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green


drawing.add(lp)

renderPDF.drawToFile(drawing, 'e:\\github\\report1.pdf','sunspot')

"""
drawing.add (PolyLine(zip(times, pred), strokeColor=colors.blue))
drawing.add (PolyLine(zip(times, high), strokeColor=colors.red))
drawing.add (PolyLine(zip(times, low), strokeColor=colors.green))
drawing.add (String(65, 115, 'Sunspots', fonSize=18, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'd:\\github\\report1.pdf', 'Sunspots')
"""