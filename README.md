# AI-Captain

Run every command from the project directory.

### Create and activate conda environment:

    conda env create -f environment.yml
    source activate aicaptain
    
### Start the simulator / controller:

    python start.py
    
### Start jupyter notebook:

    jupyter notebook notebooks
    
### To update dependancies of an existing conda environment run:

    conda env update -f environment.yml 

## Using your own steering strategies
You can change the `src/boats/my_boat/my_strategy.py` file to develop your own steering strategy. 

## Adding boats
If you want to add more boats to the simulator or the race you can add them in the config file:
 
Copy the `config_default.py` to `config.py` and edit the file.