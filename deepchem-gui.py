import os
from flask import Flask, redirect, url_for, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import deepchem as dc
import subprocess
from shutil import copyfile
import itertools

import sys

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

		proteins = request.files.getlist('proteins')
		ligands = request.files.getlist('ligands')

		protein_fns = []
		ligand_fns = []
		if proteins and ligands:

			for protein in proteins:
				protein_fn = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(protein.filename))
				protein.save(protein_fn)
				protein_fns.append(protein_fn)

			for ligand in ligands:
				ligand_fn = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(ligand.filename))
				ligand.save(ligand_fn)
				ligand_fns.append(ligand_fn)

			docking_result = dock(protein_fns, ligand_fns)
			print docking_result

			for i in range(len(protein_fns)):
				for j in range(len(ligand_fns)):

					protein_fn = docking_result[i][j]["protein"]
					new_protein_fn = "data/" + protein_fn.split("/")[-1]
					copyfile(protein_fn, os.path.join("static", new_protein_fn))
					docking_result[i][j]["protein"] = url_for("static", filename=new_protein_fn)

					ligand_fn = docking_result[i][j]["ligand"]
					new_ligand_fn = "data/" + ligand_fn.split("/")[-1]
					copyfile(ligand_fn, os.path.join("static", new_ligand_fn))
					docking_result[i][j]["ligand"] = url_for("static", filename=new_ligand_fn)

			# docking_result = [[{'protein': u'/tmp/tmp4rzz4h/4o9w_protein.pdb', 'score': 5.2361399999999936, 'ligand': u'/tmp/tmp4rzz4h/4oc0_ligand_docked.pdb'}, {'protein': u'/tmp/tmp6ReEf4/4o9w_protein.pdb', 'score': 6.7314999999999969, 'ligand': u'/tmp/tmp6ReEf4/4o9w_ligand_docked.pdb'}]]

			return jsonify(docking_result)
		else:
			return jsonify(error_msg="Invalid file transfer.")
	else:
		raise NotImplementedError

def dock(protein_fns, ligand_fns):

	docking_result = [[{} for j in range(len(ligand_fns))] for i in range(len(protein_fns))]

	for i in range(len(protein_fns)):
		for j in range(len(ligand_fns)):

			protein_fn = protein_fns[i]
			ligand_fn = ligand_fns[j]

			print "Docking: %s to %s" % (ligand_fn, protein_fn)
			docker = dc.dock.VinaGridRFDocker(exhaustiveness=1, detect_pockets=False)
			(score, (protein_docked, ligand_docked)) = docker.dock(protein_fn, ligand_fn)
			print "Scores: %f" % (score)
			print "Docked protein: %s" % (protein_docked)
			print "Docked ligand: %s" % (ligand_docked)

			ligand_docked_fn = ligand_docked.replace(".pdbqt", "")
			subprocess.call("csh scripts/stripqt.sh %s" % ligand_docked_fn, shell=True)
			ligand_docked_pdb = ligand_docked_fn + ".pdb"

			docking_result[i][j] = {'score': score[0], 'protein': protein_docked, 'ligand': ligand_docked_pdb}

	return docking_result

# begin serving requests
if __name__ == '__main__':
	app.run(debug=True)