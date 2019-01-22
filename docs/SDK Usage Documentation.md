SDK Usage Documentation
======

## 1: User Guide

![flow_chart](../images/SDK%20Basic%20User%20Manual.png)


## 2: [Sample code](demos)


Sample file | Sample content
---|---
api_demo.py | Test a single API program
max_demo.py | 3ds Max, using local analysis, demo script(Windows)
maya_demo.py | Maya, using local analysis, demo script(Windows) 
houdini_demo.py | Houdini, using local analysis, demo script(Windows) 
katana_demo.py | Katana, not using local analysis, demo script(Linux) 
c4d_demo.py | Cinema 4d, not using local analysis, demo script(Windows)


## 3: Method Analysis


---


#### 1. Log in


```
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='xxx', access_key='xxx', workspace='c:/renderfarm/sdk_test')
```


**Parameter:**<br/>


Parameter | Type | Value | Instruction
---|---|---|---
domain_name | str | task.foxrenderfarm.com | domain name, no http or https
platform | str | 2 | platform
access_id | str | xxx | AccessID
access_key | str | xxx | AccessKey
workspace | str |  | If not set up, the default path of SDK(configuration files and log files saving path) is under workspace catalogue


**Return:**<br/>


Rayvision’s object, may use this object to call other methods


---


#### 2. Set up job configuration（Plug-in settings、Project settings）


```
job_id = rayvision.set_render_env(cg_name='Maya', cg_version='2016', plugin_config={}, label_name='dasdd')
```


**Parameter:**<br/>


Parameter | Type | Value | Instruction
---|---|---|---
cg_name | str | Maya, 3ds Max, Houdini | Spelling is case sensitive
cg_version | str | 2014, 2015 ... | 
plugin_config | dict | {"fumefx":"4.0.5", "redshift":"2.0.76"} | No need to fill in if no plug-in is setting up
edit_name | str | hello | Plug-in configuration name, which represents the plug-in configuration 
label_name | str | defaultProject | Setting is optional, indicate the belonged job project 


**Return:**<br/>


Parameter | Type | Value | Instruction
---|---|---|---
job_id | str |  | Job id


---


#### 3. Analysis


```
scene_info_render, task_info = rayvision.analyse(cg_file=r'D:\gitlab\renderSDK\scenes\TEST_maya2016_ocean.mb')
```


**Parameter:**<br/>


Parameter | Type | Value | Instruction
---|---|---|---
cg_file | str |  | Scene path
project_dir | str |  | Setting is optional, project catalogue(if setting up, just detect according asset files required for rendering in your project catalogue)
software_path | str |  | Custom your local CG software location, get from the registry by default in Windows


**Return:**<br/>


Parameter | Type | Value | Instruction
---|---|---|---
scene_info_render | dict |  | The analyzed scene parameters（for rendering）, able to edit task_info | dict |  | Job parameter(for rendering), can be edited, please refer to the software configuration file in the docs directory for details.
task_info | dict |  | Job parameters (for rendering), can be edited, please refer to the software configuration file in the docs directory for details.


---


#### 4. Manually check errors and cautions before proceeding


```
error_info_list = rayvision.check_error_warn_info()
```


**Parameter:**<br/>


Parameter | Type | Value | Instruction
---|---|---|---
language | str | '0' | 0: chinese 1: English


**Return:**<br/>


Parameter | Type | Value | Instruction 
---|---|---|---
error_info_list | list |  | Manually check & fix errors and cautions before proceeding（If errors and alert occurred, SDK is not able to be proceeded）


---


#### 5.Job submit（Job parameter can be edited）


```
scene_info_render_new = scene_info_render
task_info_new = task_info
rayvision.submit_job(scene_info_render_new, task_info_new, max_speed=100)
```


**Parameter:**<br/>


Parameter | Type | Value | Instruction 
---|---|---|---
scene_info_render | dict |  | Scene parameter(for rendering)
task_info | dict |  | Job parameter(for rendering)
max_speed | int | 100 | Upload speed limit.Default value is 1048576 KB/S, means 1 GB/S


**Return:**<br/>


True


---


#### 6.Download


```
# Automatic download method 1. As soon as any frame rendering ends, the image file will be automatically downloaded to the local until the job is completed.
rayvision.auto_download(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")

# Automatic download method 2. After the job is completed, all the plot files are automatically downloaded to the local.
rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")
```


**Parameter:**<br/>


Parameter | Type | Value | Instruction 
---|---|---|---
job_id_list | list<int> |  | Job id list
local_dir | str |  | Local download
max_speed | int | 100 | Download speed limit.Default value is 1048576 KB/S, means 1 GB/S
print_log | bool | True | Whether to display the download command line. True: display; False: not display
sleep_time | int/float | 10 | Sleep time between download, unit is second


**Return:**<br/>


True

