import os
import math
import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import random

class boundary:
    def __init__(self, points):
        """
        points: a numpy array of x,y coordinate points that define the boundary of Ω (Ωs).  
        The points must be in sequential-clockwise order.
        """
        self.points = points
    
    @property
    def edges(self):
        ''' 
        edge_list: Returns a list of tuples that each contain the two vertices of an edge 
        '''
        edge_list = []
        for i in range(0,len(self.points)-1): #for each edge
            vertex1 = (self.points[i,0], self.points[i,1]) #first vertex
            vertex2 = (self.points[i+1,0], self.points[i+1,1]) #second vertex
            edge_list.append((vertex1,vertex2)) #save each edge as a tuple with the coordinates of the vertices

        #save the edge from the last point to the first point
        vertex1 = (self.points[-1,0], self.points[-1,1])
        vertex2 = (self.points[0,0], self.points[0,1])
        edge_list.append((vertex1,vertex2))

        return edge_list
         
    def contains(self, point):
        import sys
        _huge = sys.float_info.max
        _tiny = sys.float_info.min
        _eps = 0.00001

        # We start on the outside of the polygon
        inside = False
        for i in range(0,len(self.points)): #for each edge
            A, B = self.edges[i] #set A, B as the vertices of the edge
    
            #Reorder such that A is below B
            if A[1] > B[1]:
                A, B = B, A

            #Make notation easy to follow and write
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            Px = point[0]
            Py = point[1]

            #Check if P is at the same height as A or B, and move it a small amount if so
            if (Py == Ay or Py == By):
                Py += _eps
            
            #Check if P is above, below, or to the right of the edge AB
            if (Py > By or Py < Ay or Px > max(Ax, Bx)):
                continue

            #Check if P is to the left of both A and B
            if Px < min(Ax, Bx):
                inside = not inside
                continue

            #Compare slopes of AB and AP.  Toggle boolean if AP is a greater slope.    
            if abs(Ax-Bx) > _tiny:
                m_edge = (By - Ay) / (Bx - Ax)
            else:
                m_edge = _huge
                
            if abs(Ax-Px) > _tiny:
                m_point = (Py - Ay) / (Px - Ax)
            elif Ax > Bx: #assign the correct sign to 'huge'
                m_point = -_huge 
            else:
                m_point = _huge

            if m_point > m_edge:
                # The ray intersects with the edge
                inside = not inside
                continue

        return inside


    
def rangeLimits(A): #(P), returns bounds
    
    '''
    Returns the bounds of a numpy array as a list of length 4, corresponding 
    to (xmin, xmax, ymin, ymax)
    '''
    
    xmin = np.amin(P[:,0])
    xmax = np.amax(P[:,0])
    ymin = np.amin(P[:,1])
    ymax = np.amax(P[:,1])
    return (xmin, xmax, ymin, ymax) 
    
def distancefromPoint(p1,p2):
    
    '''
    Calculates and returns the scalar distance between two points
    '''
    
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    ans = np.sqrt(np.square(x2-x1)+np.square(y2-y1))
    return ans

def rayTrace(q,b): #(agriculturalField,bounds), returns fieldPixels
    
    '''
    Sweeps through each pixel in the range and determines whether or not 
    the pixel is within the enclosed boundary polygon
    '''
    
    X = []
    Y = []
    for x in range(b[0],b[1]):
        for y in range(b[2],b[3]):
            if q.contains([x, y]) == True:
                X.append((x))
                Y.append((y))
    aX = np.array([X])
    aY = np.array([Y])
    A = np.vstack((aX,aY)).T
    return A

def generateDesigns(variables,N,l,b,designs): 
    #(geneticVariables,numberSensors,loopNumber,bounds,designMatrix), returns designMatrix
    
    '''
    Generates designMatrix for a given number of sensors, where the columns of indices
    2N hold x-coordinates of sensors and columns of indices 2N+1 hold y-coordinates
    The final column of the designMatrix is returned as 0 and is scored with the fitness function later
    '''
    
    S = variables[0] #population
    P = variables[1] #parents
    C = variables[2] #children
    
    n = P+C if l > 0 else 0 #select where in the designMatrix to start generating strings
    for i in range(n,S):
        for j in range(0,N):
            phi = random.rand() #random number 0-1
            xi = int(round(phi*(b[1]-b[0])+b[0])) #pick random x-coordinate within xmin:xmax
            phi = random.rand() #random number 0-1
            yi = int(round(phi*(b[3]-b[2])+b[2])) #pick random y-coordinate within ymin:ymax
            designs[i,(2*j)] = xi
            designs[i,(2*j)+1] = yi
    return designs

def fitness(S,N,A,designs,radius): 
    #(population,numberSensors,fieldPixels,designMatrix,coverageRadius), returns designMatrix with scores
    
    '''
    Scores the designMatrix on a scale from 0-1, where 1 is 100% coverage of
    the field pixels with sensors
    '''
    
    coverage = 0
    for i in range(0,S): #for each design
        for j in range(0,len(A[:,0])): #for each point in the field
            for k in range(0,N): # for all sensors

                #if point within range of any sensor, count point as within range and continue to next point
                distance = distancefromPoint(A[j,:],[designs[i,(2*k)],designs[i,(2*k)+1]])
                if distance <= radius:
                     coverage += 1
                     break

        #Score the design
        designs[i,-1] = coverage/len(A[:,0])
        coverage = 0
    return designs

def mutate_randomReset(designs,variables,b):#(designMatrix,geneticVariables,bounds)
    
    '''
    Randomly mutates one coordinate of the children designs
    '''
    
    S = variables[0] #population
    P = variables[1] #parents
    C = variables[2] #children
    for j in range(P,P+C):
        designMatrix[j,:] = designMatrix[j-P,:]
        coordinateSelect = random.randint(0,len(designMatrix[j,:])-1)
        if (coordinateSelect % 2) == 0: #if the selected mutation is a y-coordinate
            permissibleRange = (b[2],b[3]) #permissible mutation range is ymin:ymax
        else: #else if a x coordinate,
            permissibleRange = (b[0],b[1]) #permissible mutation range is xmin:xmax
        designMatrix[j,coordinateSelect] = random.randint(permissibleRange[0],permissibleRange[1])
    return designMatrix
