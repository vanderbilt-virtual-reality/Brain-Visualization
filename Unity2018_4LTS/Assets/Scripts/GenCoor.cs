using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenCoor : MonoBehaviour
{
    public GameObject DisplayModule;
    public bool gen;
    public int yVal;

    //this is important, it is an GameObject that returns arr, a 3d array, hooked up at Start()
    public GameObject withInfo;

    private double[,,] arr;
    private List<Vector3Int> coors;
    // Start is called before the first frame update
    void Start()
    {
        gen = true;
        
    }

    // Update is called once per frame
    void Update()
    {
        if (gen)
        {
            arr = withInfo.GetComponent<LoadingJob>().arrMag;
            coors = objectFactory(ref yVal);
            DisplayModule.GetComponent<DisplayObjCo>().tracing = false;
            DisplayModule.GetComponent<DisplayObjCo>().coors = coors;
            DisplayModule.GetComponent<DisplayObjCo>().gen = true;
            DisplayModule.SetActive(true);
            gen = false;
        }
        
    }

    List<Vector3Int> objectFactory(ref int yval)
    {
        
        int xDim = arr.GetLength(0);
        int yDim = arr.GetLength(1);
        int zDim = arr.GetLength(2);

        //sanitize yVal
        yval = Mathf.Min(yval, yDim - 1);
        yval = Mathf.Max(yval, 0);

        //create empty list
        List<Vector3Int> result = new List<Vector3Int>();
        //find locations
        for(int j = 0; j < yDim; j=j+2)
        {
            for (int i = 0; i < xDim; i=i+2)
            {
                for (int k = 0; k < zDim; k=k+2)
                {
                    double val = arr[i, j, k];
                    val = Mathf.Max((float)val, 0);
                    val = Mathf.Min((float)val, 1);
                    if (val > 0)
                    {
                        result.Add(new Vector3Int(i, j, k));
                    }

                }
            }
        }
        

        return result;
    }

    IEnumerator callDisplay()
    {
        DisplayModule.SetActive(true);
        yield return new WaitForSeconds(2);
        DisplayModule.SetActive(false);
    }



}
