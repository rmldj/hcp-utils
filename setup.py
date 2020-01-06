import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hcp_utils",
    version="0.1.0",
    author="Romuald A. Janik",
    author_email="romuald.janik@gmail.com",
    description="A set of utilities for working with HCP-style fMRI data with nilearn.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmldj/hcp-utils",
    packages=['hcp_utils'],
    package_data={'hcp_utils': ['data/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False
)
