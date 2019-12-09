using UnityEngine;
using System.Collections;
using SimpleFileBrowser;

public class FileBrowserUtilities : MonoBehaviour
{

	void Start()
	{
		FileBrowser.SetFilters( true, new FileBrowser.Filter( "Processed Files", ".npy" ), new FileBrowser.Filter( "Unprocessed Files", ".nrrd" ) );
		FileBrowser.SetDefaultFilter( ".npy" );
		FileBrowser.SetExcludedExtensions( ".lnk", ".tmp", ".zip", ".rar", ".exe" );
		FileBrowser.AddQuickLink( "Users", "C:\\Users", null ); //TODO: Link to correct directory
		FileBrowser.SingleClickMode = true;

		FileBrowser.HideDialog(); //Allows usage of canvas

		StartCoroutine( ShowLoadDialogCoroutine() );
	}

	IEnumerator ShowLoadDialogCoroutine()
	{
		yield return FileBrowser.WaitForLoadDialog( false, "C:/Users/beddarbt/Desktop/BrainVis2.0/trunk/Unity2018_4LTS/Assets/tmp", "Load File", "Load" );

		// Dialog is closed
		// Print whether a file is chosen (FileBrowser.Success)
		// and the path to the selected file (FileBrowser.Result) (null, if FileBrowser.Success is false)
		Debug.Log( FileBrowser.Success + " " + FileBrowser.Result );
		string fileType = FileBrowser.Result.Substring(FileBrowser.Result.Length - 4, 4);

		if(fileType == ".npy")
		{
            //ReadFile.GetComponent.LoadingJob().pathToFile = FileBrowser.Result;
		}else if (fileType == "nrrd")
		{
            //PythonLoader.GetComponent.Testing().fileToProcess = FileBrowser.Result;
		}

		StartCoroutine( ShowLoadDialogCoroutine() );
	}

}
