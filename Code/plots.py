import numpy as np
import matplotlib.pyplot as plt
import glob     

import scipy.stats as stats

from sklearn.cluster import KMeans

from collections import defaultdict


import xml.etree.ElementTree as ET
import cv2
import os



def main():
    """
    Choose the appropriate plotting function to visualize the data.
    """


    ###Plots

    createVideo()
    #plotPressurePos()
    #plotLL()
    #plotNN()
    #plotNNSingleTimeStep()
    #plotNeigbourPressureAndNumber()
    #plotDifference()
    #plotDifferenceArea()
    #plotNNSingleTimeStep()
    #plotNormalizedPressure()
    #plotNormalizedPressurevsnormalizedArea()
    #plotNormalizedAreavsNeighbours()


    ###Tables
    #ttesttable()
    #twocelltable()


"""
def createVideo()
Arguments:
- none
Returns:
- nothing
Function to create a video of the area growth of the cells
"""

def createVideo() -> None:

    images = []

    for file in sorted(glob.glob("//home/willem/Documents/Thesis/Results3x3/Waterflux20/*.png")):
        img = cv2.imread(file)
        images.append(img)

    height, width, layers = images[0].shape
    video = cv2.VideoWriter('Waterflux_Unbalanced.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (width, height))

    for image in images:
        video.write(image)

    video.release()
    cv2.destroyAllWindows()



"""
def plotNormalizedAreavsNeighbours()
Arguments:
- none
Returns:
- nothing
Plots the normalized area of the cells against the number of neighbours
"""



def plotNormalizedAreavsNeighbours() -> None:


    totalArea = np.array([])
    totalNeigbours = np.array([])

    for file in sorted(glob.glob("/home/willem/Documents/Thesis/Simple Simulations/Random*/*3800.xml")):

        tree = ET.parse(file)
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")

        area = np.array([])
        neigbours = np.array([])

        for cell in cells:
            try:
                neigbours = np.append(neigbours, float(cell.get('neighbour_number')))
                area = np.append(area, float(cell.get('area')))
            except (ValueError, TypeError):
                print(f"Skipping cell in file {file} due to missing or invalid data.")
                break

        averageArea = np.mean(area)
        stdArea = np.std(area)

        normalizedArea = (area - averageArea) / stdArea

        totalArea = np.append(totalArea, normalizedArea)
        totalNeigbours = np.append(totalNeigbours, neigbours)   
    

    #remove the cells which aren't in the range 4 and 9

    mask = (totalNeigbours >= 4) & (totalNeigbours <= 9)
    pearsonr, pearsonp = stats.pearsonr(totalNeigbours[mask], totalArea[mask])

    print(totalArea[mask].size)

    print(f"Pearson correlation coefficient: {pearsonr}, p-value: {pearsonp}, r-squared: {pearsonr**2}")

    #create boxplot
    aggregateArea = defaultdict(list)       

    for label, value in zip(totalNeigbours, totalArea):
        aggregateArea[label].append(value)

    sortedKeys = sorted(aggregateArea.keys())
    areaPerNeighbour = [aggregateArea[key] for key in sortedKeys]

    areaPerNeighbour = areaPerNeighbour[4:9]


    
    fig, ax = plt.subplots()
    ax.boxplot(areaPerNeighbour, patch_artist=True)
    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0.3))


    ax.xaxis.set_ticklabels(['4', '5', '6', '7', '8'])

    ax.set(xlabel='Number of Neighbours', ylabel='Normalized Area',
        title='Normalized Area of Randomaxis cells against the number of neighbours')
    plt.show()

        



"""
def plotNormalizedPressurevsnormalizedArea()
Arguments:
- none
Returns:
- nothing
Plots the normalized pressure of the cells against the normalized area
"""


