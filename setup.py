"""Setup script for `tridentine_calendar`."""

from setuptools import setup

with open('README.md') as fp:
    long_description=fp.read()

setup(
    name='tridentine_calendar',
    version='0.7.0',
    description='Liturgical calendar calculator using the 1962 Roman Catholic '
                'rubrics.',
    long_description=long_description,
    url='https://github.com/joe-antognini/tridentine_calendar',
    author='Joseph O\'Brien Antognini',
    author_email='joe.antognini@gmail.com',
    license='MIT',
    packages=['tridentine_calendar'],
    install_requires=[
        'icalendar',
    ],
    entry_points={
        'console_scripts':
            ['tridentine_calendar=tridentine_calendar.cli:main'],
    },
    include_package_data=True,
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    python_requires='>=3.6',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Religion',
        'Natural Language :: English',
        'Topic :: Religion',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
