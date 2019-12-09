using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine;
using System.Collections;
using UnityEngine.UI; // Required when Using UI elements.

public class rotateObject : MonoBehaviour
{

    bool currentlyPressed;
    Quaternion brainRot;

    // Start is called before the first frame update
    void Start()
    {
        brainRot = transform.rotation;
    }

    public void ChangeXRotation(Slider slider)
    {
        transform.rotation = Quaternion.Euler(slider.value, transform.eulerAngles.y, transform.eulerAngles.z);
        brainRot = transform.rotation;
    }

    public void ChangeYRotation(Slider slider)
    {
        transform.rotation = Quaternion.Euler(transform.eulerAngles.x, slider.value, transform.eulerAngles.z);
        brainRot = transform.rotation;
    }

    public void ChangeZRotation(Slider slider)
    {
        transform.rotation = Quaternion.Euler(transform.eulerAngles.x, transform.eulerAngles.y, slider.value);
        brainRot = transform.rotation;
    }

    // Update is called once per frame
    void Update()
    {


        if (OVRInput.GetDown(OVRInput.Button.One))
        {
        }
        if (currentlyPressed && OVRInput.Get(OVRInput.Button.One))
        {
            currentlyPressed = false;
        }

        if (!OVRInput.Get(OVRInput.Button.One))
        {
            currentlyPressed = false;
        }
    }

    float rotSpeed = 20;

    void OnMouseDrag()
    {

        UnityEngine.Debug.Log("OnMouseDrag");

        float rotX = Input.GetAxis("Mouse X") * rotSpeed * Mathf.Deg2Rad;
        float rotY = Input.GetAxis("Mouse Y") * rotSpeed * Mathf.Deg2Rad;

        GameObject[] gos = GameObject.FindGameObjectsWithTag("RotationCenter");
        foreach (GameObject go in gos)
        {
            go.transform.RotateAround(Vector3.up, -rotX);
            go.transform.RotateAround(Vector3.right, rotY);
        }


    }

}
