using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenerateObj : MonoBehaviour
{
    public GameObject objTemplate1;
    public GameObject objTemplate2;

    public int yVal;

    //this is important, it is an GameObject that returns arr, a 3d array, hooked up at Start()
    public GameObject withInfo;

    private double[,,] arr;
    public bool gen;
    //control the space between each object
    private float seperationVal = (float)0.08;
    //control the center of object generation
    private Vector3Int center = new Vector3Int(0, 0, 0);
    //reference for all object generated
    private List<GameObject> inDisplay;
    // Start is called before the first frame update
    void Start()
    {
        gen = true;
        yVal = 0;
        //Destroy(objTemplate1);
        //Destroy(objTemplate2);
        //Destroy(objTemplate3);
        //GameObject tmp=Instantiate(objTemplate1, new Vector3(1 * 2.0F, 0, 0), Quaternion.identity) as GameObject;
        arr = withInfo.GetComponent<OutputArr>().arrMag;

        inDisplay = new List<GameObject>();
        objectFactory(ref yVal);
    }

    // Update is called once per frame
    void Update()
    {
        objectFactory(ref yVal);
    }

    void objectFactory(ref int yval)
    {
        if (gen)
        {
            foreach (GameObject i in inDisplay)
            {
                Destroy(i);
            }
            int xDim = arr.GetLength(0);
            int yDim = arr.GetLength(1);
            int zDim = arr.GetLength(2);
            //List<GameObject> result = new List<GameObject>();
            //compute front top right coordinate
            float x = center.x - (xDim*seperationVal / 2);
            float y = center.y - (yDim*seperationVal / 2);
            float z = center.z - (zDim*seperationVal / 2);

            //sanitize yVal
            yval = Mathf.Min(yval, yDim-1);
            yval = Mathf.Max(yval, 0);

            //create empty list
            //List<GameObject> result = new List<GameObject>();
            
            for (int i = 0; i < xDim; i++)  //axial
            {
                float xIter = x+ i*seperationVal;
                for (int j = yval; j < yval+1; j++) //coronal
                {
                    float yIter = y + j * seperationVal;
                    for (int k = 0; k < zDim; k++) //Sagittal
                    {
                        float zIter = z + k * seperationVal;
                        double val = arr[i, j, k];

                        val = Mathf.Max((float)val, 0);
                        val = Mathf.Min((float)val, 1);

                        if (val > 0.001)
                        {
                            //print(1);
                            inDisplay.Add(Instantiate(objTemplate1, new Vector3(xIter, yIter, zIter), Quaternion.identity)as GameObject);
                        }
                        else if (val > 0)
                        {
                            //print(0.5);
                            inDisplay.Add(Instantiate(objTemplate2, new Vector3(xIter, yIter, zIter), Quaternion.identity)as GameObject);
                        }




                    }
                }
            }
        }
        gen = false;
        //return result;
    }

    IEnumerator wait(int sec)
    {
        yield return new WaitForSeconds(sec);
    }
}
