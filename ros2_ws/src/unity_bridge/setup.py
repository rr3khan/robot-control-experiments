from setuptools import setup, find_packages

package_name = 'unity_bridge'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robot Control Team',
    maintainer_email='user@example.com',
    description='ROS 2 bridge for Unity communication',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tcp_bridge = unity_bridge.tcp_bridge:main',
        ],
    },
)
