from setuptools import setup, find_packages

setup(
    name="aetheris-tl",
    version="2.0.1",
    packages=find_packages(include=["aetheris_tl*"]),
    install_requires=["pyaes", "rsa"],
    extras_require={"cryptg": ["cryptg"]},
)
