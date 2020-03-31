Crawling-GoCD
====================================================
[![pypi](https://img.shields.io/pypi/v/crawling-gocd.svg)](https://pypi.org/project/crawling-gocd/)
[![Build](https://travis-ci.org/play-code-tools/crawling-gocd.svg?branch=master)](https://travis-ci.org/play-code-tools/crawling-gocd)
[![Coverage Status](https://coveralls.io/repos/github/play-code-tools/crawling-gocd/badge.svg?branch=master)](https://coveralls.io/github/play-code-tools/crawling-gocd?branch=master)

This project works for crawling the build histories of pipelines and calculate the metrics.

### Installation
1. python 3
2. pipenv

### Development
1. Install the packages
  ```
  pipenv sync --dev
  ```
2. Run test
  ```
  pipenv run python -m unittest discover
  ```
3. bump version(using bumversion)
  ```
  pipenv run bumpversion [major|minor|patch]
  ```
4. deploy to pypi
Add a tag for new commit, then push them, the commit and tag, to origin.
The Travis CI will auto deploy package into pypi after pass the build.

### Run
1. Input configration in the file `crawling-gocd.yaml`
  ```
pipelines:
  - 
    name: account-management-normal-master
    calc_grouped_stages: 
      ci:
        - code-scan
        - test-integration
        - build
      qa:
        - flyway-qa
        - deploy-qa
    start_time: 2019-07-10 00:00:00
    end_time: 2019-08-12 23:59:59
  - 
    name: account-management-normal-release
    calc_grouped_stages: 
      uat:
        - flyway-uat
        - deploy-uat

global:
  time_type: fix
  start_time: 2019-07-01 00:00:00
  end_time: 2019-08-12 23:59:59

output_class_name: crawling_gocd.outputs.OutputCsv
metrics:
  four_key_metrics:
    - DeploymentFrequency
    - ChangeFailPercentage
    - ChangeFailPercentage_ignoredContinuousFailed
    - MeanTimeToRestore
```
  **`pipeline: name`** is the string in the history API URL.  

  **`pipeline: calc_grouped_stages`** includes each phase needed to calculate metrics.  
  Such as, if we want to calculate the deployment frequency for QA environment, so we configure the `qa` phase for the QA deployment which has two stages.  
  If one of the two stages fails, determines QA deployment failed, so we configure the qa phase has `flyway-qa`、`deploy-qa`.

  **`global:time_type`** support two types: `fix` and `cycle`.
  
  **`cycle`** type means auto calculate the time range start at the several weeks before the program current thread running time.
  For example, the current thread ran with the setting `global:cycle_weeks:2` is triggered at _2019-10-07 19:00:00_.
  The program will get the data between `2019-09-23 00:00:00`(Monday) and `2019-10-06 23:59:59`(Sunday), not including the current week.

  **`fix`** type means fixed time range - hard code configration.
  When setting the `global:time_type` to `fix`, using the following keys configuration.
  **`global:start_time`** and **`global:end_time`**, determines the time slot for crawling pipeline histories.  
  Also, there are `pipeline start_time` and `pipeline end_time`, they have a high priority to `global:start_time` and `global:end_time`.  

  **`output_class_name`** points out the output classes name when autowired. Value string splitter is semicolon. If not setting up, the default value string is `crawling_gocd.outputs.OutputCsv`.
  
  **`metrics:four_key_metrics`** can customize the metrics scope. 
  This program support 4 metrics at present. They are `DeploymentFrequency`, `ChangeFailPercentage`, `ChangeFailPercentage_ignoredContinuousFailed` and `MeanTimeToRestore`. 

2. Run command
  ```
  pipenv run python -m crawling_gocd
  ``` 
  __Attention__: Need set the environment variables `GOCD_SITE`、`GOCD_USER`、`GOCD_PASSWORD` before running the command.
  Alternatively, use the following command:
  ```
  GOCD_SITE="<your_gocd_site>" GOCD_USER="<your_username>" GOCD_PASSWORD="<your_password>" pipenv run python -m crawling_gocd
  ```

### Expansibility
So far the crawling URL is according to the goCD version 18.11.  
If need use to incompatible goCD version, just replace the file `Crawler.py`.  
If need some new metrics handler, just write the implementation class under the superclass  `CalculateStrategyHandler`, and assemble into `Calculator` in the file `Portal`.
