from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='mpdaemon',
    version='0.1.2',
    description='Wrapper of python-daemon for easy use.',
    long_description=long_description,
    url='https://github.com/mptnt1988/mpdaemon',
    author='Tuan Tran',
    author_email='mptnt1988@gmail.com',
    license='BSD-3-Clause',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick license
        'License :: OSI Approved :: BSD License',
        # Specify the Python versions
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    keywords='daemon development',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'python-daemon'
    ],
    entry_points={
        'console_scripts': [
            'mpdaemon = mpdaemon:main',
        ],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
)
