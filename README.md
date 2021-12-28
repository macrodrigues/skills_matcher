# Skills Matcher

![SkillsMatcher_3](https://user-images.githubusercontent.com/62621924/147564086-7993794e-b3b9-4e5d-adee-6ed9088b7815.png)

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

Before generating any models, manual annotation was implemented in order to clearly differentiate labels in the job descriptions. The annotation was done on around 200 job descriptions, and the labels used were: SKILL, KNOWLEDGE, MIN_EXP and LEVEL. The annotated data was then used to train a Spacy NER model.

In order to detect more skills an automated annotation was also implemented, by using a dictionary of skills. The data using the automated way was also trained, but the model could not differentiate a SKILL from a KNOWLEDGE.

Finally a simple entity ruler was also used, only to rapidly check if the skills from the dictionary were also on the job descriptions.

See below the result for the manual labelling:

![image](https://user-images.githubusercontent.com/62621924/147565069-94869da3-01fc-407f-bd27-32eb61276e61.png)

# Check the app

https://skills-matcher-best.herokuapp.com/






  
