"""
Analysis Utilities

Tools for analyzing and plotting experiment data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Optional


class ExperimentAnalyzer:
    """Analyzer for robotics experiment data."""
    
    def __init__(self, log_file: str):
        """
        Initialize the analyzer.
        
        Args:
            log_file: Path to the experiment log CSV file
        """
        self.log_file = log_file
        self.data = pd.read_csv(log_file)
        
        # Convert timestamp to relative time
        if 'timestamp' in self.data.columns:
            self.data['time'] = self.data['timestamp'] - self.data['timestamp'].iloc[0]
    
    def plot_trajectory(self, ax=None, show_target=True):
        """
        Plot robot trajectory in 2D space.
        
        Args:
            ax: Matplotlib axis (creates new if None)
            show_target: Whether to show target positions
        
        Returns:
            Matplotlib axis
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot actual trajectory
        ax.plot(self.data['x'], self.data['y'], 'b-', linewidth=2, label='Actual')
        ax.plot(self.data['x'].iloc[0], self.data['y'].iloc[0], 'go', 
                markersize=10, label='Start')
        ax.plot(self.data['x'].iloc[-1], self.data['y'].iloc[-1], 'ro', 
                markersize=10, label='End')
        
        # Plot target if available
        if show_target and 'target_x' in self.data.columns:
            ax.plot(self.data['target_x'], self.data['target_y'], 'r--', 
                   linewidth=1, alpha=0.5, label='Target')
        
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_title('Robot Trajectory')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        return ax
    
    def plot_errors(self, ax=None):
        """
        Plot position and orientation errors over time.
        
        Args:
            ax: Matplotlib axis (creates new if None)
        
        Returns:
            Matplotlib axis
        """
        if ax is None:
            fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        
        # Position error
        ax[0].plot(self.data['time'], self.data['position_error'], 'b-', linewidth=2)
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Position Error (m)')
        ax[0].set_title('Position Error Over Time')
        ax[0].grid(True, alpha=0.3)
        
        # Orientation error
        ax[1].plot(self.data['time'], self.data['orientation_error'], 'r-', linewidth=2)
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('Orientation Error (rad)')
        ax[1].set_title('Orientation Error Over Time')
        ax[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return ax
    
    def plot_velocities(self, ax=None):
        """
        Plot linear and angular velocities over time.
        
        Args:
            ax: Matplotlib axis (creates new if None)
        
        Returns:
            Matplotlib axis
        """
        if ax is None:
            fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        
        # Linear velocity
        ax[0].plot(self.data['time'], self.data['linear_velocity'], 'b-', linewidth=2)
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Linear Velocity (m/s)')
        ax[0].set_title('Linear Velocity Over Time')
        ax[0].grid(True, alpha=0.3)
        
        # Angular velocity
        ax[1].plot(self.data['time'], self.data['angular_velocity'], 'r-', linewidth=2)
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('Angular Velocity (rad/s)')
        ax[1].set_title('Angular Velocity Over Time')
        ax[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return ax
    
    def plot_control_signals(self, ax=None):
        """
        Plot control signals over time.
        
        Args:
            ax: Matplotlib axis (creates new if None)
        
        Returns:
            Matplotlib axis
        """
        if ax is None:
            fig, ax = plt.subplots(2, 1, figsize=(12, 8))
        
        # Linear control
        ax[0].plot(self.data['time'], self.data['control_linear'], 'b-', linewidth=2)
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Linear Control (m/s)')
        ax[0].set_title('Linear Control Signal')
        ax[0].grid(True, alpha=0.3)
        
        # Angular control
        ax[1].plot(self.data['time'], self.data['control_angular'], 'r-', linewidth=2)
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('Angular Control (rad/s)')
        ax[1].set_title('Angular Control Signal')
        ax[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return ax
    
    def generate_full_report(self, output_path: Optional[str] = None):
        """
        Generate a comprehensive analysis report.
        
        Args:
            output_path: Path to save the report figure
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Create grid
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Trajectory
        ax1 = fig.add_subplot(gs[0, :])
        self.plot_trajectory(ax1)
        
        # Errors
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(self.data['time'], self.data['position_error'], 'b-', linewidth=2)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Position Error (m)')
        ax2.set_title('Position Error')
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(self.data['time'], self.data['orientation_error'], 'r-', linewidth=2)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Orientation Error (rad)')
        ax3.set_title('Orientation Error')
        ax3.grid(True, alpha=0.3)
        
        # Velocities
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.plot(self.data['time'], self.data['linear_velocity'], 'b-', linewidth=2)
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Linear Velocity (m/s)')
        ax4.set_title('Linear Velocity')
        ax4.grid(True, alpha=0.3)
        
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.plot(self.data['time'], self.data['angular_velocity'], 'r-', linewidth=2)
        ax5.set_xlabel('Time (s)')
        ax5.set_ylabel('Angular Velocity (rad/s)')
        ax5.set_title('Angular Velocity')
        ax5.grid(True, alpha=0.3)
        
        # Add experiment info
        exp_id = self.data['experiment_id'].iloc[0] if 'experiment_id' in self.data.columns else 'N/A'
        controller = self.data['controller_type'].iloc[0] if 'controller_type' in self.data.columns else 'N/A'
        fig.suptitle(f'Experiment Analysis: {exp_id} (Controller: {controller})', 
                    fontsize=16, fontweight='bold')
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Report saved to: {output_path}")
        
        return fig
    
    def compute_statistics(self):
        """Compute performance statistics."""
        stats = {
            'experiment_id': self.data['experiment_id'].iloc[0] if 'experiment_id' in self.data.columns else 'N/A',
            'controller_type': self.data['controller_type'].iloc[0] if 'controller_type' in self.data.columns else 'N/A',
            'duration': self.data['time'].iloc[-1] if 'time' in self.data.columns else 0,
            'mean_position_error': self.data['position_error'].mean(),
            'max_position_error': self.data['position_error'].max(),
            'final_position_error': self.data['position_error'].iloc[-1],
            'mean_orientation_error': abs(self.data['orientation_error']).mean(),
            'max_orientation_error': abs(self.data['orientation_error']).max(),
            'final_orientation_error': abs(self.data['orientation_error'].iloc[-1]),
        }
        
        return stats
    
    def print_statistics(self):
        """Print performance statistics."""
        stats = self.compute_statistics()
        
        print("\n" + "="*60)
        print("EXPERIMENT STATISTICS")
        print("="*60)
        print(f"Experiment ID: {stats['experiment_id']}")
        print(f"Controller: {stats['controller_type']}")
        print(f"Duration: {stats['duration']:.2f} s")
        print("\nPosition Error:")
        print(f"  Mean: {stats['mean_position_error']:.4f} m")
        print(f"  Max:  {stats['max_position_error']:.4f} m")
        print(f"  Final: {stats['final_position_error']:.4f} m")
        print("\nOrientation Error:")
        print(f"  Mean: {stats['mean_orientation_error']:.4f} rad ({np.degrees(stats['mean_orientation_error']):.2f}°)")
        print(f"  Max:  {stats['max_orientation_error']:.4f} rad ({np.degrees(stats['max_orientation_error']):.2f}°)")
        print(f"  Final: {stats['final_orientation_error']:.4f} rad ({np.degrees(stats['final_orientation_error']):.2f}°)")
        print("="*60 + "\n")


def compare_experiments(log_files: List[str], output_path: Optional[str] = None):
    """
    Compare multiple experiments.
    
    Args:
        log_files: List of paths to experiment log CSV files
        output_path: Path to save the comparison figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    analyzers = [ExperimentAnalyzer(f) for f in log_files]
    
    # Plot trajectories
    for analyzer in analyzers:
        controller = analyzer.data['controller_type'].iloc[0] if 'controller_type' in analyzer.data.columns else 'Unknown'
        axes[0, 0].plot(analyzer.data['x'], analyzer.data['y'], linewidth=2, label=controller)
    axes[0, 0].set_xlabel('X Position (m)')
    axes[0, 0].set_ylabel('Y Position (m)')
    axes[0, 0].set_title('Trajectory Comparison')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axis('equal')
    
    # Plot position errors
    for analyzer in analyzers:
        controller = analyzer.data['controller_type'].iloc[0] if 'controller_type' in analyzer.data.columns else 'Unknown'
        axes[0, 1].plot(analyzer.data['time'], analyzer.data['position_error'], linewidth=2, label=controller)
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Position Error (m)')
    axes[0, 1].set_title('Position Error Comparison')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot orientation errors
    for analyzer in analyzers:
        controller = analyzer.data['controller_type'].iloc[0] if 'controller_type' in analyzer.data.columns else 'Unknown'
        axes[1, 0].plot(analyzer.data['time'], abs(analyzer.data['orientation_error']), linewidth=2, label=controller)
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('Orientation Error (rad)')
    axes[1, 0].set_title('Orientation Error Comparison')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Statistics comparison
    stats_data = []
    for analyzer in analyzers:
        stats = analyzer.compute_statistics()
        stats_data.append([
            stats['controller_type'],
            f"{stats['mean_position_error']:.4f}",
            f"{stats['final_position_error']:.4f}"
        ])
    
    axes[1, 1].axis('off')
    table = axes[1, 1].table(
        cellText=stats_data,
        colLabels=['Controller', 'Mean Pos. Error (m)', 'Final Pos. Error (m)'],
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    axes[1, 1].set_title('Performance Comparison')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Comparison saved to: {output_path}")
    
    return fig


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analysis_utils.py <log_file.csv>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    analyzer = ExperimentAnalyzer(log_file)
    
    # Print statistics
    analyzer.print_statistics()
    
    # Generate report
    output_path = log_file.replace('.csv', '_report.png')
    analyzer.generate_full_report(output_path)
    
    print(f"\nAnalysis complete!")
    plt.show()
