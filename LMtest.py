from pylab import *
#import matplotlib.pyplot as plt
#from scipy.optimize import leastsq

import sys
from scipy.optimize import leastsq
import numpy as np
from numpy import array
from numpy import sqrt
import matplotlib.pyplot as plt
import time #to allow time stamp on output
# Test for Python version:
cur_version = sys.version_info

"""
LMtest.py
Author: Dr. D. S. Stutts
Original release: 12-18-2015
Port of LMFtest.m by D. S. Stutts 2-5-2014

LMtest.py uses the Levenberg-Marquardt (LM)
nonlinear least squares algorithm to
optimize the model in the least squares
sense.  The LM algorithm is invoked
via a call to leastsq(rez, z0, args=(yy, xx),
full_output=1) from the scipy.optimize library.

See: http://docs.scipy.org/doc/scipy-0.14.0/
reference/generated/scipy.optimize.leastsq.html
for more information.

 Data is supplied in the file data.txt as tab-delimitted (x,y) pairs
 of floating point numbers.

 Unknown parameter vector: z
 Curve to fit is: F(r,z) = z[0]+z[1]*exp(z[2]*r)
 Solution is: z[0] = 0.625, z[1] = 1.33, and z[2] = -0.5

 Initial guess vector: x0=[1,1,-1]
 Care must be taken to choose an initial guess vector
 which will allow the algorithm to converge. For example,
 the above choice converges, but [1,1,1] and [0,0,0] do not.
 The function call to leastsq() is:
 leastsq(rez, x0, args=(yy, xx), full_output=1)
 where:
    res(z, yy, r) = function returning the residual (difference between
          the model and the data) provided by the user, and
          called by leastsq().  The first argument, z, contains an array
          of the unknown parameters, the second argument contains the measured
          dependant veriable, and the third argument contains an array of the
          independent veriables -- x, in this case.
    x0 = initial quess solution vector provided by the user.

    args = comma separated list of additional arguments (other than
    z) called by res().

    full_output = Boolean variable (False, True, or 0, 1 (or any non-zero
    number)).  When set to True, leastsq() returns all of the optional
    output parameters, including an array of the residuals which is
    used to compute the standard error (unbiased estimate of uncertainty).

    Examples

    From the command line:

    python LMTest.py data.txt

    From an iPython or Jupyter interactive console:

    run LMTest.py data.txt

"""
# Create empty lists:
x = []
y = []

# Set the desired resolution:
res = 72# DPI.  Fine for EPS, but should use higher for PNG.

#plottype = ''# Defaults to PNG
plottype = 'EPS'# Comment this out for PNG output.

infile = sys.argv[1] #Open input file from command line

try:
    data = open(infile, "r")# get array out of input file
except:
    print ("Cannot find input file; Please try again.")
    sys.exit(0)

data.seek(0) # Reset file pointer to the beginning

linecount = 0
# Read the data from the input file:
if cur_version[0]==3:# This is necesary due to the change in the type
    for line in data:# returned by the map function in Python 3.x.x.
        linedat = list(map(float, line.split()))
        x.append(linedat[0])
        y.append(linedat[1])
        linecount += 1
else:
    for line in data:
        x.append(map(float, line.split())[0])
        y.append(map(float, line.split())[1])
        linecount += 1
xx = array(x)
yy = array(y)
xmax = max(xx)
xmin = min(xx)
ymax = max(yy)
ymin = min(yy)
# Close the input file:
close(infile)

# Define the model:
def F(r,z):
    return z[0]+z[1]*exp(z[2]*r)

# Define the residual function:
def rez(z, yy, r):
    return yy - F(r,z)

x0=[1,1,-1]# Initial guess

# Find the best values:
output = leastsq(rez, x0, args=(yy, xx), full_output=1)
err2 = output[2]['fvec']*output[2]['fvec'] #Squared deviations
sig = sqrt(sum(err2)/(len(err2)-3)) # Unbiased uncertainty estimate
a = output[0][0] # Optimal parameters
b = output[0][1]
c = output[0][2]
# Print the solutions and the standard error:
print ("a = ",a)
print ("b = ",b)
print ("c = ",c)
print ("standard error = ", sig)

# Create a list of the optimal parameters:
coeffs = [a,b,c]
# Plot the model and the data for comparision:
plt.plot(xx, F(xx, coeffs), 'r-', label='model')
plt.plot(xx, yy, 'go', label='data')
legend = plt.legend(loc='upper right', shadow=True, fontsize='large')
xlabel('x')
ylabel('F(x)')
plt.annotate(r"$\sigma$ = "+'{: 3.2e}'.format(sig),xy=(xmax*0.7,ymax*0.75))
grid(True)
# Put a nice background color on the legend:
legend.get_frame().set_facecolor('#00FFCC')
# Add date and time in plot title:
loctime = time.asctime(time.localtime(time.time()))
#Save graph:
if plottype=='PNG' or plottype=='':# Default to PNG
# Save plot as PNG:
    plotname = infile.split('.')[0]+"model"+loctime+".PNG"
    plt.savefig(plotname,format='png', dpi=res)
else:# Save plot as EPS:
    plotname = infile.split('.')[0]+"model"+loctime+".EPS"
    plt.savefig(plotname,format='eps', dpi=res)

plt.show()# Show the plot
