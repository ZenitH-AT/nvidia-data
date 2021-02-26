import os, sys, re, json, requests, xmltodict

os.chdir(sys.path[0])

## Functions
def clean_gpu_name(gpu_name):
    # Limit to first name if multiple names specified; most alternative names are repeated in other entries
    # (e.g. "GeForce 7050 / NVIDIA nForce 610i" is repeated as "nForce 610i/GeForce 7050")
    gpu_name = str(gpu_name).replace("NVIDIA", "").split("/")[0].strip()

    # Handle card variants (e.g. 1060 6GB, 760Ti (OEM))
    gpu_name = re.match(r"^(.*(?= [0-9]+GB)|.*(?= \([A-Z]+\))|.*)", gpu_name)[0]

    return gpu_name

def write_json(data, file_name):
    json_object = json.dumps(data, indent=4)

    with open(file_name, "w+") as outfile:
        outfile.write(json_object)

## Parse GPUs { name: pfid, ... }
gpu_xml = requests.get("https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3").content

gpu_lookup_values = xmltodict.parse(gpu_xml)["LookupValueSearch"]["LookupValues"]["LookupValue"]

gpu_dict = {clean_gpu_name(gpu_lookup_value["Name"]): gpu_lookup_value["Value"] for gpu_lookup_value in gpu_lookup_values}

write_json(gpu_dict, "gpu-data.json")

## Parse OSes { code: osID, ... }
os_xml = requests.get("https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=4").content

os_lookup_values = xmltodict.parse(os_xml)["LookupValueSearch"]["LookupValues"]["LookupValue"]

os_dict = {os_lookup_value["@Code"]: os_lookup_value["Value"] for os_lookup_value in os_lookup_values}

os_arr = [{"code": os_lookup_value["@Code"], "name": os_lookup_value["Name"], "id": os_lookup_value["Value"]} for os_lookup_value in os_lookup_values]

write_json(os_arr, "os-data.json")