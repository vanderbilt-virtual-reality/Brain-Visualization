using System.Collections;
using UnityEngine;

public class RawInteraction : MonoBehaviour
{
    protected Material oldHoverMat;
    public Material hoverMat;
    public Material backIdle;
    public Material backACtive;
    public UnityEngine.UI.Text outText;
    public Material selectMat;
    public Color color;
    public Material clear;
    public Material reddishClear;

    public float selectedY = float.MinValue;

    public void OnSelected(Transform t)
    {
        selectedY = t.position.y;
    }
    public void OnSelected2(Transform t)
    {
        Collider[] intersecting = Physics.OverlapSphere(t.position, 0.01f);
        if (intersecting.Length > 0)
        {
            Record obj = intersecting[0].GetComponent<Record>();
            GameObject[] gos = GameObject.FindGameObjectsWithTag("TraceTag");
            foreach (GameObject go in gos)
            {
                
                GameObject.Find("StrongCube").GetComponent<Renderer>().material = clear;
                GameObject.Find("WeakCube").GetComponent<Renderer>().material = clear;
                  //  UnityEngine.Debug.Log("CHANGING");
                  //  GetComponent<Renderer>().material = clear;
                
                
                
                selectedY = float.MinValue;
                StartCoroutine(myOnSelected2(go,obj));
            }
        }
    }
    public IEnumerator myOnSelected2(GameObject go, Record obj)
    {
        UnityEngine.Debug.Log("Waiting for keepPrev");
        yield return new WaitForSecondsRealtime(10);
        GameObject[] gos3 = GameObject.FindGameObjectsWithTag("DisplayTag");
        foreach (GameObject go3 in gos3)
        {
            DisplayObjCo go3_display = go3.GetComponent<DisplayObjCo>();
            go3_display.keepPrev = true;
            go3_display.extraTracingVar = false;
        }
        UnityEngine.Debug.Log("Waiting for trace");

        yield return new WaitForSecondsRealtime(5);



        TraceBrain obj2 = go.GetComponent<TraceBrain>();
        obj2.pos = obj.coordinate;
        
        obj2.gen = true;



        UnityEngine.Debug.Log("Waiting for gen");

        yield return new WaitForSecondsRealtime(5);


        GameObject[] gos4 = GameObject.FindGameObjectsWithTag("DisplayTag");
        foreach (GameObject go3 in gos3)
        {
            DisplayObjCo go3_display = go3.GetComponent<DisplayObjCo>();
            go3_display.extraTracingVar = true;
        }

    }
}