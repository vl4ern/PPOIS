using TMPro;
using UnityEngine;

// Этот скрипт отвечает за отображение рекорда на сцене Records
public class RecordsScreen : MonoBehaviour
{
    public TextMeshProUGUI bestScoreText;

    private void Start()
    {
        int bestScore = RecordManager.GetBestScore();

        if (bestScoreText != null)
        {
            bestScoreText.text = "Best Score: " + bestScore;
        }
    }
}