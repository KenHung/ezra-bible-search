venv:
	python -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

data:
	mkdir data
	curl -o data/dnstrunv.tgz https://bible.fhl.net/public/dnstrunv.tgz	
	curl -o data/mini.h5 http://conceptnet.s3.amazonaws.com/precomputed-data/2016/numberbatch/19.08/mini.h5

ezra/resources/fhl_unv.dsv:
	tar -xvzf data/dnstrunv.tgz
	mv data/dnstrunv $@

ezra/resources/db.h5:
	python ezra/resources/build_db.py $@

ezra/resources/conceptnet_strategy.pickle:
	python -c "from ezra.conceptnet_strategy import ConceptNetStrategy as CS; CS().to_pickle('$@')"

test:
	pytest tests

deploy: test
	gcloud app deploy
