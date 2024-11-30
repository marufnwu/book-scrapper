from pkg_resources import parse_requirements
from setuptools import setup, find_packages

    
setup(
    name="book_scraper",
    version="1.0.1",
    python_requires='>3.5.2',
    py_modules=["main"],
    packages=find_packages(),
    install_requires=[
        
    ],  
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "bookscraper=main:main",  # CLI command
        ]
    },
)
