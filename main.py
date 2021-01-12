'''
Program Start
'''

#Define some number of boundary points in the field as a numpy array of x,y coordinates 
P = np.array([[0, 0], [0, 61],[55, 143],[101, 143],[123, 110],[101, 61],[55,61],[55,0]])

#Upper and Lower Limit Bounds
bounds = rangeLimits(P)

# Define the coverage radius
coverageRadius = 30
print('The effective coverage radius of the device is ' +str(coverageRadius) + ' meters')

#Generate the agricultural field as a boundary of interconnected boundary points, P, with ray tracing capability
agriculturalField = boundary(P)

#Generate an Ax2 array of points within the boundary, Ω
fieldPixels = rayTrace(agriculturalField,bounds)
print('The area of the field is approximately ' + str(len(fieldPixels[:,0])) + ' meters squared')

#Define Genetic Algorithm Variables
population = 50 
parents = 5 #number of parent designs kept in each iteration
children = 5 #number of children designs made & kept in each iteration
geneticVariables = (population, parents, children)
N_0 = 1 #Number of devices in the initial design

#Define exit criteria for the genetic loop
convergenceCheck = 10 #loops that can occur with the same fitness score before it is considered 'converged'
maxLoops = 100 #how many loops that occur for a given N before the program stops because it is taking too long
Nmax = 10
theoreticalBest = (N_0*np.pi*(coverageRadius**2))/len(fieldPixels[:,0])

#Error Checks
if maxLoops < convergenceCheck:
    raise Exception('The maximum number of loops must be greater than the minimum number of convergence loops')
if parents > population:
    raise Exception('The number of parent designs cannot exceed the total population of designs')

    
'''
Generate a global design matrix that will store the highest scoring design in designMatrix
Each row is the best design found for N sensors, where N is the row number + 1
Each row is a design where every two columns is an x,y coordinate of a sensor positioned within the field
The last value in each row is the fitness score (from 0-1)
Used for plotting the percentage of field coverage possible for N sensors
'''
globaldesignMatrix = []

'''
Generate a scoring vector that records the 'best' design's fitness for each loop in the genetic algorithm
Used for plotting how the genetic algorithm 'learns' and improves itself over time
Also used for determining when the algorithm converges on for a given 'N'
'''
bestFitness = np.zeros((maxLoops,1))
    
#Initialize Genetic Algorithm Counters
loopNumber = 0
numberSensors = N_0
print('Solving for ' + str(numberSensors) + ' sensors')

#Genetic Loop
while(bestFitness[loopNumber] < 1):
    
    #Initialize designMatrix if this is the first loop for this N
    if loopNumber == 0: designMatrix = np.zeros((population,(numberSensors*2)+1))

    #Generate Designs
    '''
    Define a matrix of 'designs' of size S x (2N+1)
    Each row is a design where every two columns is an x,y coordinate of a sensor positioned within the field
    The last column of each row is reserved for the fitness score (from 0-1)
    Used for calculating and ranking the fitness function in the genetic algorithm
    '''
    designMatrix = generateDesigns(geneticVariables,numberSensors,loopNumber,bounds,designMatrix)

    #Calculate Fitness
    designMatrix = fitness(population,numberSensors,fieldPixels,designMatrix,coverageRadius)

    #Rank Each Design
    ind = np.argsort(designMatrix[:,-1])[::-1] #remove the [::-1] to sort in ascending order
    designMatrix = designMatrix[ind]

    #Store the highest scoring design for future plotting
    bestFitness[loopNumber] = designMatrix[0,-1]

    #Check if full coverage has been achieved
    if bestFitness[loopNumber] == 1: 
        globaldesignMatrix.append(designMatrix[0,:])
        break
            
    #Check if the algorithm has converged on a solution
    if ((loopNumber > convergenceCheck) and \
    ((bestFitness[loopNumber] == bestFitness[loopNumber-convergenceCheck]) or \
    (bestFitness[loopNumber] >= theoreticalBest))) or \
    loopNumber == maxLoops-1:
        
        #store the best design for this N
        globaldesignMatrix.append(designMatrix[0,:])
        
        #Reset counters, the design matrix, and the scoring vector.
        numberSensors += 1
        if numberSensors == Nmax+1: # +1 is because N is iterated at the end of the loop
            print('The max number of sensors has been reached')
            break
        print('Solving for ' + str(numberSensors) + ' sensors')
        theoreticalBest = (numberSensors*np.pi*(coverageRadius**2))/len(fieldPixels[:,0])
        loopNumber = 0
        bestFitness = np.zeros((maxLoops,1))    

    #If convergence has NOT occured, then loop through
    else:        
        
        #Mate Designs
        
        
        #Mutate Designs
        designMatrix = mutate_randomReset(designMatrix,geneticVariables,bounds)
        
        #Loop
        loopNumber += 1
