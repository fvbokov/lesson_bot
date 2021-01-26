from setuptools import setup, find_packages

install_requires = [
    "discord.py",
    "sortedcontainers"
]

setup(
    name="lesson-bot",
    version="1.0",
    description="",
    install_requires=install_requires,
    packages=find_packages(),
)
