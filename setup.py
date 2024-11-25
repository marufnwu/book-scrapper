from setuptools import setup, find_packages

setup(
    name="book_scraper",  # The name of your package
    version="1.0.0",
    py_modules=["book_scraper"],  # List of Python modules in your package
    packages=find_packages(),  # Automatically finds packages
    install_requires=[],        entry_points={
        "console_scripts": [
            "bookscraper=book_scraper:main",  # CLI command name = module:function
        ]
    },
)
