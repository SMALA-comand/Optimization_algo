import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="optimizationalgo",
    packages=['optimizationalgo'],
    version="0.0.4",
    description='Optimization algorithms for the traveling salesman problem',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Kozlov",
    author_email="mark.k.2012@yandex.ru",
    url="https://github.com/SMALA-comand/Optimization_algo",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
