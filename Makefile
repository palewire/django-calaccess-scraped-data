.PHONY: rs runserver shell sh ship test

rs:
	python example/manage.py runserver

runserver:
	python example/manage.py runserver

shell:
	python example/manage.py shell

sh:
	python example/manage.py shell

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

test:
	flake8 calaccess_scraped
	coverage run example/manage.py test calaccess_scraped
	coverage report -m
