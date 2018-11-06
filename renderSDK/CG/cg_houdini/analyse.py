import os,sys,time
import argparse
import json

base_houdini = os.path.dirname(sys.path[0])
print("%s/cg_houdini/function"%base_houdini)
sys.path.append("%s/cg_houdini/function"%base_houdini)
from HoudiniUtil import HoudiniUtil
from HoudiniPlugin import HoudiniPlugin

parser = argparse.ArgumentParser()
parser.add_argument('-project', type=str, required=True, help='.hip file to render')
parser.add_argument('-GPU', type=int, required=False, help='the gpu id which to be used to render')
parser.add_argument('-outdir', type=str, required=True, help='image with dir to render to')
parser.add_argument('-plugindir', type=str, required=False, help='The plugin path in B disk')
parser.add_argument('-custid', type=str, required=False, help='The user id  ')

args = parser.parse_args()

class hfs_fileBase():
    
    def __init__(self,args=""):
        HoudiniUtil.print_times('Start hfs base...')
        self.render_node_type = ['Redshift_ROP','ifd','arnold']
        self.args = args
        self.frame = ''

        self.asset_adict = {} ### for asset.json 
        self.foler_adict = {} ### the asset in folders
        self.tips_adict = {}
        self.check_history = {}

        self.basedir = os.path.abspath(self.args.project).replace("\\","/")
        self._hip_val = os.path.dirname(self.args.project).replace("\\","/")

    def loadhipfile(self):

        self.hip_file=self.args.project
        if os.path.exists(self.hip_file):
            HoudiniUtil.print_times ("Loading hip file: %s" % self.hip_file)
            try:
                hou.hipFile.load(self.hip_file)
                HoudiniUtil.print_times ("Loading hip file success")
                
                # update $HIP once file loaded
                hou.hscript("setenv HIP=" + str(self._hip_val))
                hou.hscript("varchange")
                
            except (IOError ,ZeroDivisionError),e:
                HoudiniUtil.print_times (e)
        else:
            HoudiniUtil.print_times ("ERROR: the hip file is not exist!")
            sys.exit(1)

    def Custmset(self):
        HoudiniUtil.print_times("Custom Setup start...")
        
        _files_name = []
        _config_patn = "%s/custom/Bhand"%self.args.plugindir
        from custom import Bhand
        _function_all = dir(Bhand)
        for (dirpath, dirnames, filenames) in os.walk(_config_patn):
            _files_name.extend(filenames)
        for scr in _files_name:
            _py_list = scr.split(".py")
            if _py_list[1]=='' and _py_list[0] in _function_all:
                cmds = "Bhand.%s.main(self)" % _py_list[0]
                ## print(cmds)
                try:
                    exec cmds
                except Exception as e:
                    HoudiniUtil.print_times(e)
        HoudiniUtil.print_times("Custom Setup end.")

    def DataSet(self):
        HoudiniUtil.print_times("DataSet Setup start...")

        sys.path.append(self.args.plugindir)
        cfg_path = '%s/cfg'%self.args.outdir.replace("\\","/")
        self._cfg_task = '%s/task.json'%cfg_path
        self._cfg_asset = '%s/asset.json'%cfg_path
        self._cfg_tips = '%s/tips.json'%cfg_path
        self._cfg_folder = '%s/folder_asset.json'%cfg_path

        datapath = "B:\plugins\houdini\data"
        data_file = "%s/error_id.json"%datapath

        self.Json_adict = eval(open(self._cfg_task, 'r').read()) if os.path.exists(self._cfg_task) else {}
        self.Error_ids = eval(open(data_file, 'r').read()) if os.path.exists(data_file) else {}

        HoudiniUtil.print_times("DataSet Setup end.")

    def configs(self):
        HoudiniUtil.print_times("Config Setup start...")
        ## All the code in configs folder will run one time 
        _files_name = []
        _config_patn = "%s/configs/Bhand"%self.args.plugindir
        from configs import Bhand
        _function_all = dir(Bhand)
        for (dirpath, dirnames, filenames) in os.walk(_config_patn):
            _files_name.extend(filenames)
        for scr in _files_name:
            _py_list = scr.split(".py")
            if _py_list[1]=='' and _py_list[0] in _function_all:
                cmds = "Bhand.%s.main(self)" % _py_list[0]
                try:
                    exec cmds
                except Exception as e:
                    HoudiniUtil.print_times(e)
        HoudiniUtil.print_times("Config Setup end.")

    def GetAsses(self):
        HoudiniUtil.print_times('')
        HoudiniUtil.print_times("GetAsses start...")
        from HoudiniThread import HoudiniThread
        function_all = {"cam":[HoudiniPlugin.CameraCkeck,[self]],"filecheck":[HoudiniPlugin.FilesCheck,[self]]}
        threads = HoudiniThread.StartThread(HoudiniThread.CreatThread(function_all))
        for thr in threads[0]:
            thr.join()
        ''' Informations '''
        HoudiniPlugin.TipsInfo(self)
        HoudiniUtil.WriteFile(self.asset_adict,self._cfg_asset,'json')
        HoudiniUtil.WriteFile(self.foler_adict,self._cfg_folder,'json')
        HoudiniUtil.WriteFile(self.tips_adict,self._cfg_tips,'json')

    def analy_info(self):
        HoudiniUtil.print_times("Analysis & ropnodes start...")
        rop_node = []
        geo_node = []

        if not self.args.outdir== '':
            self.file_info = self.args.outdir
        else:
            self.file_info = "D:/houdini/RS/Analysis_info.txt"
            if not os.path.exists("D:/houdini/RS"):
                os.makedirs("D:/houdini/RS")
            HoudiniUtil.print_times("The function is not used as analysis,write the infomation to default file")

        info = ''
        i = 0
        HoudiniUtil.print_times("Searching Geometrry Rops...")
        simu_cunt = 0
        for obj in hou.node('/').allSubChildren():
            nodes = {} ## {"node":"","frames":"","option":""}
            objPath = obj.path()
            objPath = objPath.replace('\\','/')
            objTypeName = obj.type().name()
            if objTypeName in ['geometry','rop_geometry']:
                render_rop_Node = hou.node(objPath)
                if render_rop_Node.parm("execute"):
                    HoudiniUtil.print_times("   Geometry ROP: %s" % render_rop_Node)
                    if i>0: info += '\n'
                    info += objPath
                    nodes["node"] = objPath
                    info += '|' + str(obj.evalParm('f1'))
                    info += '|' + str(obj.evalParm('f2'))
                    info += '|' + str(obj.evalParm('f3'))
                    pass_frame = str(int(obj.evalParm('f3'))) if int(obj.evalParm('f3'))>0 else "1"
                    nodes["frames"] = "%s-%s[%s]" % (str(int(obj.evalParm('f1'))), str(int(obj.evalParm('f2'))), pass_frame)

                    info += '|' + '0'
                    nodes["option"] = '0'
                    nodes["render"] = "0"

                    geo_node.append(nodes)
                    i+=1
                    simu_cunt += 1
        HoudiniUtil.print_times("Total Render Nodes: %s" % simu_cunt)
        HoudiniUtil.print_times("Searching Render ROPS ...")
        rop_cunt=0
        for obj in hou.node('/').allSubChildren():
            nodes={}
            objPath = obj.path()
            objPath = objPath.replace('\\','/')
            objTypeName = obj.type().name()

            if objTypeName in ['ifd', 'arnold','Redshift_ROP']:
                render_rop_Node = hou.node(objPath)
                HoudiniUtil.print_times("   Render ROP: %s" % render_rop_Node)
                if i>0: info += '\n'
                info += objPath
                info += '|' + str(obj.evalParm('f1'))
                info += '|' + str(obj.evalParm('f2'))
                info += '|' + str(obj.evalParm('f3'))
                info += '|' + '-1'

                nodes["node"] = objPath
                pass_frame = str(int(obj.evalParm('f3'))) if int(obj.evalParm('f3'))>0 else "1"
                nodes["frames"] = "%s-%s[%s]" % (str(int(obj.evalParm('f1'))), str(int(obj.evalParm('f2'))), pass_frame)
                nodes["option"] = '-1'
                nodes["render"] = "0" if obj.isBypassed() else "1"
                rop_node.append(nodes)
                i+=1
                rop_cunt+=1
        HoudiniUtil.print_times("Total Render ROPs: %s" % rop_cunt)
        
        ## default frames
        default_frames = "%s-%s[%s]"%(str(hou.hscriptExpression("$FSTART")),str(hou.hscriptExpression("$FEND")),"1.0")
        scene_info = {"geo_node":geo_node,"rop_node":rop_node}
        self.Json_adict["scene_info"] = scene_info
        HoudiniUtil.WriteFile(self.Json_adict,self._cfg_task,'json')
        HoudiniUtil.print_times("Analysis & file end.")


    def Extued(self):
        
        self.DataSet()
        # self.configs()
        self.Custmset()
        self.GetAsses()

def HfsMmain():

    ## --------------------creat a job----------------------------
    hfs_obj = hfs_fileBase(args)
    HoudiniUtil.print_times('Load hip file start...')
    try:
        hfs_obj.loadhipfile()
    except :
        HoudiniUtil.print_times('Load hip ignore Errors.')
    HoudiniUtil.print_times('Load hip file end.')

    sys.stdout.flush()
    time.sleep(1)

    ## -----------------------------------------------------------

    HoudiniUtil.print_times('Jobs start...')
    HoudiniUtil.print_times('Job type: Analysis job ')
    hfs_obj.Extued()
    
    sys.stdout.flush()
    time.sleep(1)
    
    hfs_obj.analy_info()
        
    sys.stdout.flush()
    time.sleep(1)

    HoudiniUtil.print_times('Jobs end.')

if __name__=="__main__":

    print('...')
    print('-'*60)
    print('-'*60)
    print('Creat Houdini base information for running this Job, start Houdini_Files_Function...')
    print('...')    

    HfsMmain()
