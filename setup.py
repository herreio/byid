import os
import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(ROOT, 'README.md')).read()

setuptools.setup(
    name="byid",
    version="2021.4.23",
    author="Donatus Herre",
    author_email="pypi@herre.io",
    license="MIT",
    description="Fetch metadata records by identifier.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/herreio/byid",
    project_urls={
        "Bug Tracker": "https://github.com/herreio/byid/issues",
    },
    package_dir={"byid": "byid"},
    packages=["byid"],
    python_requires=">=3.6",
    install_requires=["requests", "tqdm", "ijson", "xmltodict"],
    entry_points={
      'console_scripts': [
        'DOI = byid.doi.__main__:main',
        'DOI-RA = byid.doi.__main__:main_ra',
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
