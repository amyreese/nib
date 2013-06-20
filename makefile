VERSION:=$(shell grep version nib/__init__.py | sed -e "s|.*'\(.*\)'|\1|g")

version:
	sed -i -e "s|version=.*,|version='$(VERSION)',|" setup.py

build: version
	python setup.py build

dev: version
	python setup.py develop

upload: version
	python setup.py sdist upload

clean:
	rm -rf build dist README MANIFEST Nib.egg-info nib/sample.zip
