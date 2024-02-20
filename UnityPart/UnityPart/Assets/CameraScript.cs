using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;

public class CameraScript : MonoBehaviour
{
    public Rigidbody CameraRB;
    StreamReader dataStream;
    Vector3 currentPoint;
    Vector3 cameraRotationVariable;
    float currentVelocity;
    bool isTeleported = false;
    bool isLookingOnPoint = false;

    // Start is called before the first frame update
    void Start()
    {
        //init camera state
        dataStream = new StreamReader("CameraRoute.csv");
        string data = dataStream.ReadLine();
        while(data[0] == '#')
        {
            data = dataStream.ReadLine();
        }
        //skipp data description column
        data = dataStream.ReadLine();
        //first row, init camera
        data = dataStream.ReadLine();
        string[] values = data.Split(';');
        this.transform.position = new Vector3(float.Parse(values[1], System.Globalization.CultureInfo.InvariantCulture),
            float.Parse(values[3], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[2], System.Globalization.CultureInfo.InvariantCulture));

        this.transform.rotation = Quaternion.Euler(float.Parse(values[7], System.Globalization.CultureInfo.InvariantCulture),
        float.Parse(values[9], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[8], System.Globalization.CultureInfo.InvariantCulture));
        //next point on path of camera
        LoadNextPoint();
        CameraRB.velocity = (currentPoint-transform.position).normalized * currentVelocity;
    }

    // Update is called once per frame
    void Update()
    {
        
       Vector3 positionDifference = currentPoint-transform.position;
       if(positionDifference.sqrMagnitude <= currentVelocity/5.0f)
       {
            LoadNextPoint();
            if(isTeleported)
            {
                TeleportCamera();
            }
            this.transform.rotation = Quaternion.Euler(cameraRotationVariable);
            CameraRB.velocity = (currentPoint-transform.position).normalized * currentVelocity;
       }
        if(isLookingOnPoint)
        {
            RotateCameraTowards();
        }
        
    }
    void TeleportCamera(){
        transform.position = currentPoint;
        LoadNextPoint();
    }

    void LoadNextPoint(){
        string data = dataStream.ReadLine();
        //if is end of file
        if(!dataStream.EndOfStream)
        {
            //process data
            string[] values = data.Split(';');        

            currentPoint = new Vector3(float.Parse(values[1], System.Globalization.CultureInfo.InvariantCulture),
                float.Parse(values[3], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[2], System.Globalization.CultureInfo.InvariantCulture));

            isTeleported = System.Convert.ToBoolean(int.Parse(values[4]));
            currentVelocity = float.Parse(values[5], System.Globalization.CultureInfo.InvariantCulture);

            isLookingOnPoint = System.Convert.ToBoolean(int.Parse(values[6]));

            cameraRotationVariable = new Vector3(float.Parse(values[7], System.Globalization.CultureInfo.InvariantCulture),
            float.Parse(values[9], System.Globalization.CultureInfo.InvariantCulture),float.Parse(values[8], System.Globalization.CultureInfo.InvariantCulture));

        }
        else{
            //quit app when end of file
            Application.Quit();
        }
    }
    void RotateCameraTowards(){
        Vector3 direction = (cameraRotationVariable-transform.position).normalized;
        transform.rotation = Quaternion.LookRotation(direction);
    }
    void OnApplicationQuit()
    {
        dataStream.Close();
    }
}
