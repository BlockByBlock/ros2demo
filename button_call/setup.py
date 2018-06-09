from setuptools import setup

setup(
    name='button_call',
    version='0.0.0',
    packages=[],
    py_modules=['button_call'],
    install_requires=['setuptools'],
    author='BlockByBlock',
    author_email='ybingcheng@gmail.com',
    description='Button call in ROS2',
    license='TODO',
    test_suite='test',
    entry_points={
        'console_scripts': [
            'button_call = button_call:main',
        ],
    },
)