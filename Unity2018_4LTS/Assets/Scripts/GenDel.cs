using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenDel : MonoBehaviour
{
    public GameObject template;
    private float seperationVal = (float)0.8;
    public int val;
    public bool gen;
    private int[,,] arr;
    private List<GameObject> inDisplay;
    private Vector3Int center = new Vector3Int(0, 0, 0);
    // Start is called before the first frame update
    void Start()
    {
        gen = true;
        val = 0;
        arr=new int[2, 3, 4];
        inDisplay = new List<GameObject>();
        display(val);
    }

    void display(int yval)
    {
        if (gen)
        {
            foreach(GameObject i in inDisplay)
            {
                Destroy(i);
            }

            int xDim = arr.GetLength(0);
            int yDim = arr.GetLength(1);
            int zDim = arr.GetLength(2);
            //List<GameObject> result = new List<GameObject>();
            //compute front top right coordinate
            int x = center.x - (int)(xDim / 2);
            int y = center.y - (int)(yDim / 2);
            int z = center.z - (int)(zDim / 2);

            //create empty list
            //List<GameObject> result = new List<GameObject>();
            for (int i = 0; i < xDim; i++)
            {
                float xIter = x + i*seperationVal;
                for (int j = yval; j < yval + 1; j++)
                {
                    float yIter = y + j * seperationVal;
                    for (int k = 0; k < zDim; k++)
                    {
                        float zIter = z + k * seperationVal;
                        double val = arr[i, j, k];

                        val = Mathf.Max((float)val, 0);
                        val = Mathf.Min((float)val, 1);

                        inDisplay.Add(Instantiate(template, new Vector3(xIter, yIter, zIter), Quaternion.identity) as GameObject);




                    }
                    
                }
                
            }
        }
        gen = false;
    }



    // Update is called once per frame
    void Update()
    {
        display(val);
    }
}
