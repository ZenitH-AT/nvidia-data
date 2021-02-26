# nvidia-data

Writes the latest product family (GPU) and operating system data from the NVIDIA Download API ([lookupValueSearch](https://www.nvidia.com/Download/API/lookupValueSearch.aspx)) to a JSON file.

## Notes

* Product family (GPU) data ([gpu-data.json](https://raw.githubusercontent.com/ZenitH-AT/nvidia-data/main/gpu-data.json)) is updated whenever the results of ```https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=3``` change.
	* Updates to this file will always occur before any new GPUs are released.
* Operating system data ([os-data.json](https://raw.githubusercontent.com/ZenitH-AT/nvidia-data/main/os-data.json)) is updated whenever the results of ```https://www.nvidia.com/Download/API/lookupValueSearch.aspx?TypeID=4``` change.

## FAQ

Q. What exactly does this script do?

> This script effectively converts the XML data from the NVIDIA Download API and converts it into a form that can be read very quickly.
>
> ![Data mapping](https://i.ibb.co/q9295fg/data-mapping.png "Data mapping")

Q. What are the JSON files used for?

> The JSON files created by this script are intended to be used by the nvidia-update.ps1 script (available at [ZenitH-AT/nvidia-update](https://github.com/ZenitH-AT/nvidia-update)).
>
> Previously, the script needed to query the NVIDIA Download API multiple times, iterating through and filtering every bit of data. Measures to speed up this process (i.e. limiting queries to desktop/mobile GPU and GeForce cards only) mostly just made the code more complicated.
>
> The nvidia-update.ps1 script passes the data to the NVIDIA [AjaxDriverService](https://gfwsl.geforce.com/services_toolkit/services/com/nvidia/services/AjaxDriverService.php). An example of how this data is used can be found [here](https://github.com/ZenitH-AT/nvidia-update#faq).
>
> GPU data created by the get-nvidia-data.py script is structured in key value pairs for performance. OS data is structured more traditionally, since both the code and part of the name must be compared.
>
> * GPU data:
>	* GPU name and `pfid`
>
> ```json
> 	{
>		"GeForce RTX 3070": "933",
>	}
> ```
> * OS data:
>	* OS code, OS name and `osID`
>
> ```json
> 	[
>		{
>			"code": "10.0",
>			"name": "Windows 10 64-bit",
>			"id": "57"
>		},
>	]
> ```
>
> Additionally, since GPU data keys must match exactly with the computer's GPU name, all GPU names are run through a ```clean_gpu_name()``` function:
>
> Old name | New name
> --- | --- | ---
> GeForce 7050 / NVIDIA nForce 610i | GeForce 7050
> nForce 610i/GeForce 7050 | nForce 610i
> Quadro M6000 24GB | Quadro M6000
> GeForce GTX 760 Ti (OEM) | GeForce GTX 760 Ti
> NVIDIA TITAN RTX | TITAN RTX

## Planned changes

The script should be updated to account for not all alternative names being repeated in other entries (e.g. nForce 630i is not retrieved by this script).