def plotNormalizedPressurevsnormalizedArea() -> None:


    totalArea = np.array([])
    totalPressure = np.array([])


    for file in sorted(glob.glob("/home/willem/Documents/Thesis/Simple Simulations/Random*/*4000.xml")):

        print(file)

        tree = ET.parse(file)
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")

        pressure = np.array([])
        neigbours = np.array([])
        area = np.array([])

        for cell in cells:
                try:
                    pressure = np.append(pressure, float(cell.get('pressure')))
                    area = np.append(area, float(cell.get('area')))
                except (ValueError, TypeError):
                    print(f"Skipping cell in file {file} due to missing or invalid data.")
                    continue

        averagePressure = np.mean(pressure)
        stdPressure = np.std(pressure)
        
        normalizedPressure = (pressure - averagePressure) / stdPressure

        averageArea = np.mean(area)
        stdArea = np.std(area)

        normalizedArea = (area - averageArea) / stdArea

        totalArea = np.append(totalArea, normalizedArea)
        totalPressure = np.append(totalPressure, normalizedPressure)



    pearsonr, pearsonp = stats.pearsonr(totalArea, totalPressure)
    spearmanr, spearmanp = stats.spearmanr(totalArea, totalPressure)

    print(f"Pearson correlation coefficient: {pearsonr}, p-value: {pearsonp}, r-squared: {pearsonr**2}")
    print(f"Spearman correlation coefficient: {spearmanr}, p-value: {spearmanp}")


    data = np.column_stack((totalArea, totalPressure))

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(data)
    labels = kmeans.labels_



    # seperate the data into clusters
    cluster_0 = data[labels == 0]
    cluster_1 = data[labels == 1]

    pearsonr0, pearsonp0 = stats.pearsonr(cluster_0[:, 0], cluster_0[:, 1])
    pearsonr1, pearsonp1 = stats.pearsonr(cluster_1[:, 0], cluster_1[:, 1])

    print(f"Cluster 0 - Pearson correlation coefficient: {pearsonr0}, p-value: {pearsonp0}, r-squared: {pearsonr0**2}")
    print(f"Cluster 1 - Pearson correlation coefficient: {pearsonr1}, p-value: {pearsonp1}, r-squared: {pearsonr1**2}")

    fig, ax = plt.subplots()
    scatter = ax.scatter(totalArea, totalPressure, c=labels)
    ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.set(xlabel='Normalized Area', ylabel='Normalized Pressure',
        title='Normalized Pressure vs Normalized Area of the Errera model')

    plt.show()




"""
def plotNormalizedPressure()
Arguments:
- none
Returns:
- nothing
Plots the normalized pressure of the cells against the number of neighbours
"""

def plotNormalizedPressure() -> None:



    totalPressure = np.array([])
    totalNeigbours = np.array([])

    for file in sorted(glob.glob("/home/willem/Documents/Thesis/WATERFLUXRESULTS/results_v2/resultsv2/Errera*/*12000.xml")):

        tree = ET.parse(file)
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")

        pressure = np.array([])
        neigbours = np.array([])

        for cell in cells:
                try:
                    pressure = np.append(pressure, float(cell.get('pressure')))
                    neigbours = np.append(neigbours, float(cell.get('neighbour_number')))
                except (ValueError, TypeError):
                    print(f"Skipping cell in file {file} due to missing or invalid data.")
                    continue

        averagePressure = np.mean(pressure)
        stdPressure = np.std(pressure)
        
        normalizedPressure = (pressure - averagePressure) / stdPressure



        totalPressure = np.append(totalPressure, normalizedPressure)
        totalNeigbours = np.append(totalNeigbours, neigbours)   


    





    #create boxplot
    aggregatePressure = defaultdict(list)

    for label, value in zip(totalNeigbours, totalPressure):
        aggregatePressure[label].append(value)

    sortedKeys = sorted(aggregatePressure.keys())
    pressurePerNeighbour = [aggregatePressure[key] for key in sortedKeys]

    pressurePerNeighbour = pressurePerNeighbour[4:9]

    

    mask = (totalNeigbours >= 4) & (totalNeigbours <= 9)
    pearsonr, pearsonp = stats.pearsonr(totalNeigbours[mask], totalPressure[mask])

    print(f"Pearson correlation coefficient: {pearsonr}, p-value: {pearsonp}, r-squared: {pearsonr**2}")

    fig, ax = plt.subplots()
    ax.boxplot(pressurePerNeighbour, patch_artist=True)

    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, 0.3))

    ax.xaxis.set_ticklabels(['4', '5', '6', '7', '8'])


    ax.set(xlabel='Number of Neighbours', ylabel='Normalized Pressure',
        title='Normalized Pressure of random axis against the number of neighbours')

    plt.show()


"""
def plotNeighbourPressure()
Arguments:
- none
Returns:
- nothing
Plots the pressure of the cells against the number of neighbours

"""

def plotNeigbourPressureAndNumber()-> None:



    pressure = np.array([])
    neighbours = np.array([])
    secondorderneighbourPressure = np.array([])


    for file in sorted(glob.glob("Erreramodel0/*3400.xml")):

        tree = ET.parse(file)
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")

        for cell in cells:
                
                pressure = np.append(pressure, float(cell.get('pressure')))
                neighbours = np.append(neighbours, float(cell.get('neighbour_number')))
                secondorderneighbourPressure = np.append(secondorderneighbourPressure, float(cell.get('nofn_average_pressure')))

    

        fig, ax = plt.subplots()
        print(pressure)
        #ax.scatter(neighbours, pressure)
        #ax.scatter(neighbours, secondorderneighbourPressure, color = 'blue')
        ax.scatter(neighbours, pressure, color = 'red')
        ax.set_xticks(np.arange(0, 15, 1))
        ax.set(xlabel='Number of neighbours', ylabel='Pressure',
            title='Pressure over number of neighbours of Erreramodel at timestep 3400')
    
        plt.show()


