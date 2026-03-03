using UnityEngine;

public class EnemyHealth : MonoBehaviour
{
    public int maxHealth = 1;   // normal enemy dies in 1 hit
    private int currentHealth;

    void Start()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(int damage)
    {
        currentHealth -= damage;

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    void Die()
    {
        Destroy(gameObject);
    }
}

