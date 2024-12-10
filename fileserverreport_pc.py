import requests
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.backends.backend_pdf as pdf

# Nutanix User with viewer role
username = "username"
password = "password"

# plotting data
plotting_data = []
fileserver_description = []

# JSON body for all API calls to PC
body_fileserver_data_path = "templates/body_fileserver_data.json"
body_fileserver_size_path = "templates/body_fileserver_size.json"
body_file_server_share_path = "templates/body_file_server_share.json"

with open(body_fileserver_data_path, "r") as file:
    body_fileserver_data = json.load(file)

with open(body_fileserver_size_path, "r") as file:
    body_fileserver_size = json.load(file)

with open(body_file_server_share_path, "r") as file:
    body_file_server_share = json.load(file)

# helper method to calculate bytes to GiB
def bytes_to_gib(bytes_value):
    return bytes_value / (1024**3)

# main method for API call to get total all FS and IDs
def main():
    # POST request to get FS informations
    url_fileserver_data = "https://nxp12.lab.amanox.ch:9440/api/nutanix/v3/groups"
    fileserver_data_response = requests.post(url_fileserver_data, json=body_fileserver_data, auth=(username, password))

    if fileserver_data_response.status_code == 200:
        # Parse the JSON response
        data = fileserver_data_response.json()

        for group in data['group_results']:
            # Extract name and entity_id
            fs_name = group['entity_results'][0]['data'][0]['values'][0]['values'][0]
            fileserver_ID = group['entity_results'][0]['entity_id']
            sizes = get_fileserver_size(fileserver_ID)
            free_space = sizes[0] - sizes[1]
            print()
            print(f"{fs_name} has a total size of {sizes[0]:.2f} GiB. The used size is {sizes[1]:.2f} GiB and available free space is {free_space:.2f} GiB")
            fs_information_text = f"{fs_name} has a total size of {sizes[0]:.2f} GiB. The used size is {sizes[1]:.2f} GiB and available free space is {free_space:.2f} GiB"
            fileserver_description.append(fs_information_text)
            print()
            get_file_server_share(fileserver_ID, fs_name)
            plot_data()
    else:
        print("Error:", fileserver_data_response.status_code)

# method for API call to get total spaces and used spaces from all FS
def get_fileserver_size(fileserver_ID):
    url_fileserver_size = "https://nxp12.lab.amanox.ch:9440/api/files/nutanix/v3/" + fileserver_ID + "/groups"
    fileserver_size_response = requests.post(url_fileserver_size, json=body_fileserver_size, auth=(username, password))

    if fileserver_size_response.status_code == 200:
        data = fileserver_size_response.json()
        fileserver_size_bytes = int(data["group_results"][0]["entity_results"][0]["data"][1]["values"][0]["values"][0])
        total_space_used_bytes = int(data["group_results"][0]["entity_results"][0]["data"][2]["values"][0]["values"][0])
        return bytes_to_gib(fileserver_size_bytes), bytes_to_gib(total_space_used_bytes)
    else:
        print("Error:", fileserver_size_response.status_code)

# method for API call to get total spaces and all Shares
def get_file_server_share(fileserver_ID, fs_name):
    url_file_server_share = "https://nxp12.lab.amanox.ch:9440/api/files/nutanix/v3/" + fileserver_ID + "/groups"
    file_server_share_response = requests.post(url_file_server_share, json=body_file_server_share, auth=(username, password))

    if file_server_share_response.status_code == 200:
        data = file_server_share_response.json()
        for group in data["group_results"]:
            for entity in group["entity_results"]:
                share_name = None
                share_used_bytes = None
                for item in entity["data"]:
                    if item["name"] == "name":
                        share_name = item["values"][0]["values"][0]
                    elif item["name"] == "share_used_bytes":
                        share_used_bytes = int(item["values"][0]["values"][0])
                share_used_bytes = bytes_to_gib(share_used_bytes)
                print(f"{share_name}: {share_used_bytes}")
                plotting_data.append({
                        "fileserver_name": fs_name,
                        "share_name": share_name,
                        "share_size": share_used_bytes,
                    })
    else:
        print("Error:", file_server_share_response.status_code)

# method to create Pie Charts with the informations
def plot_data():
    pdf_pages = pdf.PdfPages("files_report.pdf")
    count = 0
    # Group data by file server name
    fileserver_data = defaultdict(list)

    for d in plotting_data:
        fileserver_data[d['fileserver_name']].append(d)

    # Plot pie charts for each file server
    for fileserver, fileserver_data in fileserver_data.items():
        share_names = [f"{d['share_name']} ({d['share_size']:.2f} GiB)" for d in fileserver_data]
        share_sizes = [d['share_size'] for d in fileserver_data]

        plt.figure(figsize=(9, 6))
        plt.pie(share_sizes, labels=share_names, autopct='%1.1f%%', textprops={'fontsize': 8})
        plt.xticks(fontsize=1)
        plt.yticks(fontsize=1)
        plt.title(f'Share Distribution for {fileserver}')
        x_center, _ = plt.gca().get_position().bounds[2:]
        text = fileserver_description[count]
        text_width = len(text) * 0.015
        plt.text(x_center - text_width/2, -1.5, text, fontsize=10, ha='center')
        count += 1
        # save as one PDF with more pages
        pdf_pages.savefig()

    pdf_pages.close()

# start point
if __name__ == "__main__":
    main()
