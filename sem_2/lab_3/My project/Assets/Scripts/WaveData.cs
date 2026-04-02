using System;
using UnityEngine;

// Данные одной волны
[Serializable]
public class WaveData
{
    // Номер волны
    public int waveNumber;

    // Тип врага для этой волны
    public string enemyType;

    // Сколько врагов нужно заспавнить
    public int enemyCount;

    // Задержка между спавнами
    public float spawnDelay;
}

// Корневой объект для json
[Serializable]
public class WaveConfig
{
    public WaveData[] waves;
}