using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RotateBrain : MonoBehaviour
{
    Slider XRotationSlider;
    Slider YRotationSlider;
    Slider ZRotationSlider;

    // Use this for initialization
    void Start()
    {
        XRotationSlider =
            GameObject.Find("XRotationSlider").GetComponent<Slider>();
        YRotationSlider =
            GameObject.Find("YRotationSlider").GetComponent<Slider>();
        ZRotationSlider =
            GameObject.Find("ZRotationSlider").GetComponent<Slider>();
    }

    // Update is called once per frame
    void Update()
    {
        transform.rotation = Quaternion.Euler(XRotationSlider.value,
            transform.eulerAngles.y, transform.eulerAngles.z);
        transform.rotation = Quaternion.Euler(transform.eulerAngles.x,
            YRotationSlider.value, transform.eulerAngles.z);
        transform.rotation = Quaternion.Euler(transform.eulerAngles.x,
            transform.eulerAngles.y, ZRotationSlider.value);
    }
}
