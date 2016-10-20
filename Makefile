venv2:
	-f .venv2/bin/activate || virtualenv -p python2.7 .venv2
	.venv2/bin/pip install -r requirements.txt

venv3:
	-f .venv3/bin/activate || virtualenv -p python3 .venv3
	.venv3/bin/pip install -r requirements.txt

test:
	python -m unittest babelvueextractor.tests