"""
def plotPressurePos
Arguments:
- none
Returns:
- nothing

Plots the position and the pressure of the cells based on their centroids
"""

def plotPressurePos() -> None:

    for file in sorted(glob.glob("/home/willem/Documents/Thesis/Simple Simulations/Randomaxis*/*3800.xml")):

        

        tree = ET.parse(file)
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")



        cellX = np.array([])
        cellY = np.array([])
        pressure = np.array([])

        for cell in cells:

            pressure = np.append(pressure, float(cell.get('pressure')))
            cellX = np.append(cellX, float(cell.get('centroid_x')))
            cellY = np.append(cellY, float(cell.get('centroid_y')))

        averagePressure = np.mean(pressure)
        stdPressure = np.std(pressure)
        print(stdPressure)

        differenceInPressure = (pressure - averagePressure) / stdPressure
        
        fig, ax = plt.subplots()
        ax.scatter(cellX, cellY, c = differenceInPressure, cmap = 'coolwarm')
    
        ax.set_ylim(-300, 300)
        ax.set_xlim(-300, 300)
        cbar = plt.colorbar(ax.scatter(cellX, cellY, c = differenceInPressure, cmap = 'coolwarm'))

        file = file[18:-4]
        ax.set(xlabel='x', ylabel='y',
            title='Pressure distribution of random axis model at timestep 3800')

        plt.show()
        #strip the file extension
        #file = file[16:]
        #plt.savefig("Figures/PressurePos of Longestaxis at timestep" + str(file) + ".png")



"""
def generateAreaGrowth
Arguments:
- none
Returns:
- nothing

Builds a 3x3 grid of plots showing the area growth of cells 0 and 1 for different waterflux simulations.

"""

def generateAreaGrowth():

    #make a 3x3 grid of plots, each plot showing the area growth of cell 0 and cell 1 for each waterflux simulation
    plt.figure(figsize=(15, 10))

    s = ["alpha^s = 0.1", "alpha^s = 0.5", "alpha^s = 0.9"]
    a = ["alpha^a = 0.1", "alpha^a = 0.5", "alpha^a = 0.9"]
    plt.suptitle("Area Growth of Cells 0 and 1 for Different Waterflux Simulations", fontsize=16)
    plt.subplots_adjust(top=0.9, hspace=0.3, wspace=0.3)
    
    count = 0
    for i in [2, 5, 8, 1, 4, 7, 0, 3, 6]:  # Paper order: 2, 5, 8, 1, 4, 7, 0, 3, 6

        area_cell_0= np.array([])
        area_cell_1 = np.array([])
        xaxis = np.array([])

        folderName = "Results3x3/Waterflux" + str(i)+ "0"

        for folder in glob.glob(folderName):
            print("Processing folder:", folder)

            xml_files = glob.glob(os.path.join(folder, "*.xml"))
            xml_files.sort()  # Sort files to ensure consistent order
            if not xml_files:
                print(f"No XML files found in folder {folder}. Skipping...")
                continue

            for xml_file in xml_files:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                cells = root.findall("./cells/cell[@area]")

                area_cell_0 = np.append(area_cell_0, float(cells[0].get("area")))
                area_cell_1 = np.append(area_cell_1, float(cells[1].get("area")))

                xaxis = np.append(xaxis, int(xml_file.split('.')[-2].split('leaf.')[-1]))

        # 0, 1, 2, 3, 4, 5, 6, 7, 8 - Paper order: 2, 5, 8, 1, 4, 7, 0, 3, 6 


        plt.subplot(3, 3, count + 1)
        plt.plot(xaxis, area_cell_0, label="Cell 0", color="blue")
        plt.plot(xaxis, area_cell_1, label="Cell 1", color="orange")
        plt.title(f"{s[i % 3]}, {a[i // 3]}")
        plt.xlabel("Time Step")
        plt.ylabel("Area")
        plt.legend()

        count += 1

    plt.tight_layout()
    plt.show()




"""
def ttesttable
Arguments:
- none
Returns:
- nothing

Generates the tables for the average number of neighbours, pressure and area.

"""



