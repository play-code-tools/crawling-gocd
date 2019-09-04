## Crawling-GoCD
This project works for crawling the pipeline build histories and calculate the metrics.

### Installation
1. python 3
2. pipenv

### Build and run
1. Install the packages
```
pipenv install
```
2. Run test
```
pipenv run python -m unittest discover
```
3. Run command
```
pipenv run python main.py
``` 
__Attention__: Need set the environment variables `GOCD_SITE`、`GOCD_USER`、`GOCD_PASSWORD` before run the command.
Alternatively, use the following command:
```
GOCD_SITE="<your_gocd_site>" GOCD_USER="<your_username>" GOCD_PASSWORD="<your_password>" pipenv run python main.py
```

### Expansibility
So far the crawling url is according to the goCD version 18.11.
If need use to incompatible goCD version, just replace the file `Crawler.py`.
If need some new metrics handler, just write the implementation class under the superclass  `CalculateStrategyHandler`, and assemble into `Calculator` in the file `Portal`.
