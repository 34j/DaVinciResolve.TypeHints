from setuptools import setup, find_packages

setup(
    name="drtypehints",
    version='0.1.0',
    description="Generate type hints for Lua from references",
    author="34j",
    url="https://github.com/34j/DaVinciResolve.TypeHints",
    packages=find_packages(),
    install_requires=['click', 'humps'],
    license='MIT License',
    entry_points={
        "console_scripts": [
            "drtypehints = drtypehints.__main__:generate_file",
        ],
    }
)