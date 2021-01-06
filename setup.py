import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yaproxy",
    version="0.0.1",
    author="Lin Xiao Hui",
    author_email="llinxiaohui@126.com",
    description="Yet Another Proxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linxiaohui/yaproxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)