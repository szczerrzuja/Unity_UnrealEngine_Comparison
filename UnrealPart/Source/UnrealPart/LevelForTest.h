// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/LevelScriptActor.h"
#include "MannequinActor.h"
#include <fstream>

#include "LevelForTest.generated.h"

/**
 * 
 */
UCLASS()
class UNREALPART_API ALevelForTest : public ALevelScriptActor
{
	GENERATED_BODY()
	UPROPERTY(EditAnywhere, Category = "Spawning")
		TSubclassOf<AMannequinActor> MannequinTemplate;
	UPROPERTY(EditAnywhere)
		int maxNumberOfMannequins;

public: 
	ALevelForTest();
	~ALevelForTest();
	virtual void Tick(float DeltaTime) override;
	virtual void BeginPlay() override;

private:
	std::ofstream outputFile;
	uint64 previousCPUTimeSaved;
	int LPoz;
	bool canUsageBeSaved;
	void Savedata();

};
