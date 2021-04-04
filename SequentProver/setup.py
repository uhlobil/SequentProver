from setuptools import setup

setup(
    name='MaterialInference',
    version='0.1',
    packages=['Controllers', 'Objects', 'Propositions', 'View'],
    package_dir={'': 'SequentProver'},
    url='https://github.com/LogicalExpressivism/SequentProver',
    license='',
    author='Adrian Anhalt-Gutierrez',
    author_email='adriananhaltg@gmail.com',
    description='A command line program for decomposing sequents'
)
