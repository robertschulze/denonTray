#!/usr/bin/env python3
# encoding: utf-8
"""System tray remote-control tool for Denon AVR receivers."""
from setuptools import find_packages, setup

setup(name='denontray',
      version='0.1',
      description='System tray remote-control tool for Denon AVR receivers',
      long_description=
      'System tray remote-control tool for Denon AVR receivers',
      url='https://github.com/robertschulze/denonTray',
      author='Robert Schulze',
      author_email='robert@guitaronline.de',
      license='MIT',
      packages=find_packages(),
      install_requires=['denonavr', 'infi.systray', 'pyyaml', 'infi'],
      tests_require=['tox'],
      platforms=['any'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries",
          "Topic :: Home Automation",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
      ])
