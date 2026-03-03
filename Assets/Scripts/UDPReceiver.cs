using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class UDPReceiver : MonoBehaviour
{
    public int listenPort = 25001;
    private UdpClient client;
    private Thread receiveThread;
    private string latestData = "0";

    void Start()
    {
        client = new UdpClient(listenPort);
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();
    }

    void ReceiveData()
    {
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, listenPort);
        while (true)
        {
            try
            {
                byte[] data = client.Receive(ref remoteEndPoint);
                latestData = Encoding.UTF8.GetString(data);
                Debug.Log("Received: " + latestData);
            }
            catch { }
        }
    }

    public string GetLatestData()
    {
        return latestData;
    }

    void OnApplicationQuit()
    {
        if (receiveThread != null) receiveThread.Abort();
        if (client != null) client.Close();
    }
}
