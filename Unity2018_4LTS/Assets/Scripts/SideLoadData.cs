using System.Collections;
using System.Collections.Generic;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;

public class SideLoadData : Threading
{

    public string pathToFile;
    public double magnification;
    //output arr
    public float[,,,] arr;
    //magnitude of longest of arr
    public double[,,] arrMag;
    public Vector3 center;

    public GameObject displayContent;

    double computeMag(float[] subArr)
    {
        //if vector stored as column vector
        Vector3 a = new Vector3(subArr[0], subArr[3], subArr[6]);
        Vector3 b = new Vector3(subArr[1], subArr[4], subArr[7]);
        Vector3 c = new Vector3(subArr[2], subArr[5], subArr[8]);
        return Mathf.Max(a.magnitude, b.magnitude, c.magnitude);
    }
    protected override void ThreadFunc()
    {
        magnification = Mathf.Pow(10, 15);
        var tensorField = Accord.IO.NpyFormat.LoadMatrix(pathToFile);
        int xDim = tensorField.GetUpperBound(0);
        int yDim = tensorField.GetUpperBound(1);
        int zDim = tensorField.GetUpperBound(2);
        arrMag = new double[xDim, yDim, zDim];
        arr = new float[xDim, yDim, zDim, 9];

        for (int i = 0; i < xDim; i++)
        {
            for (int j = 0; j < yDim; j++)
            {
                for (int k = 0; k < zDim; k++)
                {
                    float[] tmp = new float[9];
                    for (int m = 0; m < 9; m++)
                    {
                        arr[i, j, k, m] = (float)((long)tensorField.GetValue(i, j, k, m) / (float)magnification);
                        tmp[m] = arr[i, j, k, m];

                    }
                    //compute magnitude
                    arrMag[i, j, k] = computeMag(tmp);
                }
            }
        }

    }

    public override void OnFinished()
    {
        base.OnFinished();
        displayContent.SetActive(true);
    }

    public override string jobDescription()
    {
        return "LoadingData";
    }


}
