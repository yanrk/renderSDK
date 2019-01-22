# Render SDK for Python

[README of Chinese](README-CN.md)


## Overview

    We created an easy Python-based RenderSDK to better use our cloud rendering service.
    This is the official RenderSDK maintained by the FOXRenderfarm / RENDERBUS RD&TD team.
    The SDK has been tested with python2.7.10 and python3.4.4.
    
    
## Why RenderSDK

    1. Automation. The SDK automates the process of using the cloud rendering service (analysis scenarios, uploading assets, rendering, downloading). And can be embedded in the customer's own scheduling (such as DeadLine, Qube, etc.)
    2. Open source. Users can customize development or submit development suggestions
    3. Cross-version. Support for python2 and python3
    4. Cross-platform. Support for Windows and Linux
    5. High security. Use dynamic signature algorithm authentication (HmacSHA256 + Base64 + UTC timestamp time-limited authentication + random number to prevent replay attacks), more secure
    6. Provide a variety of ways to use. Support local analysis and non-local analysis
    7. Good independence. Separate the API from the business logic and easily expand
    8. Have detailed documentation

    
## Supported software

- [x] Maya
- [x] 3ds Max
- [x] Houdini
- [x] Katana
- [x] Cinema 4d
- [x] VR Standalone


## Before you begin

1. You need an [FOXRenderfarm](https://task.foxrenderfarm.com) account.
2. You need to apply for the RenderSDK in the [FOXRenderfarm Developer](https://task.foxrenderfarm.com/user/developer), and obtain the AccessID and AccessKey to use it.


## Installation

```bash
git clone https://github.com/renderbus/renderSDK.git
```

or

[Download](https://github.com/renderbus/renderSDK/archive/master.zip)


## Getting started

> There are two ways to use the SDK: using local analysis and not using local analysis.

1. Using local analysis

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

# Add source code path(renderSDK) to sys.path
renderSDK_path = r'<Your renderSDK location>'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.Log in
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='<Your AccessID>', access_key='<Your AccessKey>', workspace='<SDK workspace: The path to save job information and logs>')

# 2.Set up rendering environment(plug-in configuration, label name）
job_id = rayvision.set_render_env(cg_name='Maya', cg_version='2016', plugin_config={"mtoa": "3.0.1.1"}, label_name='label_name')

# 3.Analysis
scene_info_render, task_info = rayvision.analyse(cg_file=r'<Your scene file path>')

# 4. User can Manage the errors or warnings manually, if applicable
error_info_list = rayvision.check_error_warn_info()

# 5.User can modify the parameter list(optional), and then proceed to job submitting
rayvision.submit_job(scene_info_render, task_info)

# 6.Download
rayvision.auto_download(job_id_list=[job_id], local_dir=r"<Your output path>")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")

```

2. Not using local analysis

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

# Add source code path(renderSDK) to sys.path
renderSDK_path = r'<Your renderSDK location>'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.Log in
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='<Your AccessID>', access_key='<Your AccessKey>', workspace='<SDK workspace: The path to save job information and logs>')

# 2.Set up rendering environment(plug-in configuration, label name）
job_id = rayvision.set_render_env(cg_name='Maya', cg_version='2016', plugin_config={"mtoa": "3.0.1.1"}, label_name='label_name')

# 3.Set parameters (see the software configuration file documentation in the docs directory)
scene_info_render = {}
task_info = {}
upload_info = {}

# 4.Submit job
rayvision.submit_job(scene_info_render, task_info, upload_info)

# 5.Download
rayvision.auto_download(job_id_list=[job_id], local_dir=r"<Your output path>")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"<Your output path>")

```


## More resources
- [More examples](demos)
- [More Documents](docs)
- [SDK Usage Documentation](docs/SDK%20Usage%20Documentation.md)
- [API Reference](docs/RAYVISION%20Render%20API%20V3.0.pdf)


## Catalog description

- [demos](demos): demo scripts
- [docs](docs): documentation
- [docs_zh](docs_zh): chinese documentation
- [image](image): images references for documentation
- [renderSDK](renderSDK): source code
- [scenes](scenes): test scenes


## Other

> - Windows supported: Maya, Houdini, 3ds Max, Cinema 4d, VR Standalone
> - Linux supported: Maya, Houdini, Katana

> - Chinese supported: 3ds Max
> - Chinese not supported: Maya, Houdini, Katana, Cinema 4d, VR Standalone


## Change Log

[CHANGELOG.md](CHANGELOG.md)


## License

[Apache License 2.0](https://github.com/renderbus/renderSDK/blob/master/LICENSE).