def ttesttable():

    numberofneighbours_e =  np.array([])
    area_e = np.array([])
    pressure_e = np.array([])

    for folder in glob.glob("/home/willem/Documents/Thesis/WATERFLUXRESULTS/results_v2/resultsv2/Errera*"):
        print("Processing folder:", folder)
        finalState = "leaf.004000.xml"

        if not os.path.exists(os.path.join(folder, finalState)):
            print(f"File {finalState} not found in folder {folder}. Skipping...")
            continue

        tree = ET.parse(os.path.join(folder, finalState))
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")
        try:
            for cell in cells:
                area_e = np.append(area_e, float(cell.get("area")))
                pressure_e = np.append(pressure_e, float(cell.get("pressure")))
                numberofneighbours_e = np.append(numberofneighbours_e, float(cell.get("neighbour_number")))

        except Exception as e:
            print(f"Error processing folder {folder}: {e}")
            continue



    numberofneighbours_r = np.array([])
    area_r = np.array([])
    pressure_r = np.array([])

    for folder in glob.glob("/home/willem/Documents/Thesis/WATERFLUXRESULTS/results_v2/resultsv2/Randomaxis*"):
        print("Processing folder:", folder)
        finalState = "leaf.004000.xml"

        if not os.path.exists(os.path.join(folder, finalState)):
            print(f"File {finalState} not found in folder {folder}. Skipping...")
            continue

        tree = ET.parse(os.path.join(folder, finalState))
        root = tree.getroot()

        cells = root.findall("./cells/cell[@area]")
        try:
            for cell in cells:
                area_r = np.append(area_r, float(cell.get("area")))
                pressure_r = np.append(pressure_r, float(cell.get("pressure")))
                numberofneighbours_r = np.append(numberofneighbours_r, float(cell.get("neighbour_number")))

        except Exception as e:
            print(f"Error processing folder {folder}: {e}")
            continue



    t_stat, p_value = stats.ttest_ind(area_e, area_r)
    print("area errera: ", area_e.mean(), "area random: ", area_r.mean())
    print(f"t-statistic area: {t_stat}, p-value: {p_value}")

    t_stat, p_value = stats.ttest_ind(pressure_e, pressure_r)
    print("pressure errera: ", pressure_e.mean(), "pressure random: ", pressure_r.mean())
    print(f"t-statistic pressure: {t_stat}, p-value: {p_value}")

    t_stat, p_value = stats.ttest_ind(numberofneighbours_e, numberofneighbours_r)
    print("number of neighbours errera: ", numberofneighbours_e.mean(), "number of neighbours random: ", numberofneighbours_r.mean())
    print(f"t-statistic neighbours: {t_stat}, p-value: {p_value}")



"""
def twocelltable
Arguments:
- none
Returns:
- nothing

Generates a table with the average area, circumference and pressure of the two cells model

"""

def twocelltable():


    totalData = pd.DataFrame(columns=["Area_Average", "Area_std", "Circumference_average", "Circumference_std", "Pressure_Average", "Pressure_std"])

    for i in range(0,9):

        area_cell_0= np.array([])
        area_cell_1 = np.array([])
        circumference_cell_0 = np.array([])
        circumference_cell_1 = np.array([])
        pressure_cell_0 = np.array([])
        pressure_cell_1 = np.array([])



        folderName = "Waterflux" + str(i)+ "*"

        for folder in glob.glob(folderName):
            print("Processing folder:", folder)
            finalState = "leaf.01000.xml"

            tree = ET.parse(os.path.join(folder, finalState))
            root = tree.getroot()

            cells = root.findall("./cells/cell[@area]")



            area_cell_0 = np.append(area_cell_0, float(cells[0].get("area")))
            area_cell_1 = np.append(area_cell_1, float(cells[1].get("area")))
            pressure_cell_0 = np.append(pressure_cell_0, float(cells[0].get("pressure")))
            pressure_cell_1 = np.append(pressure_cell_1, float(cells[1].get("pressure")))
            circum_cell_0 = 0
            circum_cell_1 = 0

            for wall in cells[0].findall("./node[@base_length]"):
                circum_cell_0 += float(wall.get("base_length"))
                
            for wall in cells[1].findall("./node[@base_length]"):
                circum_cell_1 += float(wall.get("base_length"))

            circumference_cell_0 = np.append(circumference_cell_0, circum_cell_0)
            circumference_cell_1 = np.append(circumference_cell_1, circum_cell_1)

        df = pd.DataFrame({
            "Area_Average": [np.mean(area_cell_0), np.mean(area_cell_1)],
            "Area_std": [np.std(area_cell_0), np.std(area_cell_1)],
            "Circumference_average": [np.mean(circumference_cell_0), np.mean(circumference_cell_1)],
            "Circumference_std": [np.std(circumference_cell_0), np.std(circumference_cell_1)],
            "Pressure_Average": [np.mean(pressure_cell_0), np.mean(pressure_cell_1)],
            "Pressure_std": [np.std(pressure_cell_0), np.std(pressure_cell_1)]
        }, index=["Cell 0", "Cell 1"]) 

        totalData = pd.concat([totalData, df], axis=0)
    totalData.index.name = "Cell Type"
    totalData.to_csv("tableOne.csv")




if __name__ == '__main__':
    main()