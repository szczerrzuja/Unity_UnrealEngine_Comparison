// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Camera/CameraComponent.h"
#include "Components/BoxComponent.h"
#include <iostream>
#include <sstream>
#include <string>
#include <fstream>
#include "TestCameraActor.generated.h"

UCLASS()
class UNREALPART_API ATestCameraActor : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ATestCameraActor();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

private:
	UPROPERTY(EditAnywhere)
	UCameraComponent* CameraComponent;
	UPROPERTY(EditAnywhere)
	UBoxComponent* BoxComponent;

	FVector RotationVariable;
	FVector NextPointPosition;
	float currentVelocity;
	bool isTeleported, isLookingOnPoint;
	std::ifstream cameraRouteFile;
	void LoadNextPoint();
	void TeleportCamera();
	void RotateCameraTowards();

};
