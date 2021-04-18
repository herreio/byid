import os
import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.md')).read()

setuptools.setup(
    name="doi",
    version="2021.4.19",
    author="Donatus Herre",
    author_email="pypi@herre.io",
    license="MIT",
    description="DOI-based Data Retrieval",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/herreio/doi",
    project_urls={
        "Bug Tracker": "https://github.com/herreio/doi/issues",
    },
    package_dir={"doi": "doi"},
    packages=["doi"],
    python_requires=">=3.6",
    install_requires=["requests", "tqdm", "ijson"],
    entry_points={
      'console_scripts': [
        'DOI = doi.__main__:main',
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
