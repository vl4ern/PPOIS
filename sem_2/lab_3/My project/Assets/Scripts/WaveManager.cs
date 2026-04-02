using System.Collections;
using UnityEngine;

// Этот скрипт отвечает за чтение волн из json
// и запуск волн со спавном разных типов врагов
public class WaveManager : MonoBehaviour
{
    // Префабы разных типов врагов
    public GameObject enemyBasicPrefab;
    public GameObject enemyFastPrefab;
    public GameObject enemyTankPrefab;
    public GameObject enemyHeavyPrefab;
    public GameObject enemySwiftPrefab;

    // Json-файл с волнами
    public TextAsset wavesJsonFile;

    private WaveConfig waveConfig;
    private int currentWaveIndex = 0;
    private int aliveEnemies = 0;

    private GameHUD gameHUD;

    private void Start()
    {
        Debug.Log("WaveManager Start вызван");

        gameHUD = FindObjectOfType<GameHUD>();

        LoadWaveConfig();

        if (waveConfig != null && waveConfig.waves.Length > 0)
        {
            Debug.Log("Конфиг загружен, запускаем первую волну");
            StartCoroutine(StartWave(waveConfig.waves[currentWaveIndex]));
        }
        else
        {
            Debug.LogError("waveConfig пустой или волн нет");
        }
    }

    private void LoadWaveConfig()
    {
        if (wavesJsonFile == null)
        {
            Debug.LogError("Не назначен wavesJsonFile в Inspector");
            return;
        }

        string json = wavesJsonFile.text;
        Debug.Log("Содержимое json: " + json);

        waveConfig = JsonUtility.FromJson<WaveConfig>(json);

        if (waveConfig == null || waveConfig.waves == null || waveConfig.waves.Length == 0)
        {
            Debug.LogError("Не удалось загрузить данные волн");
        }
        else
        {
            Debug.Log("Загружено волн: " + waveConfig.waves.Length);
        }
    }

    private IEnumerator StartWave(WaveData wave)
    {
        Debug.Log("Старт волны: " + wave.waveNumber + ", тип врага: " + wave.enemyType);

        if (gameHUD != null)
        {
            gameHUD.SetWave(wave.waveNumber);
        }

        for (int i = 0; i < wave.enemyCount; i++)
        {
            SpawnEnemy(wave.enemyType);
            aliveEnemies++;

            yield return new WaitForSeconds(wave.spawnDelay);
        }
    }

    private void SpawnEnemy(string enemyType)
    {
        Vector2 spawnPosition = GetRandomSpawnPosition();

        GameObject prefabToSpawn = GetEnemyPrefabByType(enemyType);

        if (prefabToSpawn == null)
        {
            Debug.LogError("Не найден prefab для типа врага: " + enemyType);
            return;
        }

        GameObject enemyObject = Instantiate(prefabToSpawn, spawnPosition, Quaternion.identity);

        Enemy enemy = enemyObject.GetComponent<Enemy>();

        if (enemy != null)
        {
            enemy.SetWaveManager(this);
        }
        else
        {
            Debug.LogError("На prefab врага нет компонента Enemy!");
        }
    }

    private GameObject GetEnemyPrefabByType(string enemyType)
    {
        switch (enemyType)
        {
            case "Basic":
                return enemyBasicPrefab;

            case "Fast":
                return enemyFastPrefab;

            case "Tank":
                return enemyTankPrefab;

            case "Heavy":
                return enemyHeavyPrefab;

            case "Swift":
                return enemySwiftPrefab;
                
            default:
                return null;
        }
    }

    private Vector2 GetRandomSpawnPosition()
    {
        float offset = 0.5f;

        float minX = -7f;
        float maxX = 7f;
        float minY = -3.5f;
        float maxY = 3.5f;

        int side = Random.Range(0, 4);

        switch (side)
        {
            case 0:
                return new Vector2(minX - offset, Random.Range(minY, maxY));

            case 1:
                return new Vector2(maxX + offset, Random.Range(minY, maxY));

            case 2:
                return new Vector2(Random.Range(minX, maxX), minY - offset);

            case 3:
                return new Vector2(Random.Range(minX, maxX), maxY + offset);

            default:
                return new Vector2(0f, 0f);
        }
    }

    public void OnEnemyKilled()
    {
        aliveEnemies--;
        Debug.Log("Враг убит. Осталось врагов: " + aliveEnemies);

        if (aliveEnemies <= 0)
        {
            currentWaveIndex++;

            if (waveConfig != null && currentWaveIndex < waveConfig.waves.Length)
            {
                Debug.Log("Запускаем следующую волну");
                StartCoroutine(StartWave(waveConfig.waves[currentWaveIndex]));
            }
            else
            {
                Debug.Log("Все волны завершены");
            }
        }
    }
}