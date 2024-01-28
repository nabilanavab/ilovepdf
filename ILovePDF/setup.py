# This module is part of https://github.com/nabilanavab/ilovepdf
# Feel free to use and contribute to this project. Your contributions are welcome!
# copyright ©️ 2021 nabilanavab

file_name = "ILovePDF/setup.py"

from setuptools import setup, find_packages

setup(
    name="nabilanavab/ilovepdf",
    version="5.0.1",
    description="Telegram PDF Bot",
    author="Nabil A Navab",
    author_email="nabil.a.navab@gmail.com",
    url="https://github.com/nabilanavab/ilovepdf",
    packages=find_packages(),
    install_requires=[
        "pyrogram==2.0.106",
        "TgCrypto==1.2.3",
        "pillow==9.5.0",
        "PyMuPdf==1.22.2",
        "PyPDF2==3.0.1",
        "convertapi==1.6.0",
        "pyromod==2.0.0",
        "fpdf==1.7.2",
        "ocrmypdf==14.1.0",
        "motor==3.1.2",
        "psutil==5.9.5",
        "pymongo[srv]==4.2.0",
        "hachoir==3.2.0",
        "pytelegrambotapi==4.11.0",
        "aiohttp==3.8.4",
        "aspose-words==23.4.0",
        "pdfkit==1.0.0",
        "beautifulsoup4==4.12.2",
        "requests==2.30.0",
        "libgenesis==0.1.9",
    ],
    entry_points={"console_scripts": ["ilovepdf=ilovepdf.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# If you have any questions or suggestions, please feel free to reach out.
# Together, we can make this project even better, Happy coding!  XD
