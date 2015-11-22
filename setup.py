from setuptools import setup, find_packages

setup(
        name='advanced-counter',
        version='1.0',
        description='Advanced statistics for text files',
        author='Andrea Rosa',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'stevedore',
            'pytest',
            'regex',
            'mock'
            ],
        entry_points={
            'advcounter.plugin': [
                'stattext = castel.drivers.stattext:Stattext',
                ],

            },
        )
