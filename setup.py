from setuptools import setup

setup(
    name='division_to_csv',
    include_package_data=True,
    version='1.0',
    py_modules=['division_to_csv', 'divisions', 'namely'],
    install_requires=[
        'click', 'keyring', 'requests'
    ],
    entry_points='''
        [console_scripts]
        division_to_csv=division_to_csv:cli
    ''',
)
