import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='OneEuroFilter',  
     version='0.2.0',
     author="Géry Casiez",
     author_email="gery.casiez@gmail.com",
     description="1€ filter (One Euro Filter)",
     long_description=long_description,

     long_description_content_type="text/markdown",
     url="https://github.com/casiez/OneEuroFilter/python",
     packages=setuptools.find_packages(),

     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: BSD License"
     ],

 )