import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="holidays-flights-amiterez",
    version="1.0",
    author="amit erez",
    author_email="amiterez8@gmail.com",
    description="scan and find cheap flights during school vacations.",
    long_description=long_description,
    long_description_content_type="",
    url="https://github.com/amiterez/holidays-flights",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)