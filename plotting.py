def plotDesigns(A,designs):#(fieldPixels,globaldesignMatrix)
    
    '''
    Plots the coordinates of where to place sensors 
    over the field pixels for each number of sensors
    '''
    
    numberSensors = len(designs)
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(5, 5*numberSensors))
    for n in range(numberSensors):
        fig.add_subplot(numberSensors,1,n+1)
        thisDesign = globaldesignMatrix[n]
        x = thisDesign[0:-2:2]
        y = thisDesign[1:-1:2]
        plt.scatter(fieldPixels[:,0], fieldPixels[:,1], marker = 's', label='Field Pixels')
        plt.scatter(x, y, label='N = ' + str(n+1))
        plt.xlabel('x', color='#1C2833')
        plt.ylabel('y', color='#1C2833')

def plotAll(A,designs):#(fieldPixels,globaldesignMatrix)
    
    '''
    Plots the sensor locations as circles with an effective radius 
    over the field pixels for each number of sensors
    '''
    
    numberSensors = len(designs)
    colors = ('r','g','b','c','m','y','k','w')
    plt.style.use('seaborn')
    fig, ax = plt.subplots() 
    ax.scatter(A[:,0], A[:,1], marker = 's', label='Field Pixels')
    for n in range(numberSensors):     
        thisDesign = designs[n]
        x = thisDesign[0:-2:2]
        y = thisDesign[1:-1:2]
        circles = []
        for i in range(len(x)):
            newCircle = plt.Circle((x[i],y[i]), coverageRadius, color = colors[n], fill=False)
            ax.add_artist(newCircle)
    fig.suptitle('Agricultural Field represented by 1m\u00b2 pixels')
    ax.legend()
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
        
def printReport(N_0,designs):#(globaldesignMatrix)
    numberDesigns = len(designs)
    minSensors = N_0
    maxSensors = N_0 + numberDesigns - 1
    coverage = []
    for n in range(numberDesigns):
        thisDesign = designs[n]
        coverage.append(thisDesign[-1])
    numberSensors = np.linspace(minSensors,maxSensors,num=numberDesigns) #assumes increasing numberSensors += 1
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    plt.plot(numberSensors,coverage, 'o')
    fig.suptitle('Field Coverage vs. Number of Sensors')
    plt.xlabel('Number of Sensors in the Design (#)', color='#1C2833')
    plt.ylabel('Field Coverage (%)', color='#1C2833')
    ax.set_xlim([minSensors, maxSensors])
    ax.set_ylim([0, 1])
    plt.show()
    
#Plotting & Reporting
plotDesigns(fieldPixels,globaldesignMatrix)
plotAll(fieldPixels,globaldesignMatrix)
printReport(N_0,globaldesignMatrix)