"""
Plot Trajectory Script

Quick script to plot robot trajectory from experiment log.
"""

import sys
import matplotlib.pyplot as plt
from analysis_utils import ExperimentAnalyzer


def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_trajectory.py <log_file.csv>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    # Create analyzer
    analyzer = ExperimentAnalyzer(log_file)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    analyzer.plot_trajectory(ax)
    
    # Save and show
    output_path = log_file.replace('.csv', '_trajectory.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Trajectory plot saved to: {output_path}")
    
    plt.show()


if __name__ == '__main__':
    main()
