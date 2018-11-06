#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

# Add renderSDK path to sys.path
renderSDK_path = r'D:\gitlab\renderSDK'
sys.path.append(renderSDK_path)

from renderSDK.RayvisionAPI import RayvisionAPI

access_id = r'xxx'
access_key = r'xxx'
domain_name = r'task.foxrenderfarm.com'
platform = '2'

rayvision = RayvisionAPI(domain_name, platform, access_id, access_key, log_obj=True)
r_data = rayvision.query_platforms()
print(r_data)

# r_data = rayvision.query_platforms()
# r_data = rayvision.query_user_profile()
# r_data = rayvision.query_user_setting()
# r_data = rayvision.update_user_setting(task_over_time)
# r_data = rayvision.get_transfer_bid()
# r_data = rayvision.create_task(count=1, out_user_id=None)
# r_data = rayvision.submit_task(task_id)
# r_data = rayvision.query_error_detail(code, language='0')
# r_data = rayvision.get_task_list(page_num, page_size)
# r_data = rayvision.stop_task(task_param_list)
# r_data = rayvision.start_task(task_param_list)
# r_data = rayvision.abort_task(task_param_list)
# r_data = rayvision.delete_task(task_param_list)
# r_data = rayvision.query_task_frames(task_id, page_num, page_size, search_keyword=None)
# r_data = rayvision.query_all_frame_stats()
# r_data = rayvision.restart_failed_frames(task_param_list)
# r_data = rayvision.restart_frame(task_id, select_all, ids_list=[])
# r_data = rayvision.query_task_info(task_ids_list)
# r_data = rayvision.add_label(new_name, status)
# r_data = rayvision.delete_label(del_name)
# r_data = rayvision.get_label_list()
# r_data = rayvision.query_supported_software()
# r_data = rayvision.query_supported_plugin(cg_id)
# r_data = rayvision.add_render_env(cg_id, cg_name, cg_version, render_layer_type, edit_name, render_system, plugin_ids_list)
# r_data = rayvision.update_render_env(cg_id, cg_name, cg_version, render_layer_type, edit_name, render_system, plugin_ids_list)
# r_data = rayvision.delete_render_env(edit_name)
# r_data = rayvision.set_default_render_env(edit_name)
# r_data = rayvision.get_render_env(cg_id)
