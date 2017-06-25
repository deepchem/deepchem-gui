# DeepChem GUI

This library implements a web based GUI to [DeepChem](https://github.com/deepchem/deepchem).
As of present, it can be used to predict docking of ligands to proteins using DeepChem models pretrained on [PDBBind](http://www.pdbbind-cn.org/).
The GUI heavily relies on the molecular visualization library [NGL](https://github.com/arose/ngl) and the Chemoinformatics library [Kekule.js](http://partridgejiang.github.io/Kekule.js/).

### Table of contents:

* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Contributing to DeepChem](#contributing-to-deepchem)
* [DeepChem Publications](#deepchem-publications)
* [About Us](#about-us)

## Requirements
* [DeepChem](https://github.com/deepchem/deepchem)
* [NGL](https://github.com/arose/ngl)
* [Flask](http://flask.pocoo.org/)

## Installation

Installation from source is the only currently supported format.

1. Install DeepChem using the [instructions here](https://github.com/deepchem/deepchem).

1. Install Flask:
    In the Anaconda environment you created in the previous step to install DeepChem, execute-
    ```bash
    conda install flask
    ```

1. Clone the `deepchem-gui` github repo:
   ```bash
   git clone https://github.com/deepchem/deepchem-gui.git && cd deepchem-gui
   ```

1. Install `deepchem-gui`:
   ```bash
   python setup.py install
   ```


## Usage

1. Ensure that the Anaconda environment is activated, e.g.:
    ```source activate deepchem
    ```
1. In the Anaconda environment with `deepchem-gui` installed, execute:
    ```bash
    deepchem-gui server
    ```
   This should open your default browser and launch the application at
   http://127.0.0.1:5000/. Use the `-h` flag to reveal a full list of options.

    Note that if you have installed the software on a remote server, you may wish to open an SSH tunnel to port 5000. This can be done via the -L flag, e.g. ssh -L 5000:localhost:5000 user@servername

1. Docking: Select ligand files and protein files using the file selection tool in Dock tab. At present, the only supported format for ligand files is .sdf and for protein files is .pdb. Docking takes approx. 5 minutes, following which the predicted scores are tabulated in the browser for all possible ligand and protein pairs. Clicking on a row loads the structures of the corresponding ligand and protein. Update the molecular visualizations using the options in the right panel as specified in [these instructions](http://proteinformatics.charite.de/ngl/doc/index.html#User_manual/Usage/Molecular_representations). An example protein that you may wish to try docking is 14HR.pdb, which is encoded by NF2 tumor suppressor gene. You can download such a PDB file from a PDB database query, e.g., via a query such as to: http://www.ebi.ac.uk/pdbe/entry/search/index?all_molecule_names:Merlin
1. Molecule editing: Clicking on the "Molecule Editor" option opens a [Kekule.js](http://partridgejiang.github.io/Kekule.js/) molecule editor. Instructions to use the editor are available [here](http://partridgejiang.github.io/Kekule.js/documents/tutorial/content/composer.html).
1. Reaction visualization: Visualize SMILES strings and Reaction SMARTS stored in a CSV format using the respective tabs under "Visualize".

Note: This repository is under active development so bugs and surprises are likely. Kindly raise an issue on GitHub if you run into problems and we will try and resolve it asap. Alternatively you can also contribute to the repository by following [these guidelines](https://github.com/deepchem/deepchem#contributing-to-deepchem). Client side issues can be inspected using the JavaScript console of the browser while server side errors will be displayed in the shell.

## DeepChem Publications
1. [Computational Modeling of β-secretase 1 (BACE-1) Inhibitors using
Ligand Based
Approaches](http://pubs.acs.org/doi/abs/10.1021/acs.jcim.6b00290)
1. [Low Data Drug Discovery with One-shot Learning](https://arxiv.org/abs/1611.03199)

## About Us
DeepChem is a package by the [Pande group](https://pande.stanford.edu/) at Stanford. DeepChem was originally created by [Bharath Ramsundar](http://rbharath.github.io/), and has grown through the contributions of a number of undergraduate, graduate, and postdoctoral researchers working with the Pande lab.
