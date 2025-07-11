from setuptools import setup, find_packages

setup(
    name="favn",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "tk",
    ],
    entry_points={
        "console_scripts": [
            "favn-gui=favn.run_gui:main"
        ],
    },
    author="С. В. Генералов",
    description="Калькулятор титров по методу Рида и Менча",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/svgen83/favn ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
