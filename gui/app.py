import os
from flask import Flask, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename
import deepchem as dc
import subprocess
from shutil import copyfile


STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static/')
DEEPCHEM_GUI = Flask('deepchem-gui', static_folder=STATIC_DIR,
                     static_url_path='/static',
                     template_folder=os.path.join(STATIC_DIR, 'deepchem-gui',
                                                  'templates')
                    )
UPLOAD_DIR = os.path.join(STATIC_DIR, "data/")
if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)
    print "Created data directory"

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

        protein_fns = []
        ligand_fns = []
        if proteins and ligands:

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

            # docking_result = dock(protein_fns, ligand_fns)
            # print(docking_result)
            docking_result = [[{'protein': u'/tmp/tmp7ZY3yl/4oc0_protein.pdb', 'score': 5.3767399999999981, 'ligand': u'/tmp/tmp7ZY3yl/4oc0_ligand_docked.pdb'}]]

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
        else:
            return jsonify(error_msg="Invalid file transfer.")
    else:
        raise NotImplementedError


def dock(protein_fns, ligand_fns):

    docking_result = [[{} for j in range(len(ligand_fns))]
                      for i in range(len(protein_fns))]

    for i in range(len(protein_fns)):
        for j in range(len(ligand_fns)):

            protein_fn = protein_fns[i]
            ligand_fn = ligand_fns[j]

            print("Docking: %s to %s" % (ligand_fn, protein_fn))
            docker = dc.dock.VinaGridRFDocker(
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
