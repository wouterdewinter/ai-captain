Create and activate conda environment

    conda env create -f environment.yml
    source activate aicaptain
    
Start the simulator / controller

    python start.py
    
Start jupyter notebook

    cd notebooks
    jupyter notebook
    
To update dependancies of an existing conda environment run

    conda env update -f environment.yml 
