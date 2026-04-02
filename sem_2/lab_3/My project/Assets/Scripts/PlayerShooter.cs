using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

public enum WeaponType
{
    Glock,
    Shotgun,
    Rifle
}

public class PlayerShooter : MonoBehaviour
{
    public GameObject bulletPrefab;
    public Transform firePoint;

    public AudioClip shootSfx;

    private PlayerInput playerInput;
    private AudioSource audioSource;

    private InputAction fireAction;
    private InputAction selectGlockAction;
    private InputAction selectShotgunAction;
    private InputAction selectRifleAction;

    private WeaponType currentWeapon = WeaponType.Glock;
    private float nextFireTime = 0f;

    private GameHUD gameHUD;

    private void Awake()
    {
        playerInput = GetComponent<PlayerInput>();
        gameHUD = FindObjectOfType<GameHUD>();
        audioSource = GetComponent<AudioSource>();
    }

    private void OnEnable()
    {
        fireAction = playerInput.actions["Fire"];
        fireAction.Enable();
        fireAction.performed += OnFire;

        selectGlockAction = playerInput.actions["SelectGlock"];
        selectShotgunAction = playerInput.actions["SelectShotgun"];
        selectRifleAction = playerInput.actions["SelectRifle"];

        selectGlockAction.Enable();
        selectShotgunAction.Enable();
        selectRifleAction.Enable();

        selectGlockAction.performed += OnSelectGlock;
        selectShotgunAction.performed += OnSelectShotgun;
        selectRifleAction.performed += OnSelectRifle;
    }

    private void OnDisable()
    {
        fireAction.performed -= OnFire;
        fireAction.Disable();

        selectGlockAction.performed -= OnSelectGlock;
        selectShotgunAction.performed -= OnSelectShotgun;
        selectRifleAction.performed -= OnSelectRifle;

        selectGlockAction.Disable();
        selectShotgunAction.Disable();
        selectRifleAction.Disable();
    }

    private void Start()
    {
        UpdateWeaponHUD();
    }

    private void OnFire(InputAction.CallbackContext context)
    {
        if (Time.time < nextFireTime)
        {
            return;
        }

        Shoot();
    }

    private void Shoot()
    {
        if (bulletPrefab == null || firePoint == null)
        {
            Debug.LogWarning("Не назначен bulletPrefab или firePoint.");
            return;
        }

        PlayShootSound();

        switch (currentWeapon)
        {
            case WeaponType.Glock:
                ShootSingle();
                nextFireTime = Time.time + 0.35f;
                break;

            case WeaponType.Shotgun:
                ShootShotgun();
                nextFireTime = Time.time + 0.55f;
                break;

            case WeaponType.Rifle:
                StartCoroutine(ShootRifleBurst());
                nextFireTime = Time.time + 0.7f;
                break;
        }
    }

    private void PlayShootSound()
    {
        if (audioSource != null && shootSfx != null)
        {
            audioSource.PlayOneShot(shootSfx);
        }
    }

    private void ShootSingle()
    {
        SpawnBullet(transform.up);
    }

    private void ShootShotgun()
    {
        Vector2 leftDirection = Quaternion.Euler(0f, 0f, -10f) * transform.up;
        Vector2 rightDirection = Quaternion.Euler(0f, 0f, 10f) * transform.up;

        SpawnBullet(leftDirection);
        SpawnBullet(rightDirection);
    }

    private IEnumerator ShootRifleBurst()
    {
        SpawnBullet(transform.up);
        yield return new WaitForSeconds(0.08f);

        SpawnBullet(transform.up);
        yield return new WaitForSeconds(0.08f);

        SpawnBullet(transform.up);
    }

    private void SpawnBullet(Vector2 direction)
    {
        GameObject bulletObject = Instantiate(
            bulletPrefab,
            firePoint.position,
            Quaternion.identity
        );

        Bullet bullet = bulletObject.GetComponent<Bullet>();

        if (bullet != null)
        {
            bullet.SetDirection(direction);
        }
    }

    private void OnSelectGlock(InputAction.CallbackContext context)
    {
        currentWeapon = WeaponType.Glock;
        UpdateWeaponHUD();
    }

    private void OnSelectShotgun(InputAction.CallbackContext context)
    {
        currentWeapon = WeaponType.Shotgun;
        UpdateWeaponHUD();
    }

    private void OnSelectRifle(InputAction.CallbackContext context)
    {
        currentWeapon = WeaponType.Rifle;
        UpdateWeaponHUD();
    }

    private void UpdateWeaponHUD()
    {
        if (gameHUD == null)
        {
            return;
        }

        switch (currentWeapon)
        {
            case WeaponType.Glock:
                gameHUD.SetWeapon("Glock");
                break;

            case WeaponType.Shotgun:
                gameHUD.SetWeapon("Shotgun");
                break;

            case WeaponType.Rifle:
                gameHUD.SetWeapon("Rifle");
                break;
        }
    }
}