using UnityEngine;

public class movement : MonoBehaviour
{
    public Rigidbody rb;

    // Update is called once per frame
    void FixedUpdate()
    {
        rb.AddForce(0, 100 * Time.deltaTime, 0);   
    }
}
