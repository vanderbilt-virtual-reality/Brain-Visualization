using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VoxelRead : MonoBehaviour
{
    //location of arr
    public string pathToFile;
    private double magnification = Mathf.Pow(10, 15);
    //output arr
    public float[,,,] arr;
    //magnitude of longest of arr
    public double[,,] arrMag;

    // Start is called before the first frame update
    void Start()
    {
        //arrMag = new double[1,2,3];
        var tensorField = Accord.IO.NpyFormat.LoadMatrix(pathToFile);
        int xDim = tensorField.GetUpperBound(0);
        int yDim = tensorField.GetUpperBound(1);
        int zDim = tensorField.GetUpperBound(2);
        print(xDim);
        print(yDim);
        print(zDim);
        float[] tmp = new float[9];

        for (int m = 0; m < 9; m++)
        {
            float a = (float)((long)tensorField.GetValue(30,75,75, m) / (float)magnification);
            tmp[m] = a;
            print("val @" + m + " is " + (float)a);

        }
        print(computeMag(tmp));


    }
    double computeMag(float[] subArr)
    {
        //if vector stored as column vector
        Vector3 a = new Vector3(subArr[0], subArr[3], subArr[6]);
        Vector3 b = new Vector3(subArr[1], subArr[4], subArr[7]);
        Vector3 c = new Vector3(subArr[2], subArr[5], subArr[8]);
        return Mathf.Max(a.magnitude, b.magnitude, c.magnitude);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
