from setuptools import setup, find_packages

# Used for installing test dependencies directly
tests_require = [
    'nose',
    'mock'
]

setup(
    name='pickle_jar',
    version='1.0.0',
    description="Pickle Jar",
    author="Sam Hollenbach",
    author_email="shollenbach@axiomexergy.com",
    packages=find_packages(exclude=['test', 'test_*', 'fixtures']),
    package_data={
        'pickle_jar': []
    },
    install_requires=[
        'hashlib',
    ],
    test_suite='nose.collector',
    tests_require=tests_require,
    # For installing test dependencies directly
    extras_require={'test': tests_require},
)
