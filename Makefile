PYTHON_VERSION = 2.7
REQUIREMENTS = requirements.txt
VIRTUAL_ENV := .venv$(PYTHON_VERSION)
PYTHON := $(VIRTUAL_ENV)/bin/python
PIP_CONF = pip.conf

PYPI = dev

test: venv
	$(PYTHON) -m unittest babelvueextractor.tests

venv_init:
	if [ ! -d $(VIRTUAL_ENV) ]; then \
		virtualenv -p python$(PYTHON_VERSION) --prompt="($(PROJECT)) " $(VIRTUAL_ENV); \
	fi

venv:  venv_init
	cp $(PIP_CONF) $(VIRTUAL_ENV)/ || true
	$(VIRTUAL_ENV)/bin/pip install -r $(REQUIREMENTS)


clean_venv:
	rm -rf $(VIRTUAL_ENV)

clean_pyc:
	find . -name \*.pyc -delete

clean: clean_venv clean_pyc

package:
	$(PYTHON) setup.py sdist

pkg_upload:
	$(PYTHON) setup.py sdist upload -r $(PYPI)

pkg_register:
	$(PYTHON) setup.py sdist register -r $(PYPI)
