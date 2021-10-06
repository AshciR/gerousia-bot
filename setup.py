from setuptools import setup, find_packages

setup(
    name="gerousiabot",
    version="0.0.1",
    author="Gerousia",
    author_email="alrickabg@gmail.com",
    url="https://github.com/AshciR/gerousia-bot",
    description="A Telegram bot that inform members of the Gerousia chat group which members are online in their Discord server!",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    entry_points={"console_scripts": ["gerousiabot = gerousiabot.main:main"]},
)