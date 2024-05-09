# coding: utf-8

from distutils.core import setup

setup(
    name='XXHelper',
    version='0.0.1',
    description='Gpt powered subtitle translation tool.',
    author='Seeker472',
    author_email='gmx472@qq.com',
    url='https://seekerer.com',
    packages=['XXHelper'],
    entry_points={
        'console_scripts': [
            'XXHelper = XXHelper.XXHelper:main',
        ],
    },
    install_requires=[
        'Appium_Python_Client == 4.0.0',
        'numpy == 1.26.4',
        'openai == 1.25.2',
        'opencv_contrib_python == 4.6.0.66',
        'opencv_python == 4.6.0.66',
        'opencv_python_headless == 4.9.0.80',
        'oss2 == 2.18.5',
        'paddleocr == 2.7.3',
        'paddlepaddle == 2.6.1',
        'Requests == 2.31.0',
        'selenium == 4.20.0',
        'thefuzz == 0.22.1',
    ],
)
