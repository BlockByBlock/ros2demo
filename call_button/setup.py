from setuptools import setup

package_name = 'call_button'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    py_modules=[
        'call_button_test',
        'call_button_keyboard'
        ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    author='Morgan Quigley',
    author_email='morgan@osrfoundation.org',
    maintainer='Morgan Quigley',
    maintainer_email='morgan@osrfoundation.org',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Call button ROS 2 driver',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'call_button_test = call_button_test:main',
            'call_button_keyboard = call_button_keyboard:main'
        ],
    },
)
