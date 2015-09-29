import sys
from setuptools import setup

install_requires = [
    'clint>=0.5.1',
    'mysqlclient>=1.3.6',
    'psycopg2>=2.4.2',
    'pytz',
    'pyyaml>=3.10.0',
]

setup(
    name='py-mysql2pgsql',
    version='0.1.8',
    description='Tool for migrating/converting from mysql to postgresql.',
    long_description=open('README.rst').read(),
    license='MIT License',
    author='Philip Southam',
    author_email='philipsoutham@gmail.com',
    url='https://github.com/philipsoutham/py-mysql2pgsql',
    zip_safe=False,
    packages=['mysql2pgsql', 'mysql2pgsql.lib'],
    entry_points={
        'console_scripts': [
            'py-mysql2pgsql = mysql2pgsql.mysql2pgsql:main',
        ],
    },
    platforms='any',
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Utilities'
        ],
    keywords = 'mysql postgres postgresql pgsql psql migration',
    )
