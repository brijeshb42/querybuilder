from setuptools import setup, find_packages

setup(
    name='querybuilder',
    version='0.1.0',
    include_package_data=True,
    packages=find_packages(),
    description=(
        'A library to build human '
        'readable SQL query string using a pythonic API'),
    # long_description=open("README.md").read(),
    author='Brijesh Bittu',
    author_email='brijeshb42@gmail.com',
    url='https://github.com/brijeshb42/querybuilder',
    download_url='https://github.com/brijeshb42/querybuilder/tarball/0.1.0',
    keywords=['SQL', 'peewee', 'querybuilder'],
    license='http://www.opensource.org/licenses/mit-license.php',
    classifiers=[],
    test_suite='tests',
    extras_require={
        'peewee': ['peewee']
    }
)
