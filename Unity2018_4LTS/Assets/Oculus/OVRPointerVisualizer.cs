using UnityEngine;
using UnityEngine.SceneManagement;

namespace ControllerSelection
{

    public class OVRPointerVisualizer : MonoBehaviour
    {
        [Header("(Optional) Tracking space")]
        [Tooltip("Tracking space of the OVRCameraRig.\nIf tracking space is not set, the scene will be searched.\nThis search is expensive.")]
        public Transform trackingSpace = null;
        [Header("Visual Elements")]
        [Tooltip("Line Renderer used to draw selection ray.")]
        public LineRenderer linePointer = null;
        [Tooltip("Fallback gaze pointer.")]
        public Transform gazePointer = null;
        [Tooltip("Visually, how far out should the ray be drawn.")]
        public float rayDrawDistance = 500;
        [Tooltip("How far away the gaze pointer should be from the camera.")]
        public float gazeDrawDistance = 3;
        [Tooltip("Show gaze pointer as ray pointer.")]
        public bool showRayPointer = true;

        // Start ray draw distance
        private const float StartRayDrawDistance = 0.032f;

        [HideInInspector]
        public OVRInput.Controller activeController = OVRInput.Controller.None;

        void Awake()
        {
            if (trackingSpace == null)
            {
                Debug.LogWarning("OVRPointerVisualizer did not have a tracking space set. Looking for one");
                trackingSpace = OVRInputHelpers.FindTrackingSpace();
            }
        }

        void OnEnable()
        {
            SceneManager.sceneLoaded += OnSceneLoaded;
        }

        void OnDisable()
        {
            SceneManager.sceneLoaded -= OnSceneLoaded;
        }

        void OnSceneLoaded(Scene scene, LoadSceneMode mode)
        {
            if (trackingSpace == null)
            {
                Debug.LogWarning("OVRPointerVisualizer did not have a tracking space set. Looking for one");
                trackingSpace = OVRInputHelpers.FindTrackingSpace();
            }
        }

        public void SetPointer(Ray ray)
        {
            float hitRayDrawDistance = rayDrawDistance;
            RaycastHit hit;
            if (Physics.Raycast(ray, out hit))
            {
                hitRayDrawDistance = hit.distance;
            }

            if (linePointer != null)
            {
                linePointer.SetPosition(0, ray.origin + ray.direction * StartRayDrawDistance);
                linePointer.SetPosition(1, ray.origin + ray.direction * hitRayDrawDistance);
            }

            if (gazePointer != null)
            {
                gazePointer.position = ray.origin + ray.direction * (showRayPointer ? hitRayDrawDistance : gazeDrawDistance);
            }
        }

        public void SetPointerVisibility()
        {
            if (trackingSpace != null && activeController != OVRInput.Controller.None)
            {
                if (linePointer != null)
                {
                    linePointer.enabled = true;
                }
                if (gazePointer != null)
                {
                    gazePointer.gameObject.SetActive(showRayPointer ? true : false);
                }
            }
            else
            {
                if (linePointer != null)
                {
                    linePointer.enabled = false;
                }
                if (gazePointer != null)
                {
                    gazePointer.gameObject.SetActive(showRayPointer ? false : true);
                }
            }
        }

        void Update()
        {
            activeController = OVRInputHelpers.GetControllerForButton(OVRInput.Button.PrimaryIndexTrigger, activeController);
            Ray selectionRay = OVRInputHelpers.GetSelectionRay(activeController, trackingSpace);
            SetPointerVisibility();
            SetPointer(selectionRay);
        }
    }
}