from setuptools import setup, find_packages

setup(
    name="lxmfy-translate-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "lxmfy>=0.7.1,<0.8.0",
        "argostranslate>=1.9.6,<2.0.0",
    ],
    setup_requires=[
        "setuptools>=42",
        "wheel",
        "cmake>=3.5",
        "ninja"
    ],
    entry_points={
        'console_scripts': [
            'translate-bot=lxmfy_translate_bot.bot:main',
        ],
    },
    author="LXMFy",
    author_email="team@quad4.io",
    description="A translation bot using LXMFy and Argos Translate",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LXMFy/translate-bot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
) 