venv:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

conda:
	conda create -n ezra anaconda
	conda activate ezra
	pip install -r requirements.txt
	pip install -e .

data:
	mkdir data
	curl -o data/dnstrunv.tgz https://bible.fhl.net/public/dnstrunv.tgz	
	curl -o data/mini.h5 http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/19.08/mini.h5

ezra/resources: ezra/resources/fhl_unv.dsv ezra/resources/db.h5 ezra/resources/conceptnet_strategy.pickle

ezra/resources/fhl_unv.dsv:
	tar -xvzf data/dnstrunv.tgz
	mv dnstrunv $@

ezra/resources/db.h5:
	python ezra/resources/build_db.py $@

ezra/resources/conceptnet_strategy.pickle:
	python -c "from ezra.conceptnet_strategy import ConceptNetStrategy as CS; CS().to_pickle('$@')"

test:
	pytest tests

publish:
	rm -r dist
	python -m build
	twine upload --repository testpypi dist/*

deploy: test
	gcloud app deploy
