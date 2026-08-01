from setuptools import setup, find_packages

setup(
    name="aetheris-tl",
    version="1.0.0",
    packages=find_packages(include=["aetheris_tl*"]),
    install_requires=["pyaes", "rsa"],
    extras_require={"cryptg": ["cryptg"]},
)
