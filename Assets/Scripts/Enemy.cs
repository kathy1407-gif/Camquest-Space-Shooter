using UnityEngine;

public class Enemy : MonoBehaviour
{
    public float speed = 2f;

    // choosing which ammo can kill this enemy
    public AmmoType requiredAmmo = AmmoType.Index;

    public int damage = 1;

    [Header("Shooting")]
    public GameObject enemyBulletPrefab;
    public float shootInterval = 1f;

    private float timer;

    void Update()
    {
        // moving down
        transform.Translate(Vector2.down * speed * Time.deltaTime);

        // destroying self(enemy) if goes below gamescreen
        if (transform.position.y < -6f)
        {
            Destroy(gameObject);
            return;
        }

        // new timer set
        timer += Time.deltaTime;

        if (timer >= shootInterval)
        {
            Shoot();
            timer = 0f;
        }
    }

    void Shoot()
    {
        if (enemyBulletPrefab == null) return;

        GameObject bulletObj =
            Instantiate(enemyBulletPrefab, transform.position, Quaternion.identity);

        // Getting Bullet script from spawned bullet
        Bullet bullet = bulletObj.GetComponent<Bullet>();

        if (bullet != null)
        {
            // shooting down
            bullet.direction = Vector2.down;

            // Enemy bullet is Ammo Type 1 
            bullet.ammoType = AmmoType.Index;
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        PlayerHealth player = other.GetComponent<PlayerHealth>();

        if (player != null)
        {
            player.TakeDamage(damage);
            Destroy(gameObject);
        }
    }
}




