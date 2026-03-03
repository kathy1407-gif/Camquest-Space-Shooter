using UnityEngine;

public class AmmoSwitch : MonoBehaviour
{
    public UDPReceiver udpReceiver;

    // ammo flags
    public bool isAmmo1 = true;
    public bool isAmmo2 = false;

    public int maxAmmo = 30;
    public int ammo1Count = 30;
    public int ammo2Count = 10;

    private int currentAmmo;

    public GameObject ammo1Prefab;
    public GameObject ammo2Prefab;

    public Transform firePoint;

    public float fireRate = 0.25f;
    private float nextFireTime;

    private string lastFlick = "None";

    void Start()
    {
        LoadAmmo();
    }

    void Update()
    {
        if (udpReceiver == null)
            return;

        string data = udpReceiver.GetLatestData();

        if (!string.IsNullOrEmpty(data))
        {
            HandleGestures(data);
        }
    }

    void HandleGestures(string data)
    {
        string flick = "None";

        if (data.Contains("Flick: Index"))
            flick = "Index";
        else if (data.Contains("Flick: Middle"))
            flick = "Middle";
        else if (data.Contains("Flick: Ring"))
            flick = "Ring";

        if (flick == lastFlick)
            return;

        lastFlick = flick;

        Debug.Log("Detected Flick: " + flick);

        if (flick == "Index")
            TryShoot();
        else if (flick == "Middle")
            SwitchToAmmo1();
        else if (flick == "Ring")
            SwitchToAmmo2();
    }

    void TryShoot()
    {
        if (Time.time < nextFireTime)
            return;

        if (currentAmmo <= 0)
            return;

        nextFireTime = Time.time + fireRate;

        currentAmmo--;

        GameObject prefab;

        if (isAmmo1)
            prefab = ammo1Prefab;
        else
            prefab = ammo2Prefab;

        Instantiate(prefab, firePoint.position, firePoint.rotation);

        Debug.Log("Shot fired. Ammo left: " + currentAmmo);
    }

    void SwitchToAmmo1()
    {
        if (isAmmo1)
            return;

        SaveAmmo();

        isAmmo1 = true;
        isAmmo2 = false;

        LoadAmmo();

        Debug.Log("Switched to Ammo 1");
    }

    void SwitchToAmmo2()
    {
        if (isAmmo2)
            return;

        SaveAmmo();

        isAmmo1 = false;
        isAmmo2 = true;

        LoadAmmo();

        Debug.Log("Switched to Ammo 2");
    }

    void SaveAmmo()
    {
        if (isAmmo1)
            ammo1Count = currentAmmo;
        else
            ammo2Count = currentAmmo;
    }

    void LoadAmmo()
    {
        if (isAmmo1)
            currentAmmo = ammo1Count;
        else
            currentAmmo = ammo2Count;
    }
}


