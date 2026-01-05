from setuptools import setup, find_packages

package_name = 'robot_simulation'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/experiment.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robot Control Team',
    maintainer_email='user@example.com',
    description='Differential drive robot simulation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'diff_drive_sim = robot_simulation.diff_drive_sim:main',
        ],
    },
)
