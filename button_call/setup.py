from setuptools import setup

package_name = 'button_call'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    py_modules=['button_call'],
    install_requires=['setuptools'],
    author='bingcheng',
    author_email='ybingcheng@gmail.com',
    description='Button call in ROS2',
    license='TODO',
    test_require=['pytest'],
    entry_points={
        'console_scripts': [
            'button_call = button_call:main',
        ],
    },
)