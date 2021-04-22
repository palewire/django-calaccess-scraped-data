.PHONY: rs runserver shell sh ship test

rs:
	pipenv run python example/manage.py runserver

runserver:
	pipenv run python example/manage.py runserver

shell:
	pipenv run python example/manage.py shell

sh:
	pipenv run python example/manage.py shell

ship:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing

test:
	pipenv run flake8 calaccess_scraped
	pipenv run coverage run example/manage.py test calaccess_scraped
	pipenv run coverage report -m
