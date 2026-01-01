using UnityEngine;

/// <summary>
/// Camera Follow Script
/// Smoothly follows the robot with configurable offset and damping
/// </summary>
public class CameraFollow : MonoBehaviour
{
    [Header("Target")]
    public Transform target;
    
    [Header("Camera Settings")]
    public Vector3 offset = new Vector3(0, 5, -3);
    public float smoothSpeed = 0.125f;
    public bool lookAtTarget = true;
    
    void LateUpdate()
    {
        if (target == null) return;
        
        // Calculate desired position
        Vector3 desiredPosition = target.position + offset;
        
        // Smoothly interpolate
        Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed);
        transform.position = smoothedPosition;
        
        // Look at target
        if (lookAtTarget)
        {
            transform.LookAt(target);
        }
    }
}
