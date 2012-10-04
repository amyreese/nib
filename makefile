build:
	python setup.py build

upload:
	python setup.py sdist upload

clean:
	rm -rf build dist README MANIFEST Nib.egg-info
