using UnityEngine;

public class Enemy : MonoBehaviour
{
    public float moveSpeed = 2f;
    public int maxHealth = 1;
    public int contactDamage = 1;
    public float damageCooldown = 0.5f;
    public int scoreValue = 1;

    public AudioClip deathSfx;

    private int currentHealth;
    private Transform player;
    private PlayerHealth playerHealth;
    private GameHUD gameHUD;
    private WaveManager waveManager;
    private bool isDead = false;
    private float nextDamageTime = 0f;

    private void Start()
    {
        currentHealth = maxHealth;

        GameObject playerObject = GameObject.Find("Player");

        if (playerObject != null)
        {
            player = playerObject.transform;
            playerHealth = playerObject.GetComponent<PlayerHealth>();
        }

        gameHUD = FindObjectOfType<GameHUD>();
    }

    private void Update()
    {
        if (player == null || isDead)
        {
            return;
        }

        Vector2 direction = (player.position - transform.position).normalized;
        transform.position += (Vector3)(direction * moveSpeed * Time.deltaTime);
    }

    public void SetWaveManager(WaveManager manager)
    {
        waveManager = manager;
    }

    public void TakeDamage(int damage)
    {
        if (isDead)
        {
            return;
        }

        currentHealth -= damage;

        Debug.Log(gameObject.name + " получил урон. HP: " + currentHealth + " / " + maxHealth);

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    public void Die()
    {
        if (isDead)
        {
            return;
        }

        isDead = true;

        Debug.Log("Враг умер: " + gameObject.name);

        if (deathSfx != null)
        {
            AudioSource.PlayClipAtPoint(deathSfx, transform.position);
        }

        if (gameHUD != null)
        {
            gameHUD.AddScore(scoreValue);
        }

        if (waveManager != null)
        {
            waveManager.OnEnemyKilled();
        }
        else
        {
            Debug.LogError("WaveManager не назначен у врага!");
        }

        Destroy(gameObject);
    }

    private void OnTriggerStay2D(Collider2D other)
    {
        if (isDead)
        {
            return;
        }

        PlayerHealth health = other.GetComponent<PlayerHealth>();

        if (health != null)
        {
            if (Time.time >= nextDamageTime)
            {
                health.TakeDamage(contactDamage);
                nextDamageTime = Time.time + damageCooldown;
            }
        }
    }
}