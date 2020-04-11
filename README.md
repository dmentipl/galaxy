Galaxy lab
==========

N-body lab.

To set up Python for running the simulation use the `environment.yml` file. To
create a Conda environment:

```bash
conda env create --file environment.yml
```

To run the simulation, first activate the Conda environment, then run the main module.

```bash
conda activate galaxy
python galaxy/galaxy.py
```

To analyse and visualise the results open the `galaxy.ipynb` notebook in Jupter Lab.

Note: see also `plot.py` for plotting, etc.

To deactivate the environment to return to your "base" Conda environment:

```bash
conda deactivate
```
