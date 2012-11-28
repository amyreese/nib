build:
	python setup.py build

dev:
	python setup.py develop

upload:
	python setup.py sdist upload

clean:
	rm -rf build dist README MANIFEST Nib.egg-info nib/sample.zip
