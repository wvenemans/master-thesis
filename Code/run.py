import os
import time
import string
import numpy as np
import xml.etree.ElementTree as ET

import tqdm





def main():


    """
    Choose the amount of iterations and the model you want to run
    
    """
    iterations = 20
    models = np.array(["Erreramodel", "Longestaxis", "Randomaxis"])
    #models = np.array(["Waterflux"])


    #for model in models:
        #behaviour(model, iterations)
        #runSimulation(iterations, model)

    #behaviour("Erreramodel", 1)
    #runSimulation(1, "Waterflux")
    #bumpcells(1)

    #paramSweep("Waterflux", 1)






"""
def runSimulation
Arguments:
- iterations (int) : amount of iterations per simulation
- model (string) : model to be simulatede
Returns:
- nothing

Simulates a certain model for some iterations. Makes individual datadirectories and xml files.
"""
def runSimulation(iterations : int, model : string) -> None:
    
    #change the model name to the correct format
    newModelName = 'lib' + model + '.so'   

    print("Running simulation for model: " + newModelName)

    start = time.time()

    for i in tqdm.tqdm(range(iterations)):

        #start a clock
        start = time.time()
        
        #visually show the progress
        print("Model " + model + " in iteration " + str(i) + " of " + str(iterations))



        #createn a new name for the model with the correct iteration number
        iterName = model + str(i)


        #copy the start.xml file to a new file with the correct iteration number
        newFileName = "start" + iterName + ".xml"
        os.system("cp start.xml " + newFileName)


        #parse the xml file
        tree = ET.parse(newFileName)
        root = tree.getroot()


        #change the datadirectory
        os.system("mkdir " + iterName)
        datadir = root.find("./parameter/par[@name='datadir']")
        datadir.set('val', str(os.getcwd()) + "/" + iterName)

        #we want to loop over i1 and i2



        #create a new name for the model with the correct iteration number
        newIterName = model + str(i)

        #create a new folder to store the data
        os.system("mkdir " + newIterName)
        datadir = root.find("./parameter/par[@name='datadir']")
        datadir.set('val', str(os.getcwd()) + "/" + newIterName)

                    #copy the start.xml file to a new file with the correct iteration number
        newFileName = newIterName + "/start" + newIterName + ".xml"
        os.system("cp startWaterflux.xml " + newFileName)

        #write the new xml file
        tree.write(newFileName)

        #start the simulation
        #cmd = " '/home/willem/Documents/VirtualLeaf2021-2.0.0/bin/VirtualLeaf'  -b -l "+newFileName+" -m " +newModelName
        cmd = " '/home/willem/Documents/VirtualLeaf2021-2.0.0 - WaterFlux/bin/VirtualLeaf'  -b -l "+newFileName+" -m " + newModelName
        os.system(cmd)
        
    #print the time taken to run the simulation
    print("Time taken to run the complete iterations: " + str((time.time() - start)))





"""
def behaviour
Arguments:
- model (string) : model to be simulated
- iterations (int) : amount of iterations per simulation
Returns:
- nothing

Simulates a model and looks at 9 different behaviours, as in section 3.2.1. Makes individual datadirectories and xml files.
"""

def behaviour(model : string, iterations: int) -> None:
    
    # 0, 1, 2, 3, 4, 5, 6, 7, 8 - Paper order: 2, 5, 8, 1, 4, 7, 0, 3, 6 
    paramsets = np.array([ [1,9,81], [1,1,9], [9,1,9], [1/9,1,1], [1,1,1], [9,1,1], [1,9,1], [1,1,1/9], [9,1,1/9] ])
    #start a clock
    start = time.time()

    newModelName = 'lib' + model + '.so'   


    for j in tqdm.tqdm(range(iterations), desc="Running simulations for model " + model):

        for i in range(len(paramsets)):

            #create a new name for the model with the correct iteration number
            iterName = model + str(i) + str(j) 

            #copy the start.xml file to a new file with the correct iteration number
            newFileName = "start" + iterName + ".xml"
            os.system("cp startWaterflux.xml " + newFileName)

            #parse the xml file
            tree = ET.parse(newFileName)
            root = tree.getroot()

            #change the datadirectory
            os.system("mkdir " + iterName)
            datadir = root.find("./parameter/par[@name='datadir']")
            datadir.set('val', str(os.getcwd()) + "/" + iterName)

            #set the new values 
            kt = root.find("./parameter/par[@name='kt']")
            kc = root.find("./parameter/par[@name='kc']")
            lambdalength = root.find("./parameter/par[@name='lambda_length']")

            kt.set('val', str(paramsets[i][0]))
            kc.set('val', str(paramsets[i][1]))
            lambdalength.set('val', str(paramsets[i][2]))

            #write the new xml file
            tree.write(newFileName)

            #start the simulation
            cmd = " '//home/willem/Documents/VirtualLeaf2021-2.0.0 - WaterFlux (Copy)/bin/VirtualLeaf'  -b -l "+newFileName+" -m " + newModelName
            os.system(cmd)


    #print the time taken to run the simulation
    print("Time taken to run the simulation: " + str((time.time() - start)))



"""
def bumpcells
Arguments:
- iterations (int) : amount of iterations per simulation
Returns:
- nothing

Simulates the bumpcells behaviour for the given iterations, as in Section 3.2.2.


"""


def bumpcells(iteratons: int) -> None:



    # REF, ALPHA+, CC-
    # OM
    #paramsets = [[1,9,81],[1,1,1/9],[1/9,1,1]]
    paramsets =[[1,9,81]]

    model = "Waterflux"

    for i in range(len(paramsets)):

        #create a new name for the model with the correct iteration number
        iterName = model + str(i)

        #copy the start.xml file to a new file with the correct iteration number
        newFileName = "start" + iterName + ".xml"
        os.system("cp Waterflux_bigg.xml " + newFileName)

        #parse the xml file
        tree = ET.parse(newFileName)
        root = tree.getroot()

        #change the datadirectory
        os.system("mkdir " + iterName)
        datadir = root.find("./parameter/par[@name='datadir']")
        datadir.set('val', str(os.getcwd()) + "/" + iterName)

        #set the new values
        kt = root.find("./parameter/par[@name='kt']")
        kc = root.find("./parameter/par[@name='kc']")
        lambdalength = root.find("./parameter/par[@name='lambda_length']")

        kt.set('val', str(paramsets[i][0]))
        kc.set('val', str(paramsets[i][1]))
        lambdalength.set('val', str(paramsets[i][2]))

        #write the new xml file
        tree.write(newFileName)

        #start the simulation
        cmd = " '/home/willem/Documents/VirtualLeaf2021-2.0.0 - WaterFlux/bin/VirtualLeaf'  -b -l "+newFileName+" -m libWaterflux.so"
        os.system(cmd)



"""
paramSweep
Arguments:
- model (string) : The model to be simulated.
- iterations (int) : The number of iterations for the simulation.
Returns:
- None

Runs the parametersweep to explore the phaseplane of the behaviour model.
"""

def paramSweep(model : string, iterations: int) -> None:
    """
    Runs a parameter sweep for the given model and iterations.
    
    Arguments:
    - model (string): The model to be simulated.
    - iterations (int): The number of iterations for the simulation.
    
    Returns:
    - None
    """
    
    for i in tqdm.tqdm(range(iterations), desc="Running parameter sweep for model " + model):

        #100x100 = 1e4 iterations
        start = time.time()
         
        for alphaa in np.arange(0.1, 1.01, 0.1):
            for alphas in np.arange(0.1, 1.01, 0.1):

                a = 1

                w = ((1 -alphaa) / alphaa)
                s = ((alphas) / (1-alphas))

                alphaa = round(alphaa, 2)
                alphas = round(alphas, 2)

                print("SWEEP " + str(alphaa) + " " + str(alphas))
                print("Waterflux parameters: " + str(a) + " " + str(s) + " " + str(w))

                #create a new name for the model with the correct iteration number
                iterName = model + str(i) + str(alphaa) + str(alphas)

                #copy the start.xml file to a new file with the correct iteration number
                newFileName = "start" + iterName + ".xml"
                os.system("cp startWaterflux.xml " + newFileName)

                #parse the xml file
                tree = ET.parse(newFileName)
                root = tree.getroot()

                #change the datadirectory
                os.system("mkdir " + iterName)
                datadir = root.find("./parameter/par[@name='datadir']")
                datadir.set('val', str(os.getcwd()) + "/" + iterName)

                #set the new values
                kt = root.find("./parameter/par[@name='kt']")
                kc = root.find("./parameter/par[@name='kc']")
                lambdalength = root.find("./parameter/par[@name='lambda_length']")

                kt.set('val', str(s))
                kc.set('val', str(a))
                lambdalength.set('val', str(w))

                #write the new xml file
                tree.write(newFileName)

                #start the simulation
                cmd = " '/home/willem/Documents/VirtualLeaf2021-2.0.0 - WaterFlux/bin/VirtualLeaf'  -b -l "+newFileName+" -m libWaterflux.so"
                os.system(cmd)


    #print the time taken to run the simulation
    print("Time taken to run the simulation: " + str((time.time() - start)))

