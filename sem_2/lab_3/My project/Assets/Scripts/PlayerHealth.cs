using UnityEngine;

public class PlayerHealth : MonoBehaviour
{
    public int maxHealth = 10;

    public AudioClip hitSfx;
    public AudioClip gameOverSfx;

    private int currentHealth;
    private GameHUD gameHUD;
    private AudioSource audioSource;
    private bool isDead = false;

    private void Start()
    {
        Time.timeScale = 1f;

        currentHealth = maxHealth;
        gameHUD = FindObjectOfType<GameHUD>();
        audioSource = GetComponent<AudioSource>();

        UpdateHUD();
    }

    public void TakeDamage(int damage)
    {
        if (isDead)
        {
            return;
        }

        currentHealth -= damage;

        if (currentHealth < 0)
        {
            currentHealth = 0;
        }

        if (audioSource != null && hitSfx != null)
        {
            audioSource.PlayOneShot(hitSfx);
        }

        Debug.Log("Игрок получил урон. Текущее HP: " + currentHealth);

        UpdateHUD();

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    private void UpdateHUD()
    {
        if (gameHUD != null)
        {
            gameHUD.SetHP(currentHealth, maxHealth);
        }
    }

    private void Die()
    {
        if (isDead)
        {
            return;
        }

        isDead = true;

        Debug.Log("Игрок погиб");

        if (audioSource != null && gameOverSfx != null)
        {
            audioSource.PlayOneShot(gameOverSfx);
        }

        if (gameHUD != null)
        {
            gameHUD.ShowGameOver();
        }

        Time.timeScale = 0f;
    }
}