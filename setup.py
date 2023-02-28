from setuptools import setup

setup(
    name='division_to_csv',
    include_package_data=True,
    version='1.0',
    py_modules=['divisions', 'namely', 'namely_profile_extract'],
    install_requires=[
        'click', 'keyring', 'requests', 'pycurl', 'certifi'
    ],
    entry_points='''
        [console_scripts]
        namely_profile_extract=namely_profile_extract:cli
    ''',
)
