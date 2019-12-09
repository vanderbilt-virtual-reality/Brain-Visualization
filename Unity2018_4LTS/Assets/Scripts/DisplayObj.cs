using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DisplayObj : MonoBehaviour
{
    public GameObject objTemplate1;
    public GameObject objTemplate2;
    public GameObject tracto;
    public GameObject withInfo;
    public List<Vector3Int> coors;
    public bool tracing;
    public bool gen;
    public bool keepPrev;

    private double[,,] arr;

    //control the space between each object
    private float seperationVal = (float)0.06;
    //control the center of object generation
    private Vector3 center;
    //reference for all object generated
    private List<GameObject> inDisplay;

    // Start is called before the first frame update
    void Start()
    {
        tracing = false;
        keepPrev = false;
        gen = true;
        arr = withInfo.GetComponent<LoadingJob>().arrMag;
        center = withInfo.GetComponent<LoadingJob>().center;
        inDisplay = new List<GameObject>();
        display(coors, keepPrev);
    }

    // Update is called once per frame
    void Update()
    {
        display(coors, keepPrev);
    }

    void display(List<Vector3Int> coordinates, bool keepPrev)
    {
        //destroy everything if not keeping
        if (!keepPrev && gen)
        {
            foreach (GameObject i in inDisplay)
            {
                Destroy(i);
            }
        }
        if (gen)
        {
            int xDim = arr.GetLength(0);
            int yDim = arr.GetLength(1);
            int zDim = arr.GetLength(2);
            //List<GameObject> result = new List<GameObject>();
            //compute back bottom left coordinate
            float x = center.x - (xDim * seperationVal / 2);
            float y = center.y - (yDim * seperationVal / 2);
            float z = center.z - (zDim * seperationVal / 2);
            foreach (Vector3Int coor in coordinates)
            {
                double val = arr[coor.x, coor.y, coor.z];
                Vector3 pos = new Vector3(x + coor.x * seperationVal, y + coor.y * seperationVal, z + coor.z * seperationVal);
                if (tracing)
                {
                    UnityEngine.Debug.Log(pos.x);
                    UnityEngine.Debug.Log(pos.y);
                    UnityEngine.Debug.Log(pos.z);
                    UnityEngine.Debug.Log("___________");

                    //specialized for tractography
                    tracto.GetComponent<Record>().coordinate = coor;
                    GameObject[] gos = GameObject.FindGameObjectsWithTag("RotationCenter");
                    Quaternion brainRot = Quaternion.identity;
                    foreach (GameObject go in gos)
                    {
                        brainRot = go.transform.rotation;
                    }

                    inDisplay.Add(Instantiate(tracto, pos, brainRot) as GameObject);
                }
                else
                {
                    //show strong connectivity & low connectivity
                    val = Mathf.Max((float)val, 0);
                    val = Mathf.Min((float)val, 1);

                    if (val > 0.001)
                    {
                        //print(1);
                        objTemplate1.GetComponent<Record>().coordinate = coor;
                        inDisplay.Add(Instantiate(objTemplate1, pos, Quaternion.identity) as GameObject);
                    }
                    else if (val > 0)
                    {
                        //print(0.5);
                        objTemplate2.GetComponent<Record>().coordinate = coor;
                        inDisplay.Add(Instantiate(objTemplate2, pos, Quaternion.identity) as GameObject);
                    }
                }

            }
        }
        gen = false;

    }


}
