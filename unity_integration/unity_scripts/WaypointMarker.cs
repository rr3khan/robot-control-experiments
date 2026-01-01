using UnityEngine;

/// <summary>
/// Waypoint Marker
/// Visual marker for target positions in the scene
/// </summary>
public class WaypointMarker : MonoBehaviour
{
    [Header("Visual Settings")]
    public Color markerColor = Color.green;
    public float height = 0.5f;
    public float radius = 0.2f;
    
    void OnDrawGizmos()
    {
        // Draw waypoint marker in scene view
        Gizmos.color = markerColor;
        
        // Draw sphere
        Gizmos.DrawSphere(transform.position + Vector3.up * height, radius);
        
        // Draw line to ground
        Gizmos.DrawLine(transform.position, transform.position + Vector3.up * height);
        
        // Draw arrow for orientation
        Vector3 forward = transform.forward * 0.5f;
        Gizmos.DrawRay(transform.position + Vector3.up * height, forward);
    }
    
    void OnDrawGizmosSelected()
    {
        // Draw larger marker when selected
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position + Vector3.up * height, radius * 1.5f);
    }
}
