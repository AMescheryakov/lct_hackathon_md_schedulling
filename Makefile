init:
	git init && \
	conda env create -f ./environment.yaml && \
	pre-commit install && \
	conda activate hack_doctor_schedul

# activate environment
a:
	conda activate hack_doctor_schedul

# commit
c:
	cz c && cz bump --changelog

# commit and push to master
push-master: c
	git push --tags origin master

# commit and push to dev
p: c
	git push --tags origin develop
