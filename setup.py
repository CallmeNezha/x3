import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyx3",
    version="0.0.1",
    author="ZIJIAN JIANG",
    author_email="jiangzijian77@gmail.com",
    description="x3 is a d3-like xml selector, mapper, operator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CallmeNezha/x3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lxml>=4.2.1",
        "typing>=3.6.6"
    ]
)