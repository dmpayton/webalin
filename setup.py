import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='webalin',
    version='0.1.0-dev',
    description='Web Accessibility Linter',
    license='MIT',
    url='https://github.com/dmpayton/webalin',
    author='Derek Payton',
    author_email='derek.payton@gmail.com',
    py_modules=['webalin'],
    scripts=['webalin'],
    install_requires=['lxml', 'requests'],
    classifiers = (
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ),
)
