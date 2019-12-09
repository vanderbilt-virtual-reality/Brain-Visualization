using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Accord.Math;
using System.Linq;

public class NPYIO : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        //Note data read in are int64 values that are 10^15 times larger than original data
        //to accommodate limitation of Accord.IO that it doesn't support float
        var arr=Accord.IO.NpyFormat.LoadMatrix(@"C:\Users\op\BrainVisualization\Unity2018_4LTS\Assets\tmp\sample.npy");

        for (int x = arr.GetLowerBound(0); x <= arr.GetUpperBound(0); x++) //85
        {
            for (int y = arr.GetLowerBound(1); y <= arr.GetUpperBound(1); y++) //144
            {
                for (int z = arr.GetLowerBound(2); z <= arr.GetUpperBound(2); z++) //144
                {
                    bool dataExists = false;
                    for (int t = arr.GetLowerBound(3); t <= arr.GetUpperBound(3); t++) //9
                    {
                        if ((long)arr.GetValue(x,y,z,t) > 0)
                        {
                            dataExists = true;
                        }
                    }

                    if (dataExists)
                    {
                        // This means we have data at coordinate (x, y, z)
                    }
                }
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
