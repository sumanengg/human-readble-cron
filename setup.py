from setuptools import setup, find_packages

setup(
    name="human-readable-cron",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "human-readable-cron=human_readable_cron.cli:main",
        ],
    },
    description="Convert human-readable cron expressions to standard cron format.",
    author="Sumanta Ghosh",
    author_email="sumanengg.sg@gmail.com",
    license="MIT",
    url="https://github.com/sumanengg/human-readable-cron",
)