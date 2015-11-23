from setuptools import setup
import os

version = "0.9.0"


def write_version():
    with open(os.path.join("configoverloader", "version.py"), 'w') as fp:
        fp.write("version='{VERSION}'".format(VERSION=version))


write_version()
readme = open('README.rst').read()

setup(
    name="configoverloader",
    version=version,
    author="yokoshin",
    author_email=os.environ.get('CONFIGOVERLOADER_EMAIL'),
    url='https://bitbucket.org/yokoshin/configoverloader',
    description='this help overloading config files depends on env, role, node',
    long_description=readme,
    packages=['configoverloader', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
