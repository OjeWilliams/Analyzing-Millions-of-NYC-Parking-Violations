# **Analyzing Millions of NYC Parking Violations**
- [**Analyzing Millions of NYC Parking Violations**](#analyzing-millions-of-nyc-parking-violations)
    - [Background](#background)
    - [Setting up the Project](#setting-up-the-project)
      - [Things Needed](#things-needed)
      - [Part 1 - Folder Structure and Python Scripting](#part-1---folder-structure-and-python-scripting)
      - [Part 2 - Setting up Docker](#part-2---setting-up-docker)
      - [Part 3 - Elasticsearch and Kibana](#part-3---elasticsearch-and-kibana)
    - [Findings](#findings)


 ### Background
 
 This project involves interacting and analyzing NYC parking violations over the last decade through the [Socrata Open Data API](https://dev.socrata.com/). To achieve this I utilized a EC2 instance from Amazon Web Services, the Linux terminal, Docker, Elasticsearch and finally Kibana.

 Parking tickets are a headache for most people but for some states it's a tremendous money maker with them raking in millions if not [billions](https://www.carrentals.com/blog/parking-tickets-cost-americans/) in fees and fines. Luckily, we are afforded a chance to analyze this data through NYC Open Data which is a free public data site which offers an api for this very purpose. The Open Parking and Camera Violations api is a very large data source that can be much more easily and efficiently handled through cloud computing and thats what we plan to do here.  


 ### Setting up the Project

 #### Things Needed 
1. An [app token](https://data.cityofnewyork.us/login) for the NYC Open DATA API
2. An amazon account to create an EC2 instance with a docker container
3. A properly configured elastic search domain 



#### Part 1 - Folder Structure and Python Scripting
Assuming you have properly configured your EC2 instance and have ssh into it we can create a project folder and subsequent folders and files as seen below and do the following tasks: ![](2021-03-26-17-16-04.png) 


- [x] Create the required folders and files   
   <br />
  Once inside the terminal of your EC2 instance you can use the appropriate commands from the list below  to obtain the structure above: <br />
  ```pwd ``` displays the currrent working directory <br />
  ```mkdir directoryname``` makes a new directory/folder called 'directoryname'<br />
  ```rmdir directoryname``` deletes directory/folder called 'directoryname'<br />
  ```touch filename``` creates a new blank file called 'filename'<br />
  ```rm filename``` deletes a file called 'filename'<br />
  ```ls ``` lists the files and directories in current working directory<br />
  ```cd directoryname``` navigates into 'directoryname'<br />
  ```cd ..``` navigates to one directory up <br />
  <br />

- [x] Create main.py and subsequent files
 <br />

    The file main.py contains the python script that parses the --num_pages and --page_size arguments used to connect with the Socrata Open Data API by making a call to functions and files developed below:   
   - ```my_funcs``` - holds functions that connect with the Socrata Open Data API, get the desired amount of data from the api, format it and then send that formatted data to elasticsearch 
   -  ```maps.py was created``` - contains the mappings needed when creating an index for elasticsearch 
   -   ```file es_helper.py``` provided by my instructor to handle exceptions when running the script using python requests module.
   <br /> 
   <br />  

  
- [x] Ensure that your secret values are set as environment variables 
   <br />
  
  This is to avoid your passwords and keys being accidentally exposed to the public and help to keep them safe and secure. You can set them the following way when you mount your docker volume inside the terminal.  
  <br />
   ```
   docker run \
   -v ${PWD}:/app \
   -e APP_TOKEN='Your token' \
   -e ES_HOST='Your host'\
   -e ES_USERNAME='Your username' \
   -e ES_PASSWORD='Your password' \
    bigdata1:1.0
  ```
<div style="page-break-after: always"></div>

#### Part 2 - Setting up Docker
Assuming you have properly configured your EC2 instance and have ssh into it we can create a project folder and do the following tasks: 


- [x] Build Docker Image
  

  In order to build a docker image we first need to ensure that we have created a Dockerfile. A docker file is a text document that contains all the command line arguments needed to assemble the image. We can also create a requirements.txt file that conatins all the python packages required to run the project. For this project the following Dockerfile was used ![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/2021-03-26-16-12-07.png)
 
   To build a docker image named bigdata1:1.0 we run the following command in the terminal: 
    ``` docker build -t bigdata1:1.0 . ```
   
   <br />

- [x] Run Docker Image  
   
    To the run your docker image and create the container we do the following in the terminal:
 ```docker run -v ${PWD}:/app bigdata1:1.0```

If subsequent mounts are needed, as stated above you can do the following while setting environment variables
```  
> docker run \
   -v ${PWD}:/app \
   -e APP_TOKEN='Your token' \
   -e ES_HOST='Your host'\
   -e ES_USERNAME='Your username' \
   -e ES_PASSWORD='Your password' \
    bigdata1:1.0
```

<div style="page-break-after: always"></div>


#### Part 3 - Elasticsearch and Kibana
- [x] Create and configure an Elasticsearch Domain <br />
  Using these [instructions](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-createupdatedomains.html) we can create an elasticsearch domain. Ensure that in the configuration:

  - Deployment type is set to "Development and testing"
  - Network config is set to "Public access"
  - Create Master user and password 
  - Domain Policy is set to "Allow open access"
   <br />

   Once that is complete you should see something similar to 
![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/2021-03-27-13-21-07.png) 
  From, here you can access your elasticsearch endpoint as well as your kibana link for this elasticsearch domain. If you  click on the kibana link you will be brought to a page where you must sign in with the master user and password you defined when setting up the domain.
  <br />

- [x] Create Index pattern and plots for Kibana Dashboard <br />
 Once signed in you should be brought to the following page where you must select connect to your Elasticsearch index
 ![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/2021-03-27-13-38-06.png)
 Then create index pattern
 ![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/2021-03-27-13-40-43.png)
 Then search for your index (bigdata1 in my case) and click next step
 ![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/2021-03-27-13-42-24.png)

 If you had a date field that was properly formatted you will be prompted to select it, if not you can proceed. To create plots in Kibana check this official [documentation](https://www.elastic.co/guide/en/kibana/current/xpack-graph.html) and subsequently to create a kibana dashboard check [here](https://www.elastic.co/guide/en/kibana/current/dashboard.html).
 
<div style="page-break-after: always"></div>

  ### Findings
  I was able to load in around 1 million+ rows of data from the api this is was about 10% of the total dataset. This was still good enough to pull out some interesting observations/plots as seen below.
  - The Average Payment,Fine and Penalty amount over the last decade
  ![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/2021-03-27-14-17-05.png)

<br />

  - The Top 50 Parking Violations Wordcloud
  ![](https://github.com/OjeWilliams/Analyzing-Millions-of-NYC-Parking-Violations/blob/main/assets/Word%20cloud%20of%20top%2050%20violation.png)
  <br />
  <br />  

   Snippets of all my plots as well as my kibanadashboard can be found inside the assets folder. Also any discrepancy seen between tthe snippets and the dashboard is due to the fact that the snippets were created at a different time and also while data was still beling loaded. 

   If I were to change anything for a next time I would attempt to spin up more EC2 instances to therefore load many more rows over the same time spent running the script. With more rows loaded we could possibly obtain keener insights on the the data. 

