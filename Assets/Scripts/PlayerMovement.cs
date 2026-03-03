using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public float speed = 10f;
    public UDPReceiver udpReceiver;

    void Update()
    {
        if (udpReceiver == null) return;

        string data = udpReceiver.GetLatestData();

        if (string.IsNullOrEmpty(data)) return;

        float moveX = 0f;

        // ----- PARSE DIRECTION -----
        if (data.Contains("Left"))
            moveX = -1f;

        else if (data.Contains("Right"))
            moveX = 1f;

        else if (data.Contains("Standing"))
            moveX = 0f;

        // Move player
        transform.Translate(Vector3.right * moveX * speed * Time.deltaTime);
    }
}



