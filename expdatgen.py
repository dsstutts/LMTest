""" 
File: expdatgen.py
Author: Dr. D. S. Stutts
First release: 12-18-2015

Generates sample data for exponential curve fit example.
Based on expdatgen.m by D. S. Stutts: 2-4-2014
"""

# Import all of the necessary python libraries:
from pylab import *
import matplotlib.pyplot as plt
import itertools# itteration tools for writedat() defined below

# Create some empty lists to work with:
x = []
y = []
xx = []
yy = []

# Create a numpy array of the independent variable x:
x = linspace(-5,5, num=13)

def F(x):
    return 0.625+1.33*exp(-0.5*x);# y-vector
       

# Function to write formatted tab-delimited x,y data
# from: http://rosettacode.org/wiki/Write_float_arrays_to_a_text_file#Python:
def writedat(filename, x, y, xprecision=6, yprecision=6):
    with open(filename,'w') as f:
        for a, b in itertools.izip(x, y):
            print >> f, "%.*g\t%.*g" % (xprecision, a, yprecision, b)
            close(filename)

# Create array of function values for each x:
y = F(x)

# Write the data to data.txt:
writedat("data.txt", x, y)

infile = "data.txt"
# Check to make sure the data was written correctly:
try: 
    data = open(infile, "r")# Get array out of input file
except:
    print "Cannot find input file; Please try again."
    sys.exit(0)

# Close the input file:
close(infile)
# Parse the x,y pairs into two lists:
for line in data: # Separate the x,y data by splitting at the white space (tab).
        xx.append(map(float, (line).split())[0])
        yy.append(map(float, (line).split())[1])

# Recast the data lists into numpy arrays for plotting:     
xx = array(xx)
yy = array(yy) 
       
# Plot the data:
plt.plot(xx, yy, 'go', label='data')
plt.title("Experimental Data")
plt.xlabel('x')
plt.ylabel('F(x)')
grid(True) # Show a grid
plt.show()# Show the plot
