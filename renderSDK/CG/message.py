# -*- coding:utf-8 -*-
# Scene file is corrupted or compressed
error9900_max_damage = 'Scene has damged or been compressed'
# The 3ds Max software version used by the scene was not found
error9899_maxexe_notexist = '3ds Max software of scene has not been found'
# 3dsmax version of the scene file is inconsistent with the 3dsmax version of the project configuration
error9898_project_maxversion = '3ds Max version of scene is different from the version you configured for the project'
# Get 3ds Max software version failed
error_getcgversion_exception = 'Getting 3ds Max software version failed'
# Renderer is missing
error_getrenderer_exception = 'Missing renderer'
# Get 3ds Max software version failed
error_getcglocation_exception = 'Getting 3ds Max software version failed'
error_multiscatterandvray_confilict = '{} is not compatible with {}'

# Failed to get the scene information. The scene file may be damaged or compressed, or a non-English version may be used.
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

# Project configuration version and scene version do not match
version_not_match = "Project configuration version and scenario version mismatch"

# ----------------------------------- The following is the replacement of "software" with "CG", the software name Can be stitched with self.version_str -------------------------------------------
# The 3ds Max software version used by the scene was not found
error9899_cgexe_notexist = '{} software of scene has not been found'
# 3dsmax version of the scene file is inconsistent with the 3dsmax version of the project configuration
error9898_project_versfion = '{} version of scene is different from the version you configured for the project'
# Get 3ds Max software version failed
error_getcgversion_exception = 'Getting {} software version failed'
# Get 3ds Max software version failed
error_getcglocation_exception = 'Getting {} software version failed'
error_multiscatterandvray_confilict = '{} is not compatible with {}'

# Failed to get the scene information. The scene file may be damaged or compressed, or a non-English version may be used.
msg_get_cg_info_failed = 'Get {} file info failed,Scene maybe has damged or been compressed'
error_get_cg_info_failed = msg_get_cg_info_failed
progress_getcginfo = 'get {} file info start'
progress_get_cg_version = 'Get {} version start...'

error_zip_failed = 'Failed to compress {} scene into 7zip file'
progress_start_cg = 'Start {}'
progress_end_cg = 'Close {}'
progress_startpackcg = 'Compressing {} scene to 7zip'
progress_endpackcg = 'Compress {} scene to 7zip successfully'
