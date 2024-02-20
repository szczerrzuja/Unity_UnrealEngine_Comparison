// Fill out your copyright notice in the Description page of Project Settings.


#include "MannequinActor.h"

// Sets default values
AMannequinActor::AMannequinActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	SkeletalMesh = CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("YourSkeletalMeshComponent"));
	RootComponent = SkeletalMesh;

}

// Called when the game starts or when spawned
void AMannequinActor::BeginPlay()
{
	Super::BeginPlay();
	
}

// Called every frame
void AMannequinActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}

void AMannequinActor::SetAnimations_Implementation(float speed, int id)
{

}