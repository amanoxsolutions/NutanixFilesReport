# Nutanix Files Report
This repo consist a Python Code for automated File Server Reporting for all existing File Server, 
which are visible in Prism Central. The authentication will done with Prism Central. If more Nutanix Cluster are added
to the Prism Central or new File Server are created, it don't depends for the code. It gets everytime all File Servers, 
which are in the Prism Central and no additional actions are needed, if a new cluster oder new File Server are added. 

### Requirements
The following imports are requiered in Python to run this code:
- requests
- json
- matplotlib.pyplot 
- collections import defaultdict
- matplotlib.backends.backend_pdf as pdf

For accessing the Prism Central, a local user is needed with Viewer Role. This user will do all the API Calls to 
the Prism Central.  
