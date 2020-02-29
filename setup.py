#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import hek_pool

long_desc = ""
try:
    long_desc = open("README.txt").read()
except Exception:
    print("Couldn't read readme.")

setup(
    name='hek_pool',
    #description='',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    version='%s.%s.%s' % hek_pool.__version__,
    url=hek_pool.__website__,
    author=hek_pool.__author__,
    author_email='MoeMakesStuff@gmail.com',
    license='MIT',
    packages=[
        'hek_pool',
        ],
    package_data={
        'hek_pool': [
            # TODO: Is cmd_lists properly included like this?
            'cmd_lists/*.txt', 'ogg_v1.1.2_dll_fix.zip', '*.txt',
            '*.[mM][dD]', '*.rst', '*.pyw', '*.ico', '*.png', 'msg.dat',
            ],
        },
    platforms=["POSIX", "Windows"],
    #keywords="",
    install_requires=['supyr_struct', 'threadsafe_tkinter', 'mozzarilla'],
    requires=['supyr_struct', 'threadsafe_tkinter', 'mozzarilla'],
    provides=['hek_pool'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        ],
    zip_safe=False,
    )
