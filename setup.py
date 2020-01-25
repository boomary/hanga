from setuptools import setup, find_packages

setup(
    name='hanga',
    version='0.1',
    author='Sivadon Chaisiri',
    author_email='sivadon@ieee.org',    
    install_requires=[
        'click',
        'boto3',
    ],
    packages=['hanga'],
    include_package_data=True,   
    entry_points={
        'console_scripts': ['hanga=hanga.commands:cli']
    },
)
