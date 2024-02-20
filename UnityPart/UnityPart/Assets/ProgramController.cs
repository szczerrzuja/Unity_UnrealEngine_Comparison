using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Profiling;
using Unity.Profiling;
using System;
using System.IO;

/*
https://gist.github.com/anarkila/f0c34e4daaac4c48b575eac04ad86064
For reference to stat name
*/

public class ProgramController : MonoBehaviour
{
    //reference to object prefab
    public GameObject mannequinPrefabRef;
    
    private StreamWriter LoggingStream;
    private ProfilerRecorder gpuRecorder;
    private ProfilerRecorder cpuRecorder;
    private float cpuUsed;
    private float ramUsed;
    private float gpuUsed;
    private float vramUsed;
    private bool wasPrefromanceSaved = false;
    private int LpNumber;


    //procesor data
   
    // Start is called before the first frame update
    void Start()
    {
        
        LpNumber = 0;
        cpuUsed = 0.0f;
        ramUsed = 0.0f;
        gpuUsed = 0.0f;
        vramUsed= 0.0f;
		LoggingStream = new StreamWriter("LoggedData.csv");
        LoggingStream.WriteLine("lp;TimeStamp;CPU FrameTime;RAMUsage;GPU Frame Time;VRAMUsage;FPS");
        gpuRecorder = new ProfilerRecorder(ProfilerCategory.Internal, "GPU Frame Time", 256);

        cpuRecorder = new ProfilerRecorder(ProfilerCategory.Internal, "CPU Main Thread Frame Time", 256);
        //start mesurement

        gpuRecorder.Start();
        cpuRecorder.Start();
        //cpuRecorder;
        
        InitializeTest();     
        InvokeRepeating("SavePerformance", 0.5f, 0.5f);

    }

    // Update is called once per frame
    void Update()
    {

        LogPerformance();

    }
    private void SavePerformance()
    {

        //due to io overload those statns need to be saved in seperate thread every second or 2 :)
        //In % of usage time
        gpuRecorder.Stop();
        cpuRecorder.Stop();

        //calculate GPU usage 

        var samples = new List<ProfilerRecorderSample>();
        gpuRecorder.CopyTo(samples, true);
        gpuUsed = 0.0f;
        foreach(var x in samples)
        {
            gpuUsed += x.Value;
        }
        //samples count is in nanoseconds, so i need to make it to seconds
        gpuUsed /= samples.Count * 1000000f;
        samples.Clear();
        //calculate CPU Usage       
        samples = new List<ProfilerRecorderSample>();
        cpuRecorder.CopyTo(samples, true);
        cpuUsed = 0.0f;
        foreach(var x in samples)
        {
            cpuUsed += x.Value;
        }
        //samples count is in nanoseconds, so i need to make it to seconds
        cpuUsed /= samples.Count  * 1000000f;

        //in MB
        ramUsed = Profiler.GetTotalReservedMemoryLong() / (1024f * 1024f); 

        //in MB of used VRAM
        vramUsed = Profiler.GetAllocatedMemoryForGraphicsDriver()/ (1024f * 1024f);
        wasPrefromanceSaved = true;
        gpuRecorder.Start();
        cpuRecorder.Start();

    }
    private void LogPerformance()
    {

        float FPS = 1/Time.deltaTime;
        float timeFromStart = Time.realtimeSinceStartup;
        if(!wasPrefromanceSaved)
            LoggingStream.WriteLine(LpNumber.ToString()+";"+timeFromStart.ToString()+";"+"null"+";"+"null"+";"+"null"+";"+"null"+";"+FPS.ToString());
        else
        {
            LoggingStream.WriteLine(LpNumber.ToString()+";"+timeFromStart.ToString()+";"+cpuUsed.ToString("F2")+";"+ramUsed.ToString("F2")+";"+gpuUsed.ToString("F2")+";"+vramUsed.ToString("F2")+";"+FPS.ToString());
            wasPrefromanceSaved = false;
        }
            
        LpNumber++;
    }
    void InitializeTest()
    {
        var stream = new StreamReader("points.csv");
        
        //to read header
        string data = stream.ReadLine();
        int var_for_limiter = 0;
        int maxModels = 4000, points = 23570;
        int skipsPerLoad = Convert.ToInt32(Math.Floor((float)points/(float)maxModels));
        /*
        k = multiply by 1000
        20k models uses around 8GB of ram when camera is moving, but on GPU little over middle shelf engine runs on 1 frames per 5 seconds - 0.2fps, 98% gpu usage
        so i need to limit those, starting with 4k  
        4k still too much
        500?
        */

        while(!stream.EndOfStream && var_for_limiter <maxModels)
        {
            for(int i = 0; i<skipsPerLoad && !stream.EndOfStream;i++)
            {
                data = stream.ReadLine();
            }
            var_for_limiter++;

            string[] values = data.Split(',');
            //data in csv file are made in unreal engine system - y and z must be flipped
            
            Vector3 position = new Vector3(float.Parse(values[1], System.Globalization.CultureInfo.InvariantCulture),
            float.Parse(values[3], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[2], System.Globalization.CultureInfo.InvariantCulture));

            Quaternion quat = new Quaternion(float.Parse(values[4], System.Globalization.CultureInfo.InvariantCulture),
            float.Parse(values[6], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[5], System.Globalization.CultureInfo.InvariantCulture),
            float.Parse(values[7], System.Globalization.CultureInfo.InvariantCulture));

        
            GameObject newGameObject = Instantiate(mannequinPrefabRef, position, quat);
            newGameObject.transform.localScale = new Vector3(float.Parse(values[8], System.Globalization.CultureInfo.InvariantCulture),
            float.Parse(values[10], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[9], System.Globalization.CultureInfo.InvariantCulture));

            newGameObject.gameObject.GetComponent<MannequinScript>().SetAnimatorAnimation(int.Parse(values[11], System.Globalization.CultureInfo.InvariantCulture), 
            float.Parse(values[11], System.Globalization.CultureInfo.InvariantCulture));
        }

        stream.Close();
    }
    void OnApplicationQuit()
    {
        LoggingStream.Close();
    }


}
