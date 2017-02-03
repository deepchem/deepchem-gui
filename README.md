# DeepChem GUI

This library implements a web based GUI to [DeepChem](https://github.com/deepchem/deepchem).
As of present, it can be used to predict docking of ligands to proteins using DeepChem models pretrained on [PDBBind](http://www.pdbbind-cn.org/).
The GUI heavily relies on the molecular visualization library [NGL](https://github.com/arose/ngl), and is modeled after its [demo web application](http://proteinformatics.charite.de/ngl/html/ngl.html).

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

2. Install Flask:
    In the Anaconda environment you created in the previous step to install DeepChem, execute-
    ```bash
    pip install Flask
    ```

3. Clone the `deepchem-gui` github repo:
   ```bash
   git clone https://github.com/deepchem/deepchem-gui.git
   ```

## Usage

1. Launch the web application: <br/> At present, the only way to access the GUI is to run the server on your local machine.
   In the Anaconda environment with DeepChem installed, `cd` into the `deepchem-gui` directory and execute-
    ```bash
    export FLASK_APP=deepchem-gui.py
 
    flask run
    ```
2. Navigate to http://127.0.0.1:5000/ in your browser to open the application.

3. Select ligand files and protein files using the file selection tool in Dock tab. At present, the only supported format for ligand files is .sdf and for protein files is .pdb

4. Docking takes approx. 5 minutes, following which the predicted scores are tabulated in the browser for all possible ligand and protein pairs. Clicking on a row loads the structures of the corresponding ligand and protein.

5. Update the molecular visualizations using the options in the right panel as specified in [these instructions](http://proteinformatics.charite.de/ngl/doc/index.html#User_manual/Usage/Molecular_representations).

Note: This repository is under active development so bugs and surprises are likely. Kindly raise an issue on GitHub if you run into problems and we will try and resolve it asap. Alternatively you can also contribute to the repository by following [these guidelines](https://github.com/deepchem/deepchem#contributing-to-deepchem). Client side issues can be inspected using the JavaScript console of the browser while server side errors will be displayed in the shell. 

## DeepChem Publications
1. [Computational Modeling of β-secretase 1 (BACE-1) Inhibitors using
Ligand Based
Approaches](http://pubs.acs.org/doi/abs/10.1021/acs.jcim.6b00290)
1. [Low Data Drug Discovery with One-shot Learning](https://arxiv.org/abs/1611.03199)

## About Us
DeepChem is a package by the [Pande group](https://pande.stanford.edu/) at Stanford. DeepChem was originally created by [Bharath Ramsundar](http://rbharath.github.io/), and has grown through the contributions of a number of undergraduate, graduate, and postdoctoral researchers working with the Pande lab.
