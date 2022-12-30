import requests, xmltodict, re

CARD_VARIANT_REGEX = re.compile(r".*(?= \([A-Z]+\))|.*(?= [0-9]+GB)|.*")
NOTEBOOK_SERIES_REGEX = re.compile(r".*(\(Notebook|Quadro Blade).*")

def get_lookup_values(type_id: int):
	xml = requests.get(f"https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID={type_id}").content

	lookup_values = xmltodict.parse(xml)["LookupValueSearch"]["LookupValues"]["LookupValue"]

	return lookup_values

def clean_gpu_name(gpu_name: str):
	# Remove NVIDIA and use first name if composite (as most alternative names are repeated in other entries)
	# (e.g., "GeForce 7050 / NVIDIA nForce 610i" is repeated as "nForce 610i/GeForce 7050")
	gpu_name = gpu_name.replace("NVIDIA", "").split("/")[0].strip()

	# Handle card variants (e.g., 1060 6GB, 760Ti (OEM))
	gpu_name = CARD_VARIANT_REGEX.match(gpu_name)[0]

	return gpu_name

def get_gpu_data() -> dict:
	gpu_data = {"desktop": {}, "notebook": {}}

	# Account for some GPUs being present in both a desktop and notebook series (e.g., GeForce GTX 1050 Ti)
	notebook_series_values = [series_lookup_value["Value"] for series_lookup_value in get_lookup_values(2) if NOTEBOOK_SERIES_REGEX.match(series_lookup_value["Name"])]

	for gpu_lookup_value in get_lookup_values(3):
		gpu_data["notebook" if gpu_lookup_value["@ParentID"] in notebook_series_values else "desktop"][clean_gpu_name(gpu_lookup_value["Name"])] = gpu_lookup_value["Value"]

	return gpu_data

def get_os_data() -> list[dict]:
	return [{"id": os_lookup_value["Value"], "code": os_lookup_value["@Code"], "name": os_lookup_value["Name"]} for os_lookup_value in get_lookup_values(4)]

if __name__ == "__main__":
	# Write data to files
	import json

	def write_json(data, file_name):
		json_object = json.dumps(data, indent="\t")

		with open(file_name, "w+") as outfile:
			outfile.write(json_object)

	write_json(get_gpu_data(), "gpu-data.json")
	write_json(get_os_data(), "os-data.json")