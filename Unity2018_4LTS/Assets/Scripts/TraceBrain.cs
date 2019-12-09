using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Accord.Math;
using System.Linq;
using Vector3 = UnityEngine.Vector3;

public class TraceBrain : MonoBehaviour
{
    public Vector3Int pos;
    public GameObject withInfo;
    public GameObject DisplayModule;
    public bool gen;

    private List<Vector3Int> locations;
    float[,,,] arr;
    private int vecLength = 9;
    private double magnification = Mathf.Pow(10, 15);
    private double step = 20;
    private double error = 0.00000001;
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
            gen = false;
            arr = withInfo.GetComponent<LoadingJob>().arr;
            print(arr.GetUpperBound(0));
            print(arr.GetUpperBound(1));
            print(arr.GetUpperBound(2));
            print(arr.GetUpperBound(3));
            locations = traceBrain(pos, ref arr, pos, 1000);
            DisplayModule.GetComponent<DisplayObjCo>().tracing = true;
            DisplayModule.GetComponent<DisplayObjCo>().coors = locations;
            DisplayModule.GetComponent<DisplayObjCo>().gen = true;
            DisplayModule.SetActive(true);
        }
    }

    /*
     * origin: location start to work with
     * tensorField: entire tensorField working with, i.e. numpy 4d matrix from nrrd
     * internalKeeping: true location without rounding
     * return: a list of locations in image
     */
    List<Vector3Int> traceBrain(Vector3Int origin, ref float[,,,] tensorField, Vector3 internalKeeping, int ct)
    {
        if (ct == 0)
        {
            return new List<Vector3Int>();
        }
        int xDim = tensorField.GetUpperBound(0);
        int yDim = tensorField.GetUpperBound(1);
        int zDim = tensorField.GetUpperBound(2);
        if (origin.x < xDim && origin.y < yDim && origin.z < zDim)
        {
            List<float> subArr = new List<float>();
            for (int t = 0; t < vecLength; t++)
            {
                subArr.Add(tensorField[origin.x, origin.y, origin.z, t]);
            }
            Vector3 a = new Vector3(subArr[0], subArr[1], subArr[2]);
            Vector3 b = new Vector3(subArr[3], subArr[4], subArr[5]);
            Vector3 c = new Vector3(subArr[6], subArr[7], subArr[8]);/*
            Vector3 a = new Vector3(subArr[0], subArr[3], subArr[6]);
            Vector3 b = new Vector3(subArr[1], subArr[4], subArr[7]);
            Vector3 c = new Vector3(subArr[2], subArr[5], subArr[8]);*/
            double max = Mathf.Max(a.magnitude, b.magnitude, c.magnitude);
            double min = Mathf.Min(a.magnitude, b.magnitude, c.magnitude);
            // empty voxel
            if (max == 0)
            {
                return new List<Vector3Int>();
            }

            // no major
            if (max-min<=error)
            {
                return new List<Vector3Int>();
            }

            //with major
            Vector3 major;
            if (max == a.magnitude)
            {
                major = a;
            }else if(max== b.magnitude)
            {
                major = b;
            }
            else
            {
                major = c;
            }
          
            
            //Question: how to proceed to next location? What should be the length of each vector?
            
            //find next location and invoke transBrain recursively
            Vector3 nextVoxel = internalKeeping;
            nextVoxel.x = (float)(nextVoxel.x + major.x * step);
            nextVoxel.y = (float)(nextVoxel.y + major.y * step);
            nextVoxel.z = (float)(nextVoxel.z + major.z * step);
            Vector3Int externalVoxel = new Vector3Int((int)(nextVoxel.x), (int)(nextVoxel.y), (int)(nextVoxel.z));
            //get result from recursion and add current location AT FRONT
            while (externalVoxel.Equals(origin))
            {
                nextVoxel.x = (float)(nextVoxel.x + major.x * step);
                nextVoxel.y = (float)(nextVoxel.y + major.y * step);
                nextVoxel.z = (float)(nextVoxel.z + major.z * step);
                externalVoxel.x = (int)nextVoxel.x;
                externalVoxel.y = (int)nextVoxel.y;
                externalVoxel.z = (int)nextVoxel.z;
            }
            //print(nextVoxel);
            var result = traceBrain(externalVoxel, ref tensorField, nextVoxel, ct-1);
            result.Insert(0, externalVoxel);
            return result;
            




        }
        else
        {
            return new List<Vector3Int>();
        }

    }

    /*
     * convert 9*1 list to 3*3 vectors
     */
    void list2vector(List<float> subArr, List<Vector3> vectors, List<double> mags)
    {
        //if vector stored as column vector
        //Vector3 a = new Vector3(subArr[0], subArr[1], subArr[2]);
        //Vector3 b = new Vector3(subArr[3], subArr[4], subArr[5]);
        //Vector3 c = new Vector3(subArr[6], subArr[7], subArr[8]);
        Vector3 a = new Vector3(subArr[0], subArr[3], subArr[6]);
        Vector3 b = new Vector3(subArr[1], subArr[4], subArr[7]);
        Vector3 c = new Vector3(subArr[2], subArr[5], subArr[8]);
        vectors.Add(a);
        vectors.Add(b);
        vectors.Add(c);
        mags.Add(a.magnitude);
        mags.Add(b.magnitude);
        mags.Add(c.magnitude);
    }

}
