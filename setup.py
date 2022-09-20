from setuptools import setup,find_packages
from typing import List

#Declaring variables for setup functions
PROJECT_NAME="BACK_ORDER_PREDICTOR"
VERSION="0.0.1"
AUTHOR="Ashish Shukla"
DESRCIPTION="Predicting order went on backorder "

REQUIREMENT_FILE_NAME="requirements.txt"

E_DOT = "-e ."


def get_requirements_list() -> List[str]:
    """
    Description: This function is going to return list of requirement
    mention in requirements.txt file

    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if E_DOT in requirement_list:
            requirement_list.remove(E_DOT)
        return requirement_list



setup(
name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESRCIPTION,
packages=find_packages(), 
install_requires=get_requirements_list()
)

