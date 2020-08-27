from setuptools import setup, find_packages


setup(
    name="Idaproject",
    version='1.0',
    author="Andrey_Yurevich",
    author_email="and9019468@yandex.ru",
    install_requires=["SQLAlchemy"],
    packages=find_packages(),
    entry_points={"console_scripts": ["idaproject = console.main:main"]},
    test_suite='library.tests'
)
