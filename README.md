# Nutanix Files Report
This repository contains Python code for automated File Server Reporting. The API Calls are done 
with API Version v3. As of today (17.04.2024), there is no API documentation for API version v3 
and is therefore not supported for use. It is quite possible that these API calls will no 
longer work in a later AOS version and will have to be adapted.

### Repository overview

Provide an overview of the directory structure and files:
````
├── README.md
├── Lib
├── Scripts
├── share
├── files_report.pdf
├── templates
│   ├── body_file_server_share.json
│   ├── body_fileserver_data.json
│   └── body_fileserver_size.json
└── fileserverreport_pc.py
````
### Requirements
The following imports are requiered in Python to run this code:
- requests
- json
- matplotlib.pyplot 
- collections import defaultdict
- matplotlib.backends.backend_pdf as pdf

For accessing the Prism Central, a local user is needed with Viewer Role. This user will do all the API Calls to 
the Prism Central.  

### What does it?
The Python code authenticates with the specified user on the Prism Central. Although only data is intercepted, 
a POST is made for each call in order to obtain the information. The bodies for all the POST calls are
saved in the folder `templates` as JSON files. 
The connection is established in the 
Main method with the variable `url_fileserver_data`. This needs to be hardcoded with the API URL 
path of the Prism Central. All existing file server names with the file server IDs are stored 
temporarily in the Main method. The IDs are used to calculate the sizes and information of the 
file server and the shares that are located on the file server. The following data can be read out via API using 
the file server ID: 
- File server capacity
- File server used space
- Share names in the respective file server
- Share used space

All the information of the sizes, used spaces, etc. will come as bytes. The calculation to GiB will 
be done with the helper method `bytes_to_gib(bytes_value)`.

All this information is stored in the `plotting_data` list. This list is used to generate a series of 
pie charts, where all file servers are displayed graphically with the occupancy of the shares and the 
space used by the share. In the footer of each page, the size of the file server is calculated, 
how much of it is used and how much is still free. All information can be seen at a glance for a share.

### Benefits of this code
If more Nutanix Cluster are added to Prism Central or new file servers are created, it does not 
depend on the code. It retrieves all file servers within Prism Central and no additional actions a
re required when adding a new cluster or new file server.


