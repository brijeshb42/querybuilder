from setuptools import setup, find_packages

description = (
    'A library to build human '
    'readable SQL query string using a pythonic API'),
long_desc = description
with open("README.rst") as f:
    long_desc = f.read()

setup(
    name='querybuilder',
    version='0.1.2',
    include_package_data=True,
    packages=find_packages(),
    description=description,
    long_description=long_desc,
    author='Brijesh Bittu',
    author_email='brijeshb42@gmail.com',
    url='https://github.com/brijeshb42/querybuilder',
    download_url='https://github.com/brijeshb42/querybuilder/tarball/0.1.2',
    keywords=['SQL', 'peewee', 'querybuilder'],
    license='http://www.opensource.org/licenses/mit-license.php',
    classifiers=[],
    test_suite='tests',
    extras_require={
        'peewee': ['peewee']
    }
)
