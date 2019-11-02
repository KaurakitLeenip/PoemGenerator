
from setuptools import find_packages
from setuptools import setup

setup(
    name="PoemGenerator",
    version="0.0.1",
    url="kaurakitleenip.me",
    license="BSD",
    maintainer="kaurakitleenip",
    maintainer_email="kaurakit@gmail.com",
    description="The basic blog app built in the Flask tutorial.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"]
)