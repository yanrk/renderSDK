# -*- coding:utf-8 -*-
# 场景文件已损坏或者被压缩
error9900_max_damage = 'Scene has damged or been compressed'
# 未找到场景使用的3ds Max 软件版本
error9899_maxexe_notexist = '3ds Max software of scene has not been found'
# 场景文件用的3dsmax版本和项目配置的3dsmax版本不一致
error9898_project_maxversion = '3ds Max version of scene is different from the version you configured for the project'
# 获取3ds Max 软件版本失败
error_getcgversion_exception = 'Getting 3ds Max software version failed'
# 渲染器丢失
error_getrenderer_exception = 'Missing renderer'
# 获取3ds Max 软件版本失败
error_getcglocation_exception = 'Getting 3ds Max software version failed'
error_multiscatterandvray_confilict = '{} is not compatible with {}'

# 获取场景信息失败，可能场景文件已损坏或者被压缩，或者使用了非英文版本制作。
msg_getmaxinfo_failed = 'Get max file info failed,Scene maybe has damged or been compressed'
error_getmaxinfo_failed = msg_getmaxinfo_failed
progress_getmaxinfo = 'get max file info start'
progress_getmaxversion = 'Get 3ds Max version start...'

error_zip_failed = 'Failed to compress 3dsmax scene into 7zip file'
progress_startmax = 'Start 3ds Max'
progress_endmax = 'Close 3ds Max'
progress_startpackmax = 'Compressing 3dsmax scene to 7zip'
progress_endpackmax = 'Compress 3dsmax scene to 7zip successfully'
progress_subSuccessed = 'Submit task successfully'
progress_subFailed = 'Submit task failed'

# 项目配置的版本和场景版本不匹配
version_not_match = "Project configuration version and scenario version mismatch"

# -----------------------------------以下是把"软件"换成"CG", 软件名字可以用self.version_str拼接-------------------------------------------
# 未找到场景使用的3ds Max 软件版本
error9899_cgexe_notexist = '{} software of scene has not been found'
# 场景文件用的3dsmax版本和项目配置的3dsmax版本不一致
error9898_project_versfion = '{} version of scene is different from the version you configured for the project'
# 获取3ds Max 软件版本失败
error_getcgversion_exception = 'Getting {} software version failed'
# 获取3ds Max 软件版本失败
error_getcglocation_exception = 'Getting {} software version failed'
error_multiscatterandvray_confilict = '{} is not compatible with {}'

# 获取场景信息失败，可能场景文件已损坏或者被压缩，或者使用了非英文版本制作。
msg_get_cg_info_failed = 'Get {} file info failed,Scene maybe has damged or been compressed'
error_get_cg_info_failed = msg_get_cg_info_failed
progress_getcginfo = 'get {} file info start'
progress_get_cg_version = 'Get {} version start...'

error_zip_failed = 'Failed to compress {} scene into 7zip file'
progress_start_cg = 'Start {}'
progress_end_cg = 'Close {}'
progress_startpackcg = 'Compressing {} scene to 7zip'
progress_endpackcg = 'Compress {} scene to 7zip successfully'
