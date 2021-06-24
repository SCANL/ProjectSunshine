# IDEAL Setup and Use

Note: The following steps have been verified on a Windows 10 operating system.

A. [Prerequisites](#Prerequisites)

B. [Setup IDEAL](#Setup-IDEAL)

C. [Configure and Run IDEAL For Project](#Configure-and-Run-IDEAL-For-Project)



## Prerequisites

1. Install [Git](https://git-scm.com/download/win)
2. Install [Java JDK](https://www.oracle.com/java/technologies/javase-jdk16-downloads.html)
3. Install [Python 3.7.1](https://www.python.org/downloads/release/python-371/)
4. Install [srcML 1.0.0](https://www.srcml.org/#download)
5. Download [Stanford JARs 4.2.0](https://nlp.stanford.edu/software/tagger.shtml#Download)
6. Clone/Download [IDEAL repository 1.0.0](https://github.com/SCANL/ProjectSunshine/releases)

## Setup IDEAL

1. Install virtual environment: `py -m pip install      --user virtualenv`

   <img src="images\setup\virtualenv_install.png" style="zoom:40%;" />

2. Create virtual environment: `py -m venv venv`

   <img src="images\setup\virtualenv_create.png"  style="zoom:40%;" />

3. Activate virtual environment: `.\venv\Scripts\activate`

   <img src="images\setup\virtualenv_activate.png"  style="zoom:40%;" />

4. Install packages from requirements files: `py -m pip install      -r requirements.txt`

   <img src="images\setup\package_install.png"  style="zoom:40%;" />

5. Download NLTK data. Enter the following commands:
    1. `python`
	2. `import nltk`
	3. `nltk.download('wordnet')`
	4. `nltk.download('punkt')`
	5. `quit()`

   <img src="images\setup\nltk_download.png"  style="zoom:40%;" />

6. Update all paths in config file: **src\common\config.txt**	

   <img src="images\setup\config_file.png"  style="zoom:40%;" />

## Configure and Run IDEAL For Project

1. Update all paths in the run command file: **src\apps\IDEAL\run.cmd**

   <img src="images\setup\cmd_file.png"  style="zoom:40%;" />

2. Update all paths in the project config file: **src\apps\IDEAL\project1.config**

   <img src="images\setup\projectconfig_file.png"  style="zoom:40%;" />

3. Create input.csv file and add paths to the source code files/directories

   <img src="images\setup\input_file.png"  style="zoom:40%;" />

4. Run the run.cmd file

   <img src="images\setup\cmd_run.png"  style="zoom:40%;" />

5. Results saved in IDEAL_Results.csv file

   <img src="images\setup\results.png"  style="zoom:40%;" />


##### [Back To ReadMe](../README.md)
