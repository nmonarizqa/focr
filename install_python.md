# Installing Python and Required Libraries on a Windows Computer

## 1. Install Miniconda
Miniconda contains python and conda package manager. Download [here](https://conda.io/miniconda.html) and choose an installer for Python2.7 that suitable for your machine (32 or 64 bit)
Once donwloaded, run the installer.

## 2. Install all required packages
- Install directly via pip

Type "Anaconda Prompt" on the search bar and choose the Anaconda Prompt app.
Try type 
```
pip install numpy scipy matplotlib pandas statsmodel sklearn jupyter
``` 
and hit enter to install packages commonly used for data processing.
If failed, try
```
pip install --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org  numpy scipy matplotlib pandas statsmodel sklearn jupyter
```
to bypass some network securities.

- install geopandas and geo related packages via conda
In Anaconda prompt, type
```
conda install -c conda-forge GDAL
```
Followed by
```
conda install -c conda-forge geopandas
```
