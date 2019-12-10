# Brain Visualization
This repository serves as the main repository for the Brain Visualization project.
Mentor: Ipek Oguz

## Goals
Read NRRD file and visualize neural connections in the brain through diffusion tensor imaging tractography in the VR environment.

## Versions
Unity Version: 2018.4.11
Oculus Version: 1.4.3

## Steps Taken
* **VR Environment Design** - Our environment design was minimalistic. We created a black environment to host our environment in. We had our brain in the middle, a file explorer to the left and a canvas to the right displaying text that explains how to use the buttons on Oculus Touch controllers.
* **NRRD Format IO w/ C#** - NRRD IO is handled by external python environment (v3.7, numpy). NRRD data is saved as NPY file, and handled by Accord.io in C#. Due to Accord.io’s limitation on type (int/long only), all data are multiplied by 10^15, and saved as long, remaining decimals are truncated. After reading, all values are divided by 10^15 to approximate original values. -Lingfeng
* **Display Module** - In order to fit and display brain model in an efficient and timely manner, display module is separated into three components:
  * Reading Data: Reading NPY file is done in async, allowing smooth VR experience.
  * Preparing Data: Selecting voxels to be displayed.
  * Displaying Data: Display data prepared by the second part. -Lingfeng
* **Full Brain Model Display** - At second part of display module, every other voxel in each dimension is selected and computed to approximate the represented brain model. -Lingfeng
* **Partial Brain Display** - At second part of display module, all voxels of selected slices are computed and handed to third part for display. -Lingfeng
* **Compute Tensor and Track Connectivity** - At second part of display module, computing tensor started with selected voxel along the major axis. Computation stops when reached the end of data or any voxel without major axis. -Lingfeng
* **Selection with Lasers** -  Added laser pointer controlled for the Oculus controllers for the selection of items within the application. Used Raycast to detect 3D objects in the scene by determining whether ray intersects with a Collider. Used UnityEvent to register a selection event callback that triggers the custom behavior when a particular button is pressed and released.
* **File Browsing** - Used a file browsing asset from the Unity Asset Store to be able to select and load files within the VR environment. Modified it to work in VR.
* **Slicing Brain** - Used y position of Raycast hit as the cutoff to generate a sliced brain.

## Controls
* Left Controller:
  * Joystick -- Move in Y-plane
  * Button X -- Move down
  * Button Y -- Move up
  * Grip -- Reset
* Right Controller:
  * Button A -- Interact with file browser
  * Grip -- Slice
  * Trigger - Select voxel for trace
