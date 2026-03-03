using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    public GameObject[] enemyPrefabs;   

    public float spawnInterval = 1f;
    public float xRange = 5f;

    void Start()
    {
        InvokeRepeating(nameof(SpawnEnemy), 1f, spawnInterval);
    }

    void SpawnEnemy()
    {
        float x = Random.Range(-xRange, xRange);
        Vector2 spawnPosition = new Vector2(x, transform.position.y);

       
        int index = Random.Range(0, enemyPrefabs.Length);

        Instantiate(enemyPrefabs[index], spawnPosition, Quaternion.identity);
    }
}


