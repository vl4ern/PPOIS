using UnityEngine;

// Этот скрипт отвечает за сохранение и загрузку лучшего результата
public static class RecordManager
{
    // Ключ, под которым будем хранить лучший счет
    private const string BestScoreKey = "BestScore";

    // Получить лучший счет
    public static int GetBestScore()
    {
        return PlayerPrefs.GetInt(BestScoreKey, 0);
    }

    // Сохранить лучший счет, если новый результат лучше старого
    public static void SaveBestScore(int score)
    {
        int currentBest = GetBestScore();

        if (score > currentBest)
        {
            PlayerPrefs.SetInt(BestScoreKey, score);
            PlayerPrefs.Save();

            Debug.Log("Новый рекорд сохранен: " + score);
        }
    }

    // Сброс рекорда (полезно для тестов)
    public static void ResetBestScore()
    {
        PlayerPrefs.DeleteKey(BestScoreKey);
        PlayerPrefs.Save();

        Debug.Log("Рекорд сброшен");
    }
}