import sys

from setuptools import setup

version = __import__('yaff').__version__


if sys.hexversion < 0x02070000:
    EXTRA_INSTALL_REQUIRES = ['backport_collections']
else:
    EXTRA_INSTALL_REQUIRES = []

setup(
    name='yaff',
    version=version,
    description='Yet Another Faield Framework',
    author='Francesco Pischedda',
    author_email='francesco.pischedda@gmail.com',
    url='https://github.com/fpischedda/yaff',
    packages=('yaff',
              'yaff.conf',
              'yaff.animation',
              'yaff.animation.loaders',
              'yaff.utils',
              'yaff.contrib',
              'yaff.contrib.mixins',
              'yaff.contrib.scenes'),
    package_data={
    },
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'pyglet',
    ] + EXTRA_INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: Alpha/Unstable',
        'Environment :: Gaming',
        'Framework :: pyglet',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
