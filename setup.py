from setuptools import setup
import os

version = "0.1.0"


def write_version():
    with open(os.path.join("configoverload", "version.py"), 'w') as fp:
        fp.write("version='{VERSION}'".format(VERSION=version))


write_version()

setup(
    name="configoverload",
    version="version",
    author="shinsuke.yokoyama",
    author_email='',
    description='help overload config files depends on env, role, node',
    packages=['configoverload', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
