import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OMIEData",
    version="0.1.0.1",
    author="Alberto Cruz and Mirel Mora",
    author_email="a.cruz.garcia@gmail.com, mirel.mora@gmail.com",
    description="Package to download electricity time series from https://www.omie.es/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acruzgarcia/OMIEData",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    keywords=['OMIE', 'Electricity prices'],
    install_requires=['pandas', 'requests', 'datetime']
)
