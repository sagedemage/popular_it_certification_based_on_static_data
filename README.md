# popular_it_certification_based_on_static_data
A program to compile data to get the most popular IT certifications in the defense industry.

Install the shell plugin for poetry
```
poetry self add poetry-plugin-shell
```

Install the dependencies
```
poetry install
```

Run a subshell with virtual environment activated
```
poetry shell
```

Run the program
```
flask --app main run
```

## Running the Program on FreeBSD
These are the steps that are required to run the program on FreeBSD.

Install the dependencies
```
sudo pkg install py312-pandas
sudo pkg install py312-flask
```

Run the program on FreeBSD
```
flask --app main run
```

poetry env activate 