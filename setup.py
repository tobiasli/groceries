import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='groceries-tobiasli',
                 version='1.1.1',
                 description='Module for parsing shopping lists and dinner menus and compiling shopping lists.',
                 author='Tobias Litherland',
                 author_email='tobiaslland@gmail.com',
                 url='https://github.com/tobiasli/groceries',
                 packages=['groceries/config',
                           'groceries/config/constants',
                           'groceries/config/languages',
                           'groceries/config/menu_format',
                           'groceries/config/settings',
                           'groceries/config/unit_definition',
                           'test'],
                 package_data={'': ['groceries/test/bin/cookbook.yaml']},
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 install_requires=['tregex-tobiasli', 'numpy', 'pytest', 'pyyaml'],
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 )
