import os, sys, requests, xmltodict, re, json

os.chdir(sys.path[0])

## Regular expression variables and functions
CARD_VARIANT_REGEX = re.compile(r".*(?= [0-9]+GB)|.*(?= \([A-Z]+\))|.*")
NOTEBOOK_SERIES_REGEX = re.compile(r".*((Notebooks)|Quadro Blade).*")

def get_lookup_values(type_id):
	xml = requests.get(f"https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID={type_id}").content

	lookup_values = xmltodict.parse(xml)["LookupValueSearch"]["LookupValues"]["LookupValue"]

	return lookup_values

def clean_gpu_name(gpu_name):
	# Limit to first name if multiple names specified; most alternative names are repeated in other entries
	# (e.g. "GeForce 7050 / NVIDIA nForce 610i" is repeated as "nForce 610i/GeForce 7050")
	gpu_name = str(gpu_name).replace("NVIDIA", "").split("/")[0].strip()

	# Handle card variants (e.g. 1060 6GB, 760Ti (OEM))
	gpu_name = CARD_VARIANT_REGEX.match(gpu_name)[0]

	return gpu_name

def write_json(data, file_name):
	json_object = json.dumps(data, indent=4)

	with open(file_name, "w+") as outfile:
		outfile.write(json_object)

## Parse GPUs
series_lookup_values = get_lookup_values(2)

# Account for some GPUs being present in both a desktop and notebook series (e.g. GeForce GTX 1050 Ti)
notebook_series_values = [series_lookup_value["Value"] for series_lookup_value in series_lookup_values if NOTEBOOK_SERIES_REGEX.match(series_lookup_value["Name"])]

gpu_lookup_values = get_lookup_values(3)

gpu_dict = {"desktop": {}, "notebook": {}}

for gpu_lookup_value in gpu_lookup_values:
	gpu_pair = {clean_gpu_name(gpu_lookup_value["Name"]): gpu_lookup_value["Value"]}

	if gpu_lookup_value["@ParentID"] in notebook_series_values:
		gpu_dict["notebook"].update(gpu_pair)
	else:
		gpu_dict["desktop"].update(gpu_pair)

write_json(gpu_dict, "gpu-data.json")

## Parse OSes
os_lookup_values = get_lookup_values(4)

os_arr = [{"code": os_lookup_value["@Code"], "name": os_lookup_value["Name"], "id": os_lookup_value["Value"]} for os_lookup_value in os_lookup_values]

write_json(os_arr, "os-data.json")