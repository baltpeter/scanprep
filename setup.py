import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scanprep",
    version="1.0.3",
    author="Benjamin Altpeter",
    author_email="hi@bn.al",
    description="Small utility to prepare scanned documents. Supports separating PDF files by separator pages and removing blank pages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baltpeter/scanprep",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['scanprep=scanprep.scanprep:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy==1.26.1',
        'pillow==10.1.0',
        'pymupdf==1.23.5',
        'pyzbar==0.1.9'
    ]
)
