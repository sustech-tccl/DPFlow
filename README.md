# DPFlow - A workflow to generate deep potential force field
---------

DPFlow is a code to:  
(1) Optimize neural network force field  
(2) Analyze CP2K and LAMMPS trajectory  

The code is mainly written in Python and Fortran.  

Email: lujunbo15@gmail.com
  
# Installation for DPFlow

* Prerequisites
   - Python 3.5 or higher
   - Numpy 1.8.0 or higher
   - psutil

   Suggestion: as we will use deepmd-kit software, we recommend users could install deepmd-kit  
   at first. Then add the environmental variable of deepmd-kit. It will include python and numpy.  
   Then intall psutil by using pip3 in deepmd-kit/bin directory:  
   pip3 install psutil  

* Install GNU parallel

    Download GNU parallel source code from https://www.gnu.org/software/parallel/  
    tar -jxvf parallel-latest.tar.bz2  
    cd parallel-latest  
    ./configure --prefix=parallel_install_path  
    make  
    make install  

* Compile core module
  
    git clone https://github.com/JunboLu/DPFlow.git  
    !Caution: When downloading DPFlow through zip version, please change the name "DPFlow-main"  
    to "DPFlow" after you unzip it.  
    cd DPFlow_directory/lib  
    change directory of f2py in Makefile  
    !Caution: If your gcc version is low, f2py cannot compile core code successfully, please update your  
    gcc up to 6.3.  
    make  

* Environmental variable

    export PYTHONPATH=../DPFlow_directory:$PYTHONPATH  
    change python_exe and DPFlow directory in DPFlow_directory/bin/DPFlow file  
    export PATH=DPFlow_directory/bin:$PATH  

# How to use 
* DPFlow is an user-friendly code.  

  The input files are in example directory.  
  Users just need to run:  
  DPFlow input.inp  
