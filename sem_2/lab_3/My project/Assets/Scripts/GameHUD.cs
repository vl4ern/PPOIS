using TMPro;
using UnityEngine;

public class GameHUD : MonoBehaviour
{
    public TextMeshProUGUI waveText;
    public TextMeshProUGUI weaponText;
    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI hpText;

    public GameObject gameOverText;

    public GameObject backToMenuButton;

    private int score = 0;

    private void Start()
    {
        SetWave(1);
        SetWeapon("Glock");
        SetScore(0);
        SetHP(10, 10);

        HideGameOver();
    }

    public void SetWave(int waveNumber)
    {
        if (waveText != null)
        {
            waveText.text = "Wave: " + waveNumber;
        }
    }

    public void SetWeapon(string weaponName)
    {
        if (weaponText != null)
        {
            weaponText.text = "Weapon: " + weaponName;
        }
    }

    public void SetScore(int newScore)
    {
        score = newScore;

        if (scoreText != null)
        {
            scoreText.text = "Score: " + score;
        }
    }

    public void AddScore(int amount)
    {
        score += amount;

        if (scoreText != null)
        {
            scoreText.text = "Score: " + score;
        }
    }

    public int GetScore()
    {
        return score;
    }

    public void SetHP(int currentHp, int maxHp)
    {
        if (hpText != null)
        {
            hpText.text = "HP: " + currentHp + " / " + maxHp;
        }
    }

    public void ShowGameOver()
    {
        if (gameOverText != null)
        {
            gameOverText.SetActive(true);
        }

        if (backToMenuButton != null)
        {
            backToMenuButton.SetActive(true);
        }
    }

    public void HideGameOver()
    {
        if (gameOverText != null)
        {
            gameOverText.SetActive(false);
        }

        if (backToMenuButton != null)
        {
            backToMenuButton.SetActive(false);
        }
    }
}