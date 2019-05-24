# Analyze module document 

## 1. Call method

 Used as a module:
1. `cg_file` Scene file
2. `job_info` Example, see file for details
3. `exe_path` exe path of CG software, this parameter can be submitted and used directly, otherwise, path will be detected based on CG files. The default exe path is ‘None’ 


## 2. User guide:

1. Required parameter: `job_info`, `cg_file`, optional parameter: `exe_path`
    1. `job_info`: customized category or `RayvisionJob` category, certain attributes required, refer to 2 paragraph for an example
    2. `cg_file`: scene file path, supported software include 3ds Max, Maya, Houdini, corresponding file layout `.max`, `.ma/.mb`, `.hip`
    3. `exe_path`: optional parameter, default exe path is `None`, if not setting up, exe path will be detected in the module; if setting up manually, should be as exe executing path(Absolute path), be sure to execute the correct path, the software path is:                       `<abspath>/3dsmax.exe`, `<abspath>/mayabatch.exe`, `<abspath>/hython.exe` 

2. Example

Customized “job” category, required attributes are as follow:

```python
class Job(object):
    def __init__(self, job_id, local_os, work_dir, zip_path, log_dir, task_json_path, asset_json_path, tips_json_path, upload_json_path, task_info):
        self.job_id = job_id
        self._local_os = local_os
        self._work_dir = work_dir
        self._zip_path = zip_path
        self._log_dir = log_dir
        self._task_json_path = task_json_path
        self._asset_json_path = asset_json_path
        self._tips_json_path = tips_json_path
        self._upload_json_path = upload_json_path
        self._task_info = task_info
```

Create a “job” example, and initialize it to analyze module

```python
job_id = "1234"
local_os = "windows"
work_dir = "d:\\rayvision\\1234"
zip_path = "d:\\rayvision\\tool\\zip\\windows\\7z.exe"
log_dir = "d:\\rayvision\\1234"
task_json_path = "d:\\rayvision\\1234\\task.json"
asset_json_path = "d:\\rayvision\\1234\\asset.json"
tips_json_path = "d:\\rayvision\\1234\\tips.json"
upload_json_path = "d:\\rayvision\\1234\\upload.json"
task_info = {
    "software_config": {
        "cg_version": "2015",
        "cg_name": "3ds Max",
        "plugins": {
        }
    }
}

job = Job(job_id, local_os, work_dir, zip_path, log_dir, task_json_path, asset_json_path, tips_json_path, upload_json_path, task_info)

```

3. Execute

3.1 Run analysis module (Integral process)

```python

cg_file = "d:\\xxxx.max"
ray = RayvisionAnalyse(job_info=job, cg_file=cg_file, exe_path=None)
ray.run()
```

3.2 Or separately run a function:

```python
# Get access to scene info, detect software exe path 
ray.analyse_cg_file()

# Separate analysis
ray.analyse()
```

## 3. Caution instruction
```python
class MaxDamageError(RayvisionError):
    """Max File Damage"""


class MaxExeNotExistError(RayvisionError):
    """Max exe path does not exist """


class CGExeNotExistError(RayvisionError):
    """CG exe path does not exist """


class ProjectMaxVersionError(RayvisionError):
    """Max version error"""


class GetCGVersionError(RayvisionError):
    """CG software version accessing error"""


class GetRendererError(RayvisionError):
    """Renderer accessing error"""


class GetCGLocationError(RayvisionError):
    """ CG software location accessing error """


class MultiscatterandvrayConfilictError(RayvisionError):
    """Multiscatter and Vray version confict"""


class VersionNotMatchError(RayvisionError):
    """ Versions matching error"""


class CGFileNotExistsError(RayvisionError):
    """CG file does not exist"""


class CGFileZipFailError(RayvisionError):
    """CG file compressing error"""


class CGFileNameIllegalError(RayvisionError):
    """CG file name not illegal """


class AnalyseFailError(RayvisionError):
    """Analysis error"""

```

