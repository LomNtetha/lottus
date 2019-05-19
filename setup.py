import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lottus",
    version="0.0.1",
    author="Benjamim Chambule",
    author_email="benchambule@gmail.com",
    description="An ussd library that will save you time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benchambule/lottus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)