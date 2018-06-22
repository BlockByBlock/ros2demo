from setuptools import setup

package_name = 'one_button'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    py_modules=[
        'one_button'
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
            'one_button = one_button:main'
        ],
    },
)
