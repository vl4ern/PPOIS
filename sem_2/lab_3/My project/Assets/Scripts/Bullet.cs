using UnityEngine;

// Этот скрипт отвечает за полет пули и нанесение урона врагу
public class Bullet : MonoBehaviour
{
    // Скорость пули
    public float speed = 10f;

    // Время жизни пули
    public float lifeTime = 2f;

    // Урон пули
    public int damage = 1;

    // Ссылка на Rigidbody2D
    private Rigidbody2D rb;

    private void Awake()
    {
        // Получаем Rigidbody2D пули
        rb = GetComponent<Rigidbody2D>();
    }

    private void Start()
    {
        // Удаляем пулю через некоторое время,
        // чтобы они не копились бесконечно
        Destroy(gameObject, lifeTime);
    }

    // Задаем направление полета
    public void SetDirection(Vector2 direction)
    {
        direction = direction.normalized;

        // Если linearVelocity у тебя работает — оставляем его
        rb.linearVelocity = direction * speed;

        // Если вдруг снова будет ошибка, поменяешь на:
        // rb.velocity = direction * speed;
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        // Проверяем, есть ли у объекта компонент Enemy
        Enemy enemy = other.GetComponent<Enemy>();

        if (enemy != null)
        {
            // Наносим врагу урон
            enemy.TakeDamage(damage);

            // Уничтожаем пулю после попадания
            Destroy(gameObject);
        }
    }
}