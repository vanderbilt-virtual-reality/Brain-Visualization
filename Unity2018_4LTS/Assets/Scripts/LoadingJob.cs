using System.Collections;
using System.Collections.Generic;
using Unity.Jobs;
using UnityEngine;

public class LoadingJob : MonoBehaviour
{
    SideLoadData loadingJob;
    //output arr
    public float[,,,] arr;
    public string pathToFile;
    public bool gen;
    public bool working;
    //magnitude of longest of arr
    public double[,,] arrMag;
    public Vector3 center;
    public GameObject displayContent;

    private bool oneTime;

    // Start is called before the first frame update


    void Start()
    {
        oneTime = false;
        gen = false;
        loadingJob = new SideLoadData();
        loadingJob.pathToFile = pathToFile;
        loadingJob.center = center;
        loadingJob.displayContent = displayContent;
        loadingJob.Start();
        working = !loadingJob.isCompleted();
    }

    // Update is called once per frame
    void Update()
    {
        
        
        working = !loadingJob.isCompleted();

        if (working && !oneTime)
        {
            print(loadingJob.jobDescription());
            oneTime = true;
        }
        if (!working)
        {
            arr = loadingJob.arr;
            arrMag = loadingJob.arrMag;
            //set active
            loadingJob.OnFinished();
            
            
        }
        if (working && gen)
        {
            gen = false;
        }
        if (gen)
        {
            oneTime = false;
            gen = false;
            loadingJob = new SideLoadData();
            loadingJob.pathToFile = pathToFile;
            loadingJob.center = center;
            loadingJob.displayContent = displayContent;
            loadingJob.Start();
        }
        
    }
}
