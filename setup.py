import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='groceries-tobiasli',
                 version='1.1.0',
                 description='Module for parsing shopping lists and dinner menus and compiling shopping lists.',
                 author='Tobias Litherland',
                 author_email='tobiaslland@gmail.com',
                 url='https://github.com/tobiasli/groceries',
                 packages=setuptools.find_packages(),
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
