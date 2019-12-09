using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement : MonoBehaviour
{
    private int speed = 3;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Vector2 delt = OVRInput.Get(OVRInput.Axis2D.PrimaryThumbstick);
        if (delt != Vector2.zero)
        {
            GameObject[] gos = GameObject.FindGameObjectsWithTag("OVRCamera");
            foreach (GameObject go in gos)
            {
                float currentX = go.transform.position.x;
                float currentY = go.transform.position.y;
                float currentZ = go.transform.position.z;
                go.transform.position = new Vector3(currentX, currentY + speed * delt.x, currentZ + speed * delt.y);
            }
        }

        if (OVRInput.Get(OVRInput.Button.Three))
        {
            GameObject[] gos = GameObject.FindGameObjectsWithTag("OVRCamera");
            foreach (GameObject go in gos)
            {

                float currentX = go.transform.position.x;
                float currentY = go.transform.position.y;
                float currentZ = go.transform.position.z;
                go.transform.position = new Vector3(currentX + (float)((float)(speed) * 0.5), currentY, currentZ);
            }
        }

        if (OVRInput.Get(OVRInput.Button.Four))
        {
            GameObject[] gos = GameObject.FindGameObjectsWithTag("OVRCamera");
            foreach (GameObject go in gos)
            {

                float currentX = go.transform.position.x;
                float currentY = go.transform.position.y;
                float currentZ = go.transform.position.z;
                go.transform.position = new Vector3(currentX - (float)((float)(speed) * 0.5), currentY, currentZ);
            }
        }

    }
}
