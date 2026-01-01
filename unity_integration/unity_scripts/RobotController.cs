using UnityEngine;
using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;

/// <summary>
/// Robot Controller for Unity-ROS Communication
/// Handles TCP communication with ROS 2 bridge and applies control commands
/// </summary>
public class RobotController : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosHost = "localhost";
    public int rosPort = 10000;
    
    [Header("Robot Configuration")]
    public float wheelRadius = 0.05f;
    public float wheelBase = 0.3f;
    
    [Header("Visual Elements")]
    public Transform leftWheel;
    public Transform rightWheel;
    
    // Network
    private TcpClient client;
    private NetworkStream stream;
    private Thread receiveThread;
    private bool isConnected = false;
    
    // Robot state
    private Vector3 position;
    private float orientation; // theta in radians
    private float linearVelocity;
    private float angularVelocity;
    
    // Control
    private float targetLinearVel = 0f;
    private float targetAngularVel = 0f;
    
    void Start()
    {
        ConnectToROS();
    }
    
    void ConnectToROS()
    {
        try
        {
            client = new TcpClient(rosHost, rosPort);
            stream = client.GetStream();
            isConnected = true;
            
            Debug.Log($"Connected to ROS at {rosHost}:{rosPort}");
            
            // Start receive thread
            receiveThread = new Thread(ReceiveData);
            receiveThread.IsBackground = true;
            receiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.LogError($"Failed to connect to ROS: {e.Message}");
        }
    }
    
    void Update()
    {
        if (!isConnected) return;
        
        // Apply control commands
        ApplyControl();
        
        // Send state to ROS
        SendStateToROS();
        
        // Manual control with keyboard (for testing)
        HandleKeyboardInput();
    }
    
    void ApplyControl()
    {
        // Update velocities
        linearVelocity = targetLinearVel;
        angularVelocity = targetAngularVel;
        
        // Apply to transform
        float dt = Time.deltaTime;
        
        // Update orientation
        orientation += angularVelocity * dt;
        
        // Update position
        position.x += linearVelocity * Mathf.Cos(orientation) * dt;
        position.z += linearVelocity * Mathf.Sin(orientation) * dt;
        
        // Apply to GameObject
        transform.position = position;
        transform.rotation = Quaternion.Euler(0, orientation * Mathf.Rad2Deg, 0);
        
        // Animate wheels
        if (leftWheel != null && rightWheel != null)
        {
            float leftWheelVel = (linearVelocity - angularVelocity * wheelBase / 2) / wheelRadius;
            float rightWheelVel = (linearVelocity + angularVelocity * wheelBase / 2) / wheelRadius;
            
            leftWheel.Rotate(Vector3.right, leftWheelVel * Mathf.Rad2Deg * dt);
            rightWheel.Rotate(Vector3.right, rightWheelVel * Mathf.Rad2Deg * dt);
        }
    }
    
    void SendStateToROS()
    {
        if (!isConnected || stream == null) return;
        
        try
        {
            // Create JSON message
            string json = $"{{\"type\":\"state\",\"x\":{position.x},\"y\":{position.z}," +
                         $"\"theta\":{orientation},\"linear_vel\":{linearVelocity}," +
                         $"\"angular_vel\":{angularVelocity}}}}\n";
            
            byte[] data = Encoding.UTF8.GetBytes(json);
            stream.Write(data, 0, data.Length);
        }
        catch (Exception e)
        {
            Debug.LogError($"Failed to send state: {e.Message}");
            isConnected = false;
        }
    }
    
    void ReceiveData()
    {
        byte[] buffer = new byte[4096];
        
        while (isConnected)
        {
            try
            {
                if (stream.DataAvailable)
                {
                    int bytesRead = stream.Read(buffer, 0, buffer.Length);
                    string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    
                    // Parse JSON (simplified)
                    if (message.Contains("\"type\":\"control\""))
                    {
                        // Extract velocities from JSON
                        // Note: For production, use a proper JSON parser
                        ParseControlMessage(message);
                    }
                }
                Thread.Sleep(20); // 50 Hz
            }
            catch (Exception e)
            {
                Debug.LogError($"Receive error: {e.Message}");
                isConnected = false;
                break;
            }
        }
    }
    
    void ParseControlMessage(string json)
    {
        // Simplified JSON parsing (use JsonUtility or Newtonsoft.Json for production)
        try
        {
            // More robust parsing using string constants
            string linearVelKey = "\"linear_velocity\":";
            string angularVelKey = "\"angular_velocity\":";
            
            int linVelIndex = json.IndexOf(linearVelKey);
            int angVelIndex = json.IndexOf(angularVelKey);
            
            if (linVelIndex != -1 && angVelIndex != -1)
            {
                string linVelStr = json.Substring(linVelIndex + linearVelKey.Length);
                linVelStr = linVelStr.Substring(0, linVelStr.IndexOfAny(new char[] { ',', '}' }));
                
                string angVelStr = json.Substring(angVelIndex + angularVelKey.Length);
                angVelStr = angVelStr.Substring(0, angVelStr.IndexOfAny(new char[] { ',', '}' }));
                
                // Use TryParse for safe parsing
                if (float.TryParse(linVelStr, out float parsedLinear))
                {
                    targetLinearVel = parsedLinear;
                }
                else
                {
                    Debug.LogWarning($"Failed to parse linear velocity: {linVelStr}");
                }
                
                if (float.TryParse(angVelStr, out float parsedAngular))
                {
                    targetAngularVel = parsedAngular;
                }
                else
                {
                    Debug.LogWarning($"Failed to parse angular velocity: {angVelStr}");
                }
            }
        }
        catch (Exception e)
        {
            Debug.LogWarning($"Failed to parse control message: {e.Message}");
        }
    }
    
    void HandleKeyboardInput()
    {
        // Manual control for testing
        float forward = Input.GetAxis("Vertical");
        float turn = Input.GetAxis("Horizontal");
        
        if (Mathf.Abs(forward) > 0.01f || Mathf.Abs(turn) > 0.01f)
        {
            targetLinearVel = forward * 0.5f;
            targetAngularVel = turn * 1.0f;
        }
    }
    
    void OnApplicationQuit()
    {
        isConnected = false;
        
        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Join(1000);
        }
        
        if (stream != null) stream.Close();
        if (client != null) client.Close();
    }
    
    void OnDestroy()
    {
        OnApplicationQuit();
    }
}
