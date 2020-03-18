
run: 
	env PYTHONPATH=${PWD} python routes/rest.py
release:
	git checkout master && git merge develop
