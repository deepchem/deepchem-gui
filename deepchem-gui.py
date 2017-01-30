import os
from flask import Flask, redirect, url_for, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import deepchem as dc
import subprocess
from shutil import copyfile

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/data/'

# serve ngl webapp clone
@app.route('/')
def webapp():
    return render_template('webapp.html')

# download protein and ligand files
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':

        protein_file = request.files['protein']
        ligand_file = request.files['ligand']
        if protein_file and ligand_file:

            protein_fn = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(protein_file.filename))
            ligand_fn = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ligand_file.filename))

            protein_file.save(protein_fn)
            ligand_file.save(ligand_fn)

            docking_result = dock(protein_fn, ligand_fn)

            docked_files = docking_result['files']
            urls = []
            for docked_file in docked_files:
                fn = "data/" + docked_file.split("/")[-1]
                copyfile(docked_file, os.path.join("static", fn))
                urls.append(url_for("static", filename=fn))

            return jsonify(score=docking_result['score'], protein=urls[0], ligand=urls[1])
        else:
            return jsonify(error_msg="Invalid transfer of protein or ligand file.")
    else:
        raise NotImplementedError

def dock(protein_fn, ligand_fn):

    print "Docking: %s to %s" % (ligand_fn, protein_fn)
    docker = dc.dock.VinaGridRFDocker(exhaustiveness=1, detect_pockets=False)
    (score, (protein_docked, ligand_docked)) = docker.dock(protein_fn, ligand_fn)
    print "Scores: %f" % (score)
    print "Docked protein: %s" % (protein_docked)
    print "Docked ligand: %s" % (ligand_docked)

    ligand_docked_fn = ligand_docked.replace(".pdbqt", "")
    subprocess.call("csh /home/prasadkawthekar/deepchem-gui/scripts/stripqt.sh %s" % ligand_docked_fn, shell=True)
    ligand_docked_pdb = ligand_docked_fn + ".pdb"

    docking_result = {'score': score[0], 'files': [protein_docked, ligand_docked_pdb]}

    return docking_result

# begin serving requests
if __name__ == '__main__':
    app.run(debug=True)