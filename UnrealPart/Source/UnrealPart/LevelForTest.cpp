// Fill out your copyright notice in the Description page of Project Settings.

#include "LevelForTest.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"

#include "GenericPlatform/GenericPlatformMemory.h"
#include "Engine/Engine.h"

#include "Kismet/GameplayStatics.h"
#include "RHI.h"

//needed to process data from file
#include <iostream>
#include <sstream>
#include <string>
#include <fstream>

double LastFrameTime = FApp::GetCurrentTime();

ALevelForTest::ALevelForTest() : ALevelScriptActor()
{
    canUsageBeSaved = false;
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.bStartWithTickEnabled = true;
   
}

ALevelForTest::~ALevelForTest()
{
    outputFile.close();
}
void ALevelForTest::BeginPlay()
{
    Super::BeginPlay();
    FString filePath = FPaths::ProjectDir() + TEXT("points.csv");
    std::ifstream file(TCHAR_TO_UTF8(*filePath));
    std::string line;
    int lp, animIndex;
    float posX, posY, posZ, rotX, rotY, rotZ, rotW, scaleX, scaleY, scaleZ, animSpeed;
    std::getline(file, line); //read description
    int tmp = 1, counter = 0, numberOfIndexes = 23570,
        numberToSkipp =  std::floor(numberOfIndexes/maxNumberOfMannequins);
    // Read each line in the file
    while (std::getline(file, line) && maxNumberOfMannequins > counter)
    { 
        if (numberToSkipp - 1 < tmp)
        {
            tmp = 1;
            counter++;

            sscanf_s(line.c_str(), "%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%i,%f", &lp, &posX, &posY, &posZ, &rotX, &rotY, &rotZ, &rotW, &scaleX, &scaleY, &scaleZ, &animIndex, &animSpeed);
            //need unreal engine basic distance units are CM so need to multiply everything by 100
            FVector position = FVector(posX, posY, posZ);
            position = position * 100.0f;
            FQuat rotation = FQuat(rotX, rotY, rotZ, rotW);
            FVector scale = FVector(scaleX, scaleY, scaleZ);
            //create transofrm matrix, because cant pass scale otherwise
            FTransform transform = FTransform(rotation.Rotator(), position, scale);
            AMannequinActor* spawnedObject = GetWorld()->SpawnActor<AMannequinActor>(MannequinTemplate, transform);

            spawnedObject->SetAnimations(animSpeed, animIndex);
        }
        else
        {
            tmp++;
        }
    }

    LPoz = 0;
    file.close(); // Always remember to close the file
    
    previousCPUTimeSaved = FPlatformTime::Cycles64();
    LastFrameTime = FApp::GetCurrentTime();
    FString oututString = FPaths::ProjectDir() + TEXT("statisticsCollected.csv");
    outputFile = std::ofstream(TCHAR_TO_UTF8(*oututString), std::ios::out | std::ios::trunc);
    outputFile << "lp;TimeStamp;CPU FrameTime;RAMUsage;GPU Frame Time;VRAMUsage;FPS\n";
}

void ALevelForTest::Tick(float DeltaTime)
{

    Savedata();

    Super::Tick(DeltaTime);
 

}

void ALevelForTest::Savedata()
{
    LPoz += 1;
    const float deltaTime = FApp::GetCurrentTime() - LastFrameTime;
    const float frameRate = 1.0 / deltaTime;
    float cpuUsageFraction, cpuIdleFraction;

    //real cpu time = (cpuUsageFraction+cpuUdleFraction) * delta time
    //cpu Usage time and cpu idle time are calculated every frame by engine
    FPlatformProcess::GetPerFrameProcessorUsage(FPlatformProcess::GetCurrentProcessId(), cpuUsageFraction, cpuIdleFraction);
    const float cpuTime = (cpuUsageFraction + cpuIdleFraction) * deltaTime * 1000.0f;
    
    //gpu time from nanosecond to miliseconds
    const float gpuTime = FPlatformTime::ToMilliseconds(GGPUFrameTime);
    FPlatformMemoryStats memorystats;
    memorystats = FPlatformMemory::GetStats();
  
    const float ramUsed = memorystats.UsedPhysical / (1024.0f * 1024.0f);

    FRHICommandListImmediate* RHICmdList = &GRHICommandList.GetImmediateCommandList();
    //get used memory for some reason returns used memory in KB, no documentation btw :)
    const int64 intMemory = RHICmdList->GetUsedMemory();
    //vramUsed is in MB
    const float vramUsed = intMemory / 1024.0f;

    previousCPUTimeSaved = FPlatformTime::Cycles64();
    LastFrameTime = FApp::GetCurrentTime();
    if (outputFile.is_open())
    {
        outputFile << LPoz << ";" << FPlatformTime::ToSeconds(previousCPUTimeSaved) << ";" << cpuTime << ";" << ramUsed << ";" << gpuTime << ";" << vramUsed << ";" << frameRate << std::endl;
    }
    
}
