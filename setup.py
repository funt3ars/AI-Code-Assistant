from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devin_integration",
    version="0.1.0",
    author="funt3ars",
    author_email="your.email@example.com",
    description="A package for integrating Devin-like AI capabilities into your projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/funt3ars/devin_integration",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=8.0.0",
        "pytest-asyncio>=0.23.5",
        "pytest-cov>=6.1.0",
        "openai>=1.59.8",
        "anthropic>=0.42.0",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.11.12",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "mypy>=0.900",
            "flake8>=3.9.0",
        ]
    }
) 