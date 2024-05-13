from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='analysis_utils',
        version='1.0',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/evidencebp/analysis_utils",
        packages=find_packages(),
        install_requires=[
            'pandas',
            'psutil',
            'plotly',
            'scikit-learn',
            'cloudpickle'
            ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            ]
        )
