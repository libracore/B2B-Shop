# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re, ast

# get version from __version__ variable in b2bshop/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('b2bshop/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

setup(
	name='b2bshop',
	version=version,
	description='ERPNext App for easy web orders',
	author='libracore',
	author_email='info@libracore.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.req) for ir in requirements],
	dependency_links=[str(ir._link) for ir in requirements if ir._link]
)
