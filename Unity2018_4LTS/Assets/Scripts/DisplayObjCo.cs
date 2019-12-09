using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class DisplayObjCo : MonoBehaviour
{
    public GameObject objTemplate1;
    public GameObject objTemplate2;
    public GameObject tracto;
    public GameObject withInfo;

    public Transform parent;

    public List<Vector3Int> coors;
    public bool tracing;
    public bool gen;

    public bool keepPrev;

    private double[,,] arr;

    //control the space between each object
    private float seperationVal = (float)0.8;
    //control the center of object generation
    private Vector3 center;
    //reference for all object generated
    public List<GameObject> inDisplay;
    private bool working;
    // Start is called before the first frame update

    public float previousYCutoff = float.MinValue;
    public bool extraTracingVar = true;
    void Start()
    {
        working = true;
        arr = withInfo.GetComponent<LoadingJob>().arrMag;
        center = withInfo.GetComponent<LoadingJob>().center;
        StartCoroutine(Display(keepPrev, previousYCutoff));
    }

    // Update is called once per frame
    void Update()
    {
        //reset
        if (OVRInput.Get(OVRInput.Axis1D.PrimaryHandTrigger, OVRInput.Controller.LTouch) > 0)
        {
            SceneManager.LoadScene(SceneManager.GetActiveScene().name);
//            previousYCutoff = float.MinValue;
  //          Start();
        }


        GameObject[] gos = GameObject.FindGameObjectsWithTag("RawInteraction");
        float yCutoff = previousYCutoff;
        foreach (GameObject go in gos)
        {
            RawInteraction obj = go.GetComponent<RawInteraction>();
            yCutoff = obj.selectedY;
        }

        if (working && gen)
        {
            gen = false;
        }
        if (gen || yCutoff != previousYCutoff)
        {
            previousYCutoff = yCutoff;
            Start();
        }

    }

    public IEnumerator Display(bool keepPrev, double yCutoff)
    {

        List<Vector3Int> coordinates = coors;
        //destroy everything if not keeping
        if (!keepPrev || gen)
        {
            if (extraTracingVar)
            {
                foreach (GameObject i in inDisplay)
                {
                    Destroy(i);
                }
                inDisplay = new List<GameObject>();
            }
        }
        gen = false;
        if (working)
        {
            int xDim = arr.GetLength(0);
            int yDim = arr.GetLength(1);
            int zDim = arr.GetLength(2);
            //List<GameObject> result = new List<GameObject>();
            //compute back bottom left coordinate
            float x = center.x - (xDim * seperationVal / 2);
            float y = center.y - (yDim * seperationVal / 2);
            float z = center.z - (zDim * seperationVal / 2);

            for (int i = 0; i < coordinates.Count; i++)
            {
                double val = arr[coordinates[i].x, coordinates[i].y, coordinates[i].z];
                Vector3 pos = new Vector3(x + coordinates[i].x * seperationVal, y + coordinates[i].y * seperationVal, z + coordinates[i].z * seperationVal);

                if (pos.y >= yCutoff)
                {


                    if (tracing)
                    {
                        //specialized for tractography
                        tracto.GetComponent<Record>().coordinate = coordinates[i];
                        GameObject[] gos = GameObject.FindGameObjectsWithTag("RotationCenter");
                        Quaternion brainRot = Quaternion.identity;
                        foreach (GameObject go in gos)
                        {
                            brainRot = go.transform.rotation;
                            brainRot.z -= 90;
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
                            objTemplate1.GetComponent<Record>().coordinate = coordinates[i];
                            GameObject tmp = Instantiate(objTemplate1, pos, Quaternion.identity);
                            tmp.transform.SetParent(parent, false);
                            //tmp.isStatic = true;
                            inDisplay.Add(tmp);
                        }
                        else if (val > 0)
                        {
                            //print(0.5);
                            objTemplate2.GetComponent<Record>().coordinate = coordinates[i];
                            GameObject tmp = Instantiate(objTemplate2, pos, Quaternion.identity);
                            tmp.transform.SetParent(parent, false);
                            //tmp.isStatic = true;
                            inDisplay.Add(tmp);
                        }
                    }

                    if (i % 100000 == 0)
                    {
                        yield return null;
                    }
                }
            }
        }
        working = false;
        yield return null;
    }
}
