using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class Listener : MonoBehaviour
{
    private Thread thread;
    private UdpClient udpServer;
    private bool isRunning = true;

    public int connectionPort = 25001;

    // Define the incoming streamed data variables here

    void Start()
    {
        thread = new Thread(GetData);
        thread.IsBackground = true;
        thread.Start();
    }

    void GetData()
    {
        try
        {
            udpServer = new UdpClient(connectionPort);
            IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, connectionPort);

            while (isRunning)
            {
                if (udpServer.Available > 0)
                {
                    byte[] receivedBytes = udpServer.Receive(ref remoteEndPoint);
                    string dataReceived = Encoding.UTF8.GetString(receivedBytes);
                    ParseData(dataReceived);
                }

                Thread.Sleep(5);
            }
        }
        catch (Exception e)
        {
            Debug.LogError("UDP Error: " + e.Message);
        }
        finally
        {
            Cleanup();
        }
    }

    void ParseData(string data)
    {
        string[] values = data.Split(' ');
        // if (values.Length < n) return; apply a failsafe here based on the output format

        try
        {
            //convery string values to float by indexing on the array
        }
        catch (Exception e)
        {
            Debug.LogError("Parsing error: " + e.Message);
        }
    }

    void OnApplicationQuit()
    {
        isRunning = false;
        thread.Join();
        Cleanup();
    }

    void Cleanup()
    {
        if (udpServer != null)
        {
            udpServer.Close();
            udpServer = null;
        }
    }
}
