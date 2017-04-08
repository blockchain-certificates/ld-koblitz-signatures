import os

from pip.req import parse_requirements
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

with open(os.path.join(here, 'README.md')) as fp:
    long_description = fp.read()

setup(
    name='ld-koblitz-signatures',
    version='0.0.2',
    url='https://github.com/blockchain-certificates/ld-koblitz-signatures',
    license='MIT',
    author='Blockchain Certificates',
    author_email='info@blockcerts.org',
    description='Blockchain certificates JSON-LD Koblitz signatures library',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs
)
