'''
Function Definitions
'''

def plotDesigns(A,designs,fitness,radius):#(fieldPixels,globaldesignMatrix,globalFitness,coverageRadius)
    
    '''
    Plots the coordinates of where to place sensors as
    over the field pixels for each number of sensors
    '''
    
    numberDesigns = len(designs)
    
    #Build Subplot Architecture
    plt.style.use('seaborn')    
    fig, axs = plt.subplots(numberDesigns,2,figsize=(10, 5*numberSensors))
    cols = ['Optimized Sensor Positions','Development of Objective Function']
    for ax, col in zip(axs[0], cols):
        ax.set_title(col)
        
    #Fill in the Subplots
    for n in range(numberDesigns):
        
        #Plot Sensor Positions with Coverage
        thisDesign = designs[n]
        x = thisDesign[0:-2:2]
        y = thisDesign[1:-1:2]
        axs[n,0].scatter(A[:,0], A[:,1], marker = 's')
        axs[n,0].scatter(x, y, color = '#ff7f0e', label='N = {} Sensors'.format(n+1))
        axs[n,0].legend()
        circles = []
        for i in range(len(x)):
            newCircle = plt.Circle((x[i],y[i]), radius, fill=False)
            axs[n,0].add_artist(newCircle)
        plt.setp(axs[n,0],xlabel = 'x (m)')
        plt.setp(axs[n,0],ylabel = 'y (m)')
        
        #Plot Convergence
        thisFitness = fitness[:,n]*100
        y = np.ma.masked_equal(thisFitness,0).compressed()
        x = np.linspace(1,len(y),len(y))
        axs[n,1].plot(x,y,label = 'N = {} Sensors'.format(n+1))
        axs[n,1].set_xlim([0, len(thisFitness)])
        axs[n,1].set_ylim([0, 100])
        plt.setp(axs[n,1],xlabel = 'Iterations (#)')
        plt.setp(axs[n,1],ylabel = 'Coverage (%)')

def plotthisDesign(A,designs,radius,N):#(fieldPixels,globaldesignMatrix,coverageRadius,designNumber)
        
    '''
    Plots the coordinates of where to place sensors 
    over the field pixels for the N sensor design
    '''
    
    #Build Subplot Architecture
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(5, 5))
    
    #Fill in the Subplots
    thisDesign = globaldesignMatrix[N-1]
    x = thisDesign[0:-2:2]
    y = thisDesign[1:-1:2]
    plt.scatter(A[:,0], A[:,1], marker = 's', label='Field Pixels')
    for i in range(len(x)):
        newCircle = plt.Circle((x[i],y[i]), radius, fill=False)
        ax.add_artist(newCircle)
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    
def graphCoverage(N_0,designs):#(N_0,globaldesignMatrix)
    
    '''
    Make a scatter plot that shows the percent field coverage achievable by varying the number of sensors used
    '''
    
    #Build Subplot Architecture
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize = [10,5])
    
    #Fill in the Subplots
    numberDesigns = len(designs)
    minSensors = N_0
    maxSensors = N_0 + numberDesigns - 1
    coverage = []
    for n in range(numberDesigns):
        thisDesign = designs[n]
        coverage.append(thisDesign[-1]*100)
    numberSensors = np.linspace(minSensors,maxSensors,num=numberDesigns).astype('int')  #assumes increasing numberSensors += 1
    plt.plot(numberSensors,coverage, 'o')
    fig.suptitle('Field Coverage vs. Number of Sensors', size = 'xx-large')
    plt.xlabel('Number of Sensors in the Design (#)', color='#1C2833')
    plt.ylabel('Coverage (%)', color='#1C2833')
    ax.set_xlim([minSensors, maxSensors])
    ax.set_ylim([0, 100])
    plt.show()
    

    
'''
Plotting & Reporting
'''
graphCoverage(N_0,globaldesignMatrix)
plotDesigns(fieldPixels,globaldesignMatrix,globalFitness,coverageRadius)
# plotthisDesign(fieldPixels,globaldesignMatrix,coverageRadius,3)
