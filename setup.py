"""
Installs Pelican Plugins in an easy way
"""
from setuptools import find_packages, setup

dependencies = ['click']
test_dependencies = ['pytest', 'pytest-runner', 'pytest-mock']

setup(
    name='pelican-plugin-installer',
    version='0.0.2',
    url='https://github.com/kplaube/pelican-plugin-installer',
    license='GPL3',
    author='Klaus Laube',
    author_email='kplaube@gmail.com',
    description='Installs Pelican Plugins in an easy way',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    tests_require=test_dependencies,
    entry_points={
        'console_scripts': [
            'pelican-plugin-installer = pelican_plugin_installer.cli:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
