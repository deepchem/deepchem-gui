import os
from flask import Flask, url_for, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import deepchem as dc
import subprocess
from shutil import copyfile
import csv
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static/')
DEEPCHEM_GUI = Flask('deepchem-gui', static_folder=STATIC_DIR,
                     static_url_path='/static',
                     template_folder=os.path.join(STATIC_DIR, 'deepchem-gui',
                                                  'templates')
                    )

UPLOAD_DIR = os.path.join(STATIC_DIR, "data/")
if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)
    print("Created data directory")

# serve ngl webapp clone
@DEEPCHEM_GUI.route('/')
def webapp():
    return render_template('webapp.html')

# download protein and ligand files
@DEEPCHEM_GUI.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        proteins = request.files.getlist('proteins')
        ligands = request.files.getlist('ligands')
        smiles = request.files.getlist('smiles')
        smarts = request.files.getlist('smarts')

        if proteins and ligands:

            protein_fns = []
            ligand_fns = []

            for protein in proteins:
                protein_fn = os.path.join(
                    UPLOAD_DIR,
                    secure_filename(protein.filename)
                    )
                protein.save(protein_fn)
                protein_fns.append(protein_fn)

            for ligand in ligands:
                ligand_fn = os.path.join(
                    UPLOAD_DIR,
                    secure_filename(ligand.filename)
                    )
                ligand.save(ligand_fn)
                ligand_fns.append(ligand_fn)

            docking_result = dock(protein_fns, ligand_fns)
            print(docking_result)

            for i in range(len(protein_fns)):
                for j in range(len(ligand_fns)):

                    protein_fn = docking_result[i][j]["protein"]
                    new_protein_fn = protein_fn.split("/")[-1]
                    copyfile(protein_fn, os.path.join(
                        UPLOAD_DIR, new_protein_fn))
                    docking_result[i][j]["protein"] = url_for(
                        'static', filename="data/" + new_protein_fn)

                    ligand_fn = docking_result[i][j]["ligand"]
                    new_ligand_fn = ligand_fn.split("/")[-1]
                    copyfile(ligand_fn,
                             os.path.join(UPLOAD_DIR, new_ligand_fn))
                    docking_result[i][j]["ligand"] = url_for(
                        'static', filename="data/" + new_ligand_fn)

            return jsonify(docking_result)

        elif smiles:

            smiles = smiles[0]

            smiles_fn = os.path.join(
                UPLOAD_DIR,
                secure_filename(smiles.filename)
            )
            smiles.save(smiles_fn)

            csvfile = open(smiles_fn, 'r')
            csvreader = csv.reader(csvfile, delimiter=',')
            data = []
            for row in csvreader:
                data.append(row)

            data = render_smiles(data)

            return jsonify(data)

        elif smarts:

            smarts = smarts[0]

            smarts_fn = os.path.join(
                UPLOAD_DIR,
                secure_filename(smarts.filename)
            )
            smarts.save(smarts_fn)

            csvfile = open(smarts_fn, 'r')
            csvreader = csv.reader(csvfile, delimiter=',')
            data = []
            for row in csvreader:
                data.append(row)

            data = render_smarts(data)

            return jsonify(data)

        else:
            return jsonify(error_msg="Invalid file transfer.")
    else:
        raise NotImplementedError


def render_smiles(data):

    smiles_col_idx = [j for j in range(len(data[0])) if data[0][j]=="SMILES"][0]

    for i, row in enumerate(data):
        if i==0:
            data[i].append("SMILES IMG")
            continue
        try:
            smiles_str = data[i][smiles_col_idx]
            smiles = Chem.MolFromSmiles(smiles_str)
            AllChem.Compute2DCoords(smiles)
            smiles_fn = 'smiles_%d.png' % i
            smiles_img = os.path.join(UPLOAD_DIR, smiles_fn)
            Draw.MolToFile(smiles, smiles_img)

            data[i].append(url_for('static', filename='data/' + smiles_fn))
        except Exception as e:
            print(e)
            data[i].append("Invalid")
            pass
    return data


def render_smarts(data):

    smarts_col_idx = [j for j in range(len(data[0])) if data[0][j]=="SMARTS"][0]
    smiles_col_idx_1 = [j for j in range(len(data[0])) if data[0][j]=="SMILES_1"][0]
    smiles_col_idx_2 = [j for j in range(len(data[0])) if data[0][j]=="SMILES_2"][0]

    for i, row in enumerate(data):
        if i==0:
            data[i].append("PRODUCT")
            data[i].append("SMILES_1 IMG")
            data[i].append("SMILES_2 IMG")
            data[i].append("PRODUCT IMG")
            continue

        try:
            smarts_str = data[i][smarts_col_idx]
            smiles_str_1 = data[i][smiles_col_idx_1]
            smiles_str_2 = data[i][smiles_col_idx_2]

            rxn = AllChem.ReactionFromSmarts(smarts_str)
            ps = rxn.RunReactants((Chem.MolFromSmiles(smiles_str_1), Chem.MolFromSmiles(smiles_str_2)))

            product = ps[0][0]
            product_str = Chem.MolToSmiles(product)
            data[i].append(product_str)

            AllChem.Compute2DCoords(product)
            product_fn = 'product_%d.png' % i
            product_img = os.path.join(UPLOAD_DIR, product_fn)
            Draw.MolToFile(product, product_img)

            smiles_1 = Chem.MolFromSmiles(smiles_str_1)
            AllChem.Compute2DCoords(smiles_1)
            smiles_1_fn = 'smiles_1_%d.png' % i
            smiles_1_img = os.path.join(UPLOAD_DIR, smiles_1_fn)
            Draw.MolToFile(smiles_1, smiles_1_img)

            smiles_2 = Chem.MolFromSmiles(smiles_str_2)
            AllChem.Compute2DCoords(smiles_2)
            smiles_2_fn = 'smiles_2_%d.png' % i
            smiles_2_img = os.path.join(UPLOAD_DIR, smiles_2_fn)
            Draw.MolToFile(smiles_2, smiles_2_img)

            data[i].append(url_for('static', filename='data/' + product_fn))
            data[i].append(url_for('static', filename='data/' + smiles_1_fn))
            data[i].append(url_for('static', filename='data/' + smiles_2_fn))

        except Exception as e:
            print(e)
            data[i].append("Invalid")
            data[i].append("Invalid")
            data[i].append("Invalid")
            pass

    return data

def dock(protein_fns, ligand_fns):

    docking_result = [[{} for j in range(len(ligand_fns))]
                      for i in range(len(protein_fns))]

    for i in range(len(protein_fns)):
        for j in range(len(ligand_fns)):

            protein_fn = protein_fns[i]
            ligand_fn = ligand_fns[j]

            print("Docking: %s to %s" % (ligand_fn, protein_fn))
            docker = dc.dock.VinaGridDNNDocker(
                exhaustiveness=1, detect_pockets=False)
            (score, (protein_docked, ligand_docked)
             ) = docker.dock(protein_fn, ligand_fn)

            print("Scores: %f" % (score))
            print("Docked protein: %s" % (protein_docked))
            print("Docked ligand: %s" % (ligand_docked))

            ligand_docked_fn = ligand_docked.replace(".pdbqt", "")
            subprocess.call("csh %s %s" % (os.path.join(STATIC_DIR, 'deepchem-gui', 'scripts', 'stripqt.sh'),
                                           ligand_docked_fn), shell=True)
            ligand_docked_pdb = ligand_docked_fn + ".pdb"

            docking_result[i][j] = {'score': score[
                0], 'protein': protein_docked, 'ligand': ligand_docked_pdb}

    return docking_result
