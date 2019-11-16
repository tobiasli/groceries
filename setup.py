import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='tregex-tobiasli',
                 version='1.0.2',
                 description='Wrapper for more functionality out of regex parse results.',
                 author='Tobias Litherland',
                 author_email='tobiaslland@gmail.com',
                 url='https://github.com/tobiasli/tregex',
                 packages=setuptools.find_packages(),
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 )
