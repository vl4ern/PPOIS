using UnityEngine;
using UnityEngine.InputSystem;

// Этот скрипт отвечает за движение игрока
// и ограничивает его в пределах видимой области камеры
public class PlayerController : MonoBehaviour
{
    // Скорость игрока
    public float moveSpeed = 5f;

    // Небольшой отступ от края экрана
    public float borderPadding = 0.01f;

    // Ссылка на Rigidbody2D
    private Rigidbody2D rb;

    // Ссылка на PlayerInput
    private PlayerInput playerInput;

    // Действие движения
    private InputAction moveAction;

    // Направление движения
    private Vector2 movement;

    // Ссылка на главную камеру
    private Camera mainCamera;

    // Радиус игрока, чтобы он не вылезал за экран половиной корпуса
    private float playerRadius = 0.5f;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        playerInput = GetComponent<PlayerInput>();
        mainCamera = Camera.main;

        // Пробуем взять радиус из CircleCollider2D
        CircleCollider2D circleCollider = GetComponent<CircleCollider2D>();
        if (circleCollider != null)
        {
            // Учитываем масштаб объекта
            playerRadius = circleCollider.radius * transform.localScale.x;
        }
    }

    private void OnEnable()
    {
        moveAction = playerInput.actions["Move"];
        moveAction.Enable();
    }

    private void OnDisable()
    {
        moveAction.Disable();
    }

    private void Update()
    {
        // Считываем направление движения
        movement = moveAction.ReadValue<Vector2>();

        // Нормализуем, чтобы по диагонали не было ускорения
        movement = movement.normalized;
    }

    private void FixedUpdate()
    {
        // Двигаем игрока
        rb.linearVelocity = movement * moveSpeed;

        // Ограничиваем позицию в пределах камеры
        ClampPositionToCamera();
    }

    private void ClampPositionToCamera()
    {
        // Получаем нижнюю левую точку экрана в мировых координатах
        Vector3 bottomLeft = mainCamera.ViewportToWorldPoint(new Vector3(0f, 0f, 0f));

        // Получаем верхнюю правую точку экрана в мировых координатах
        Vector3 topRight = mainCamera.ViewportToWorldPoint(new Vector3(1f, 1f, 0f));

        Vector3 position = transform.position;

        // Ограничиваем X с учетом размера игрока
        position.x = Mathf.Clamp(
            position.x,
            bottomLeft.x + playerRadius + borderPadding,
            topRight.x - playerRadius - borderPadding
        );

        // Ограничиваем Y с учетом размера игрока
        position.y = Mathf.Clamp(
            position.y,
            bottomLeft.y + playerRadius + borderPadding,
            topRight.y - playerRadius - borderPadding
        );

        transform.position = position;
    }
}