using UnityEngine;

public class Bullet : MonoBehaviour
{
    public float speed = 8f;
    public AmmoType ammoType;

    public Vector2 direction = Vector2.up;

    public int damage = 1; 

    void Update()
    {
        transform.Translate(direction * speed * Time.deltaTime);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        Enemy enemy = other.GetComponent<Enemy>();
        EnemyHealth health = other.GetComponent<EnemyHealth>();

        if (enemy != null && health != null)
        {
          
            if (enemy.requiredAmmo == ammoType)
            {
                health.TakeDamage(damage);   // damage instead of destroy
            }

            Destroy(gameObject); // destroy bullet
        }
    }
}


