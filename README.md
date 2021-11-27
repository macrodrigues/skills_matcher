# Skills Matcher

![image](https://user-images.githubusercontent.com/62621924/143722908-7e35e501-a4a1-4adf-ace8-fd2e9b90da14.png)

<!--
# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for skills_matcher in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/skills_matcher`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "skills_matcher"
git remote add origin git@github.com:{group}/skills_matcher.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
skills_matcher-run
```

# Install

Go to `https://github.com/{group}/skills_matcher` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/skills_matcher.git
cd skills_matcher
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
skills_matcher-run
```
-->

# Motivation

Recruiters have several difficulties when trying to find the right candidates for their job positions. They can spend a lot of time trying to get the perfect match for the task, and in the path they might end up picking an "okay" candidate instead. In addition, they receive tones of applications, that are difficult to parse.

In the other hand, the job seekers tend to apply for several job positions. Partially because some of these job descriptions are not properly built to catch the right candidate, and also because there is few guidance in order to help them all through this process.

There are several platforms that have been improving their technology in order to provide good matches between job positions and job seekers. And most of this effort is being done using **Natural Language Processing (NLP)**.

# The Dataset

**[Scraping](https://peakd.com/hive-163521/@macrodrigues/scraping-job-descriptions-for-nlp-project)** and data cleaning was done beforehand. See below a sample of the dataset:  

![image.png](https://files.peakd.com/file/peakd-hive/macrodrigues/23swkNnbaXYwZTPzdBvEsCDXtQZVM9dSUDYxjSJ84tcSmxEcRPGUQdwd1AyzDPSoSzFyQ.png)

See below an example of job description:

```
"[' Minimum of three years experience in Python Software Development + experience with Python web frameworks Experience with API integration will be highly advantageous Experience with Tenable, Kryptowire, Netsparker is advantageous Banking/financial services background is preferred (not essential) Good understanding of Agile and DevOps cultures ', ' Create and maintain the Rest APIs Migrate the application to the cloud Dockerize and orchestrate the applications Maintain the codebase for the application. Setup end to end data processing pipelines. ']"
```

# The Models



  
