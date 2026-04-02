using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneLoader : MonoBehaviour
{
    public void LoadGame()
    {
        SceneManager.LoadScene("Game");
    }

    public void LoadRecords()
    {
        SceneManager.LoadScene("Records");
    }

    public void LoadHelp()
    {
        SceneManager.LoadScene("Help");
    }

    public void LoadMainMenu()
    {
        SceneManager.LoadScene("MainMenu");
    }

    public void ExitGame()
    {
        Debug.Log("Выход из игры");
        Application.Quit();
    }
}
