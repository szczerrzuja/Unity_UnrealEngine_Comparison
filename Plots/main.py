import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#cpu and gpu time is in ms not in %

folders = ["pc1","pc2","pc3", "pc4", "pc5", "pc6", "pc7"]

unityFileName = "LoggedData.csv"
unreaFileName = "statisticsCollected.csv"
columnsForAllData = ['PCIndex','AvarageFPX', 'STAD_DEV FPS','Worst 1 fps', 'Worst 0.1 fps', 'MinCPU', 'MaxCPU', 'Avaragecpu',  'MinGPU', 'MaxGPU', 'AvarageGpu', 'MaxRAM', 'AVG RAM', 'MinRAM', 'Min VRAM', 'Avg VRAM', 'Max VRAM', 'STAD_DEV']
dataFrameForAllDataUNREAL = pd.DataFrame(columns=columnsForAllData)
dataFrameForAllDataUNITY = pd.DataFrame(columns=columnsForAllData)

def unrealRepairTimestamp(column):
    valueToAdd = 0
    savedLastValue = 0.0
    frame = pd.DataFrame(columns=['lp','TimeStamp'])
    
    for index, value in column.items():
        if value < savedLastValue:
            valueToAdd += 430
        savedLastValue = value
        frame.loc[len(frame.index)] = [index, value+valueToAdd] 
    return frame

def loadDataFromFileUNREAL(filePath):
    loadedData = pd.read_csv(filePath, sep=";", decimal='.', header=0, dtype={'lp':int, 'TimeStamp':float, 'CPU FrameTime':float, 'RAMUsage':float, 'GPU Frame Time':float, 'VRAMUsage':float, 'FPS':float})
    savedColumn=unrealRepairTimestamp(loadedData['TimeStamp']);
    loadedData['TimeStamp'] = savedColumn['TimeStamp'] 
    return loadedData


def loadDataFromFileUNITY(filePath):
    df = pd.read_csv(filePath, sep=";", decimal=',', header=0, dtype={'lp':int, 'TimeStamp':float, 'CPU FrameTime':float, 'RAMUsage':float, 'GPU Frame Time':float, 'VRAMUsage':float, 'FPS':float})
    df.drop(index=range(4))
    return df

def createEnginePlots(DataSets, UnrealOrUnity, searchedDataName, serachedDataInDataFrameName):
    
    plt.figure()
    for data in DataSets:
        plt.plot(data['TimeStamp'], data[serachedDataInDataFrameName])
    plt.xlim(0, None)  
    plt.ylim(0, None)  
    plt.xlabel('Czas w sekundach')
    plt.ylabel('Klatki na sekundę')
    plt.title('Wykres zależności klatek na sekundę od czasu w silniku ' +UnrealOrUnity)
    plt.legend(folders)
    plt.grid(True)
    plt.savefig(UnrealOrUnity+searchedDataName+'.png')

def createPairPlot(UnitySet, UnrealSet, pcName, serachedDataInDataFrameName, searchedDataName):
    
    plt.figure()
    
    plt.plot(UnitySet['TimeStamp'], UnitySet[serachedDataInDataFrameName])
    plt.plot(UnrealSet['TimeStamp'], UnrealSet[serachedDataInDataFrameName])
    plt.xlim(0, 3000.0)  
    plt.ylim(0, None)  
    plt.xlabel('Czas w sekundach')
    plt.ylabel('Klatki na sekundę')
    plt.title('Wykres zależności klatek na sekundę od czasu w silnikach na ' +pcName)
    plt.legend(['Unity', 'UnrealEngine'])
    plt.grid(True)
    plt.savefig(pcName+'searchedDataName'+'.png')

def getStatisticsFromDataSet(dataframe):
    listedstats = []
    listedstats.append("{:.2f}".format(dataframe['FPS'].min()))
    listedstats.append("{:.2f}".format(dataframe['FPS'].max()))
    listedstats.append("{:.2f}".format(dataframe['FPS'].mean()))
    listedstats.append("{:.2f}".format(dataframe['FPS'].std()))
    listedstats.append("{:.2f}".format(dataframe['FPS'].quantile(0.01)))
    listedstats.append("{:.2f}".format(dataframe['FPS'].quantile(0.001)))
    
    listedstats.append("{:.2f}".format(dataframe['CPU FrameTime'].min()))
    listedstats.append("{:.2f}".format(dataframe['CPU FrameTime'].max()))
    listedstats.append("{:.2f}".format(dataframe['CPU FrameTime'].mean()))
    
    listedstats.append("{:.2f}".format(dataframe['RAMUsage'].min()))
    listedstats.append("{:.2f}".format(dataframe['RAMUsage'].max()))
    listedstats.append("{:.2f}".format(dataframe['RAMUsage'].mean()))
    
    listedstats.append("{:.2f}".format(dataframe['GPU Frame Time'].min()))
    listedstats.append("{:.2f}".format(dataframe['GPU Frame Time'].max()))
    listedstats.append("{:.2f}".format(dataframe['GPU Frame Time'].mean()))
   
    listedstats.append("{:.2f}".format(dataframe['VRAMUsage'].min()))
    listedstats.append("{:.2f}".format(dataframe['VRAMUsage'].max()))
    listedstats.append("{:.2f}".format(dataframe['VRAMUsage'].mean()))
    
    return listedstats
    
def saveStats(dataToSave, filename):
    with open(filename + 'Table.txt', 'w') as file:
        file.write(' & '.join(['LP', 'Min FPS', 'Max FPS', 'Avg FPS', 'Std FPS','Worst 1%', 'Worst 0.1%', 'Min CPU FrameTime', 'Max CPU FrameTime', 'Avg CPU FrameTime', 'Min RAMUsage', 'Max RAMUsage', 'Avg RAMUsage', 'Min GPU Frame Time', 'Max GPU Frame Time', 'Avg GPU Frame Time', 'Min VRAMUsage', 'Max VRAMUsage', 'Avg VRAMUsage'])+ ' \\\\\n')
        iterator = 1
        for i in dataToSave:
            file.write(str(iterator) + ' & '+' & '.join(i) + ' \\\\\n')
            iterator +=1
            
unrealDataFrames = []
unityDataFrames = []
resourcesStatsUNITY = []
resourcesStatsUnreal = []
iterator = 0
for i in folders:
    unrealDataFrames.append(loadDataFromFileUNREAL(i+"\\"+unreaFileName))
    unityDataFrames.append(loadDataFromFileUNITY(i+"\\"+unityFileName))
    createPairPlot(unityDataFrames[iterator], unrealDataFrames[iterator],i, 'FPS', 'Liczba klatek na sekundę')
    resourcesStatsUNITY.append(getStatisticsFromDataSet(unityDataFrames[iterator]))
    resourcesStatsUnreal.append(getStatisticsFromDataSet(unrealDataFrames[iterator]))  
    iterator+=1
    print(i)

#createPlots(unrealDataFrames, 'Unreal Engine', 'liczby klatek na sekundę', 'FPS')
createEnginePlots(unityDataFrames, 'Unity', 'liczba klatek na sekundę', 'FPS')
createEnginePlots(unrealDataFrames, 'Unrea Engine', 'Liczba klatek na sekundę', 'FPS')

#print(resourcesStatsUNITY)
#saveStats(resourcesStatsUNITY, 'Unity')
#saveStats(resourcesStatsUnreal, 'Unreal')