// Fill out your copyright notice in the Description page of Project Settings.


#include "TestCameraActor.h"
#include "Kismet/KismetSystemLibrary.h"
// Sets default values
ATestCameraActor::ATestCameraActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;

	isTeleported = false;
	isLookingOnPoint = false;

	BoxComponent = CreateDefaultSubobject<UBoxComponent>(TEXT("BoxComponent"));
	CameraComponent = CreateDefaultSubobject<UCameraComponent>(TEXT("CameraComponent"));
	RootComponent = BoxComponent;
	CameraComponent->AttachToComponent(BoxComponent, FAttachmentTransformRules::KeepRelativeTransform);

}

// Called when the game starts or when spawned
void ATestCameraActor::BeginPlay()
{

	GetWorld()->GetFirstPlayerController()->SetViewTarget(this);
	

	
	FString filePath = FPaths::ProjectDir() + TEXT("CameraRoute.csv");
	cameraRouteFile = std::ifstream(TCHAR_TO_UTF8(*filePath));
	std::string line;
	std::getline(cameraRouteFile, line);
	while (line[0] == '#')
	{
		std::getline(cameraRouteFile, line);
	}
	//skipp data description line
	std::getline(cameraRouteFile, line);
	int lp, teleport, looking;
	float posX, posY, posZ, velocity, rx, ry, rz;
	//process data into variables
	sscanf_s(line.c_str(), "%i;%f;%f;%f;%i;%f;%i;%f;%f;%f", &lp, &posX, &posY, &posZ, &teleport, &velocity, &looking, &rx, &ry, &rz );
	this->SetActorLocationAndRotation(FVector(posX, posY, posZ)*100.0f, FRotator(rx, rz, ry));
	LoadNextPoint();
	//need to be check for code safety reasons
	if (BoxComponent)
	{
		//velocity in ue is cm/s need to be converted to m/s
		BoxComponent->SetPhysicsLinearVelocity((NextPointPosition - GetActorLocation()).GetSafeNormal() * currentVelocity);
	}
	Super::BeginPlay();

}

// Called every frame
void ATestCameraActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	FVector positionDifference = NextPointPosition - GetActorLocation();
	if (positionDifference.Length() <= currentVelocity / 5.0f)
	{

		LoadNextPoint();
		if (isTeleported)
		{
			TeleportCamera();
		}
		this->SetActorRotation(FRotator(RotationVariable.X, RotationVariable.Y, RotationVariable.Z));

		BoxComponent->SetPhysicsLinearVelocity(FVector(NextPointPosition - GetActorLocation()).GetSafeNormal() * currentVelocity, false);
		//BoxComponent->AddImpulse(FVector(NextPointPosition - GetActorLocation()).GetSafeNormal() * currentVelocity, NAME_None, true);

	}
	if (isLookingOnPoint)
	{
		RotateCameraTowards();
	}

}

void ATestCameraActor::LoadNextPoint()
{
	if (!cameraRouteFile.eof())
	{
		
		std::string line;
		std::getline(cameraRouteFile, line);
		int lp, teleport, looking;
		float posX, posY, posZ, velocity, rx, ry, rz;
		//process data into variables
		sscanf_s(line.c_str(), "%i;%f;%f;%f;%i;%f;%i;%f;%f;%f", &lp, &posX, &posY, &posZ, &teleport, &velocity, &looking, &rx, &ry, &rz);
		currentVelocity = velocity*100.0f;
		NextPointPosition.Set(posX*100.0f, posY * 100.0f, posZ * 100.0f);
		RotationVariable.Set(rx, rz, ry);
		isTeleported = (bool)teleport;
		isLookingOnPoint = (bool)looking;
		UE_LOG(LogTemp, Warning, TEXT("%i"), lp);
	}
	else
	{
		//end of file reached, end of test, close "game"
		cameraRouteFile.close();
		UKismetSystemLibrary::QuitGame(GetWorld(), GetWorld()->GetFirstPlayerController(), EQuitPreference::Quit, false);
		
	}
}
void ATestCameraActor::TeleportCamera()
{
	SetActorLocation(NextPointPosition);
	LoadNextPoint();
}
void ATestCameraActor::RotateCameraTowards()
{
	FVector DirectionToTarget = RotationVariable - GetActorLocation();
	FRotator rotator = FRotationMatrix::MakeFromX(DirectionToTarget).Rotator();
	SetActorRotation(rotator);

}