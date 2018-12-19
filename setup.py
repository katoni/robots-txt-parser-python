import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robots-txt-parser",
    version="1.0.1",
    author='Philip Semanchuk',
    author_email='philip@pyspoken.com',
    maintainer="Martin Skovvang Petersen",
    maintainer_email="martin@katoni.dk",
    description="A Robot Exclusion Rules Parser for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/katoni/robotexclusionrulesparser",
    license='BSD',
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)