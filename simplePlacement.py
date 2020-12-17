# Point-in-Polygon Using Ray Tracing Method
#Payton Goodrich
#Dec. 17th, 2020

#This program determines whether or not a point is within or without of a boundary that is defined by a numpy array of clockwise-sequential x,y coordinates.

import numpy as np
import matplotlib.pyplot as plt

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

    
#Program Start
if __name__ == "__main__":

    #Define the boundary, P
    P = np.array([[50, 70], [60, 65],[70, 50],[80, 50],[80, 40],[70, 40],[60, 10],[50, 20],[40, 10],[20, 0],[0, 30],[20, 40],[30, 60]])

    #Define the enclosed boundary, q
    q = boundary(P)


    #Upper and Lower Limit Bounds
    xmin = np.amin(P[:,0])
    xmax = np.amax(P[:,0])
    ymin = np.amin(P[:,1])
    ymax = np.amax(P[:,1])

    #Calculate an Ax2 array of points within the boundary Ω
    aMatrixX = []
    aMatrixY = []
    for x in range(xmin,xmax):
        for y in range(ymin,ymax):
            if q.contains([x, y]) == True:
                aMatrixX.append([x])
                aMatrixY.append([y])

    #Plot the points of P (that make up the boundary Ωs)
    #Plot the points of A (each point within the boundary, ie Ω)
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.scatter(aMatrixX, aMatrixY, label='Interior Points')
    ax.scatter(P[:,0], P[:,1], c='#d62728', marker='D', label='Boundary Points')
    fig.suptitle('Enclosed Boundary Ω')
    ax.legend()
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.show()



    #Test points for ray trace algorithm

    # Test 1: Point inside boundary - Output = TRUE
    p1 = [40, 50]
    print("P1 inside boundary: " + str(q.contains(p1)))


    # Test 2: Point inside boundary at same height as vertex - Output = TRUE
    p2 = [40,40]
    print("P2 inside boundary: " + str(q.contains(p2)))


    # Test 3: Point inside boundary crossing multiple vertices - Output = TRUE
    p3 = [20,10]
    print("P3 inside boundary: " + str(q.contains(p3)))


    # Test 4: Point on minimum height vertex of boundary - Output = TRUE
    p4 = [20,0]
    print("P4 inside boundary: " + str(q.contains(p4)))


    # Test 5: Point set as the maximum height vertex of boundary - Output = FALSE
    p5 = [50,70]
    print("P5 inside boundary: " + str(q.contains(p5)))


    #Test 6: Point outside to the left of the boundary - Output = FALSE
    p6 = [-10,40]
    print("P6 inside boundary: " + str(q.contains(p6)))


    #Test 7: Point outside to the right of the boundary - Output = FALSE
    p7 = [70,15]
    print("P7 inside boundary: " + str(q.contains(p7)))
