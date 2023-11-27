FROM deepchemio/deepchem

RUN conda install flask
RUN pip install rdkit
RUN conda install -c conda-forge deepchem
RUN git clone https://github.com/deepchem/deepchem-gui.git && \
	cd deepchem-gui && \
	python setup.py install

EXPOSE 5000

ENTRYPOINT exec deepchem-gui server -H 0.0.0.0 --no-browser

