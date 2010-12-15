from setuptools import setup

setup(
    name='varnishpurge',
    version='0.1.2',
    author='Giacomo Bagnoli',
    author_email='info@asidev.com',
    packages=['varnishpurge'],
    url='https://code.asidev.net/projects/varnishpurge',
    license='LICENSE.txt',
    description='Varnish HTTP purge library',
    long_description=open('README.txt').read(),
    install_requires = [ ],
    test_suite = 'nose.collector',
    tests_require = [ "Nose", "coverage" ],
    classifiers  = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    entry_points= {
        'console_scripts' : [
            'vpurge = varnishpurge.vpurge:main'
        ]
    }
)
