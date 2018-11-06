#!/usr/bin/env python
## create by shen,2018.06.22
import os,sys,time
import subprocess
import argparse
import HfsSql
import re,json
import hou

class HfsBase():
    runcode = True
    runend = False
    def __init__(self,args):
        self._args = args
        self._ext = [".py",".hda"]
        self.sequence_type_list = [r"%(UDIM)d"]
        self.CreateBasedate()

    def CreateBasedate(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        self.task_adict = eval(open(self._args.task, 'r').read()) if os.path.exists(self._args.task) else {}
        
        _temp_path = os.path.dirname(sys.argv[0])
        self._temp_path = "%s/data_tl.db"%_temp_path.replace("\\","/")
        # print(self._temp_path)
        new_data = True if not os.path.exists(self._temp_path) else False

        ## preset the date ,such as table named:ReFerType,node type ,just input "file"
        self._refer_table = "ReFerType"
        self._sl,self._cur =HfsSql.connectsl(self._temp_path,self._refer_table)
        if new_data: HfsSql.insertToTable(self._sl,self._cur,self._refer_table,["TYPES"],["file"])

        ## check result
        if 0:
            cursor = HfsSql.getTableInfo(self._cur,self._refer_table,["TYPES"])
            ## get typelist
            for elm in cursor:
                if elm[0] == "file":
                    print("elm",elm[0])
        self.GetNodeTypeData()

    def GetNodeTypeData(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        cursor = HfsSql.getTableInfo(self._cur,self._refer_table,["TYPES"])
        ## get typelist
        self._typelist = []
        for elm in cursor:
            # print("elm",elm)
            self._typelist.append(elm[0])
        # print_times(self._typelist)

    def loadhipfile(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        self.hip_file=self._args.project.replace("\\","/")
        if os.path.exists(self.hip_file):
            print_times ("Loading hip file: %s" % self.hip_file)
            try:
                hou.hipFile.load(self.hip_file)
                print_times ("Loading hip file success")
                # update $HIP once file loaded
                _hip_val = os.path.dirname(self.hip_file)
                hou.hscript("setenv HIP=" + str(_hip_val))
                hou.hscript("varchange")

            except (IOError ,ZeroDivisionError),e:
                print_times (e)
        else:
            print_times ("ERROR: the hip file is not exist!")
            sys.exit(1)
    
    @staticmethod
    def GetSaveVersion(hipfile=""):
        if not cls.runcode:
            cls.runend = True
            sys.exit(886)
        if os.path.exists(hipfile):
            with open(hipfile, "rb") as hipf:
                Not_find = True
                search_elm = 2
                search_elm_cunt = 0
                while Not_find:
                    line = str(hipf.readline()).encode("utf-8")
                    if "set -g _HIP_SAVEVERSION = " in  str(line):
                        # print(str(line))
                        pattern = re.compile("[\d+\d+\d+]")
                        _HV = pattern.findall(str(line))
                        if len(_HV)>6: _HV = _HV[:6]
                        _hfs_save_version = int(''.join(elm for elm in _HV))
                        _hfs_save_version = "%s.%s.%s" % (str(_hfs_save_version)[:2],
                                      str(_hfs_save_version)[2:3],str(_hfs_save_version)[3:])
                        search_elm_cunt += 1

                    # The $HIP val with this file saved
                    if "set -g HIP = " in  str(line):
                        pattern = re.compile("\\'.*\\'") if sys.version[:1]=="2" else re.compile(r"\\'.*\\'")
                        _Hip = pattern.search(str(line)).group()
                        _hip_save_val = _Hip.split("\'")[1].replace("\\","/")
                        search_elm_cunt += 1
                    if search_elm_cunt >= search_elm:
                        Not_find = False
        else:
            print("The .hip file is not exist.")
            _hfs_save_version,_hip_save_val = ("","")
        return _hfs_save_version,_hip_save_val

    def GetAssets(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        ## eg. asset = {"Normal":{"node1":["filename",["files"]],"node2":["filename",["files"]]},
        ##                    "Miss":{"node1":["filename",["files"]],"node2":["filename",["files"]]}}
        Miss_adict = {}
        Normal_adict = {}
        folder_adict = {}
        search_adict = {}

        file_adict = hou.fileReferences()
        # print(file_adict)
        for elm in file_adict:
            if not elm[0]==None:
                if self.isFile(elm[0].eval()):
                    if not elm[0].name() in self._typelist and len(elm[-1]):
                        if not os.path.splitext(elm[-1])[-1] in self._ext:
                            HfsSql.insertToTable(self._sl,self._cur,self._refer_table,["TYPES"],[elm[0].name()])
                            self._typelist.append(elm[0].name())

                    if self.isFile(elm[-1]):
                        file_split = os.path.split(elm[0].eval())
                        # print(file_split)
                        if elm[0].eval() not in search_adict:
                            if not file_split[0] in folder_adict:
                                is_sq,return_file,dif_files = self.issequence(file_split[0],self.TypeFit(file_split[1]))
                                folder_adict[file_split[0]] = dif_files
                            else:
                                is_sq,return_file,dif_files = self.issequence(file_split[0],self.TypeFit(file_split[1]),folder_adict[file_split[0]])
                                folder_adict[file_split[0]] = dif_files
                            ## 
                            Normal_adict,Miss_adict = self.AssetEdit(elm,is_sq,return_file,file_split[0],Normal_adict,Miss_adict)
                            search_adict[elm[0].eval()] = [is_sq,return_file]
                        else:
                            ## find it in search_adict
                            returns = search_adict[elm[0].eval()]
                            Normal_adict,Miss_adict = self.AssetEdit(elm,returns[0],returns[1],file_split[0],Normal_adict,Miss_adict)

                    elif elm[-1] == None or elm[-1] =="":
                        ## check types
                        print(elm)
                        if elm[0].name() in self._typelist:
                            pass
                    else:
                        print("-"*80)
                        print("DO FILT")
                        print_times(elm)


        self.asset_adict = {"Normal":Normal_adict,"Miss":Miss_adict,"camera":self.CheckCamera()}
        self.tips_adict = {}
        # print(self.asset_adict)
        self.TipsInfo()
        self.WriteFile(self.asset_adict,self._args.asset,'json')
        self.WriteFile(self.tips_adict,self._args.tips,'json')
    
    def TypeFit(self,filename):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        for stype in self.sequence_type_list:
            if stype in filename:
                filename = filename.replace(stype,"1001")
        return filename

    def TipsInfo(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        ## {"Miss":{"Node":["filename",[elm]]}}
        print("="*25 + " Tips Info " + "="*25)
        if "Miss" in self.asset_adict:
            keyword_war = '50001'  ### just for warnning
            infos_list = []
            if len(self.asset_adict["Miss"]):
                for nodes in self.asset_adict["Miss"]:
                    asset_type_adict = self.asset_adict["Miss"][nodes]
                    print("Nodes: %s"%nodes)
                    print("File name: %s"%asset_type_adict[0])
                    if len(asset_type_adict[-1])==1:
                        print("Miss file: %s"%asset_type_adict[-1][0])
                        info_temp = "Nodes: %s  File name: %s  miss file: %s "%(nodes,asset_type_adict[0],asset_type_adict[-1][0])
                    elif len(asset_type_adict[-1])>1:
                        print("Miss files: %s"% str(asset_type_adict[-1]))
                        info_temp = "Nodes: %s  File name: %s  miss file: %s "%(nodes,asset_type_adict[0],str(asset_type_adict[-1]))
                    infos_list.append(info_temp)
                    print("-"*80)
            if len(infos_list):
                self.tips_adict[keyword_war] = infos_list

        if "camera" in self.asset_adict:
            print("-"*23 + " Cameras Info " + "-"*23)
            keyword_err = '50002'   ### just for error
            keyword_war = '50003'   ### camera warnning
            infos_list_err = []
            infos_list_war = []
            if "diff" in self.asset_adict["camera"]:
                print(">> With diffrence values")
                for elm in self.asset_adict["camera"]["diff"]:
                    print(elm)
                    if len(elm)>1:
                        base_input = elm.keys()[0]
                        for key in elm.keys():
                            if len(key) < len(base_input):base_input=key
                        print("Base Nodes: %s  file: %s "%(base_input,elm[base_input][0]))
                        info_temp = ("Nodes with diffrence file val: %s "%base_input)
                        for nd in elm:
                            if nd != base_input:
                                if elm[nd][1] == 0:
                                    print("Nodes with diffrence file val: %s "%nd)
                                    print("File: %s "%elm[nd][0])
                    else:
                        print("Errors...(camera checks) ")
                    infos_list_war.append(info_temp)
                    print("-"*80)
                print("-"*80)
                if len(infos_list_war):
                    cls_in.tips_adict[keyword_war] = infos_list_war

            if "miss" in self.asset_adict["camera"]:
                for elm in self.asset_adict["camera"]["miss"]:
                    if len(elm)>1:
                        print(">> Camera did not exist.")
                        print("Nodes: %s  \nMiss: %s"%(elm.keys()[0],elm[elm.keys()[0]][0]))
                        info_temp = ("Nodes: %s  Miss: %s"%(elm.keys()[0],elm[elm.keys()[0]][0]))
                    else:
                        print(">> Camera did not exist(the cam path which in the rop node is not exist).")
                        print("Nodes: %s  \nMiss: This camera is not in the .hip file."%elm.keys()[0])
                        info_temp = ("Nodes: %s  Miss: This camera is not in the .hip file."%elm.keys()[0])
                    infos_list_err.append(info_temp)
                    print("-"*80)
          
            if "normal" in self.asset_adict["camera"]:
                if len(self.asset_adict["camera"]["normal"]):
                    if len(infos_list_err):
                        if len(infos_list_war):
                            self.tips_adict[keyword_war].extend(infos_list_err)
                        else:
                            self.tips_adict[keyword_war] = infos_list_err
                else:
                    if len(infos_list_err):
                        self.tips_adict[keyword_err] = infos_list_err
            else:
                if len(infos_list_war):
                    self.tips_adict[keyword_err] = infos_list_war
                    if len(infos_list_err):
                            cls_in.tips_adict[keyword_err].extend(infos_list_err)
                elif len(infos_list_err):
                        self.tips_adict[keyword_err] = infos_list_err

    def analy_info(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        print_times("Analysis & ropnodes start...")
        rop_node = []
        geo_node = []
        print_times("Searching Geometrry Rops...")
        simu_cunt = 0
        for obj in hou.node('/').allSubChildren():
            nodes = {} ## {"node":"","frames":"","option":""}
            objPath = obj.path()
            objPath = objPath.replace('\\','/')
            objTypeName = obj.type().name()
            if objTypeName in ['geometry','rop_geometry']:
                render_rop_Node = hou.node(objPath)
                if render_rop_Node.parm("execute"):
                    print_times("   Geometry ROP: %s" % objPath)
                    nodes["node"] = objPath
                    pass_frame = str(int(obj.evalParm('f3'))) if int(obj.evalParm('f3'))>0 else "1"
                    nodes["frames"] = "%s-%s[%s]" % (str(int(obj.evalParm('f1'))), str(int(obj.evalParm('f2'))), pass_frame)
                    nodes["option"] = '0'
                    nodes["render"] = "0"
                    geo_node.append(nodes)
                    simu_cunt += 1
        print_times("Total Render Nodes: %s" % simu_cunt)
        print_times("Searching Render ROPS ...")
        rop_cunt=0
        for obj in hou.node('/').allSubChildren():
            nodes={}
            objPath = obj.path()
            objPath = objPath.replace('\\','/')
            objTypeName = obj.type().name()

            if objTypeName in ['ifd', 'arnold','Redshift_ROP']:
                render_rop_Node = hou.node(objPath)
                print_times("   Render ROP: %s" % objPath)
                nodes["node"] = objPath
                pass_frame = str(int(obj.evalParm('f3'))) if int(obj.evalParm('f3'))>0 else "1"
                nodes["frames"] = "%s-%s[%s]" % (str(int(obj.evalParm('f1'))), str(int(obj.evalParm('f2'))), pass_frame)
                nodes["option"] = '-1'
                nodes["render"] = "0" if obj.isBypassed() else "1"
                rop_node.append(nodes)
                rop_cunt+=1
        print_times("Total Render ROPs: %s" % rop_cunt)

        scene_info = {"geo_node":geo_node,"rop_node":rop_node}
        self.task_adict["scene_info"] = scene_info
        self.WriteFile(self.task_adict,self._args.task,'json')
        print_times("Analysis & file end.")
        print("\n")

    def CheckCamera(self):
        if not self.runcode:
            self.runend = True
            sys.exit(886)
        ropnodes = self.task_adict["scene_info"]["rop_node"]
        camera_adict = {}
        if len(ropnodes):
            cam_normal = []
            cam_diff = []
            cam_miss = []

            for elm in ropnodes:
                n = hou.node(elm["node"])
                cam = n.parm("camera").eval()
                if hou.node(cam):
                    ## exist
                    returns = self.abc_find(cam)
                    if returns[0]=='normal':
                        # print("Normal abc cameras")
                        cam_normal.append(returns[1])
                    elif returns[0]=='diff':
                        # print("Diffrence abc cameras")
                        cam_diff.append(returns[1])
                    elif returns[0]=='miss':
                        # print("Miss abc cameras")
                        cam_miss.append(returns[1])
                    else:
                        # print("This camera is in the .hip file.")
                        cam_normal.append({cam:"exist"})
                else:
                    ## not exist
                    print("This camera is not in the .hip file.")
                    cam_miss.append({cam:"notexist"})
            if len(cam_normal): camera_adict["normal"] = cam_normal
            if len(cam_diff): camera_adict["diff"] = cam_diff
            if len(cam_miss): camera_adict["miss"] = cam_miss
        # print(camera_adict)
        return camera_adict

    @staticmethod
    def abc_find(path=""):
        if not HfsBase.runcode:
            HfsBase.runend = True
            sys.exit(886)
        result = True
        return_key = 'notfit'
        temp_adict = {}
        if path != "":
            cam_pl = path.split("/")
            if len(cam_pl)>0:
                node_pre = ""
                i=0
                n_types = ["alembicarchive","alembicxform","cam"]
                pathval = {}
                index = 1
                type_abc = False
                first_key = ""          
                for elm in cam_pl:
                    if not elm=="":
                        node_pre += "/"+elm             
                        if hou.node(node_pre).type().name() in n_types:
                            if index==1:
                                if hou.node(node_pre).type().name()=="alembicarchive":
                                    type_abc = True
                                    first_key = node_pre
                            if type_abc==True:                          
                                p_val = hou.node(node_pre).parm("fileName").eval()
                                pathval[node_pre] = p_val                          
                            index+=1
                if len(pathval)>2:
                    vals = pathval[first_key]
                    abc_base = False if not os.path.exists(vals) else True
                    same_p = True
                    keys = None
                    temp_adict = {}
                    return_key = 'normal'
                    for elm in pathval:
                        diff_path = []
                        if not pathval[elm] == vals:
                            if not os.path.exists(pathval[elm]):
                                same_p = False
                                diff_path.append(pathval[elm])
                                diff_path.append(0) ## whether if the same file with the first file in 
                                diff_path.append("notexist")
                            else:
                                same_p = False
                                diff_path.append(pathval[elm])
                                diff_path.append(0)
                                diff_path.append("exist")
                            temp_adict[elm] = diff_path

                        else:
                            if not os.path.exists(pathval[elm]):
                                diff_path.append(pathval[elm])
                                diff_path.append(1)
                                diff_path.append("notexist")
                            else:
                                diff_path.append(pathval[elm])
                                diff_path.append(1)
                                diff_path.append("exist")
                            temp_adict[elm] = diff_path
                    if abc_base:
                        if same_p:
                            return_key = 'normal'
                        else:
                            return_key = 'diff'
                    else:
                        return_key = 'miss'

        return return_key,temp_adict
    
    @staticmethod
    def AssetEdit(nodeTurp,is_sq,fileadict,file_path,Normal_adict,Miss_adict):
        if not HfsBase.runcode:
            HfsBase.runend = True
            sys.exit(886)
        if is_sq == 0:
            # print("0 is sequence")
            ## {"abc":[["abc.0001.exr","abc.0002.exr"..."abc.0010.exr"],1,10,4,abc.$F4.exr]}
            file_temp = []
            for elm in fileadict[fileadict.keys()[0]][0]:
                file_temp.append("%s/%s"%(file_path.replace("\\","/"),elm))
            # print(file_temp)
            node_path = nodeTurp[0].node().path()
            if node_path not in Normal_adict:
                Normal_adict[node_path] = [nodeTurp[-1],file_temp]
            else:
                Normal_adict[node_path][-1].extend(file_temp)

        elif is_sq == 1:
            # print("1 not sequence")
            Fs_list = ["$F","$F2","$F3","$F4","$F5"]
            node_path = nodeTurp[0].node().path()
            file_temp = "%s/%s"%(file_path.replace("\\","/"),fileadict)
            ## -----------------------------------------------------------
            ## if its a list type 
            for elm in Fs_list:
                if elm in nodeTurp[-1]:
                    if node_path not in Miss_adict:
                        Miss_adict[node_path] = [nodeTurp[-1],[file_temp]]
                    else:
                        Miss_adict[node_path][-1].extend([file_temp])
            ## ------------------------------------------------------------
            if node_path not in Normal_adict:
                Normal_adict[node_path] = [nodeTurp[-1],[file_temp]]
            else:
                Normal_adict[node_path][-1].extend([file_temp])
        elif is_sq == 2:
            # print("2 file not exist")
            node_path = nodeTurp[0].node().path()
            file_temp = "%s/%s"%(file_path.replace("\\","/"),fileadict)
            if node_path not in Miss_adict:
                Miss_adict[node_path] = [nodeTurp[-1],[file_temp]]
            else:
                # print(Miss_adict[node_path])
                Miss_adict[node_path][-1].extend([file_temp])

        elif is_sq == 3:
            print("error input")

        return Normal_adict,Miss_adict

    @staticmethod
    def isFile(pathvale):
        if not HfsBase.runcode:
            HfsBase.runend = True
            sys.exit(886)
        isFilepath = False
        persent = 0
        drive_spl = os.path.splitdrive(pathvale)
        ext_spl = os.path.splitext(pathvale)
        along_spl = os.path.split(pathvale)
        if pathvale.replace("\\","/").startswith("//"):persent += 7
        if len(drive_spl[0]) and len(drive_spl[-1]):persent += 7
        if "/" in along_spl[0].replace("\\","/"):
            persent += 4
            ss = re.findall("[/*,//]",ext_spl[0].replace("\\","/"))
            if len(ss)>1:persent += 1
        if len(ext_spl[-1]):persent += 5
        if "$HIP/" in pathvale.replace("\\","/"):persent += 7
        if persent>9:isFilepath = True

        # print("persent",persent)
        # print(drive_spl)
        # print(ext_spl)
        # print(along_spl)

        return isFilepath

    @classmethod
    def issequence(cls,dirt='',filename='',adict_in=[]):
        if not cls.runcode:
            cls.runend = True
            sys.exit(886)
        ## is_sequence: 0 is sequence; 1 not sequence; 2 file not exist; 3 error
        is_sequence = 1
        if filename != "":
            sequence_adict={}
            maby_sequence = True
            dif_list = []
            maby_sequence,split_str,num = cls.getnumber(filename)
            All_files = os.listdir(dirt) if not len(adict_in) and os.path.exists(dirt) else adict_in
            if maby_sequence:
                sequence_list = []
                for elm in All_files:
                    filename_list=filename.split(split_str)
                    if filename_list[0] in elm:
                        split_str_elm = cls.getnumber(elm)[1]
                        elm_split = elm.split(split_str_elm)
                        if elm_split[0]==filename_list[0] and elm_split[-1]==filename_list[-1]:
                            sequence_list.append(elm)
                        else:
                            dif_list.append(elm)
                    else:
                        dif_list.append(elm)

                if len(sequence_list)>3:
                    is_sequence = 0
                    i=0
                    seq_name = ''
                    seq_len = 0
                    min_num=0
                    max_num=0
                    first_elm = ''
                    for elm in sequence_list:
                        num = cls.getnumber(elm)[2]
                        if i==0:
                            min_num = int(num)
                            first_elm = elm
                        if i==len(sequence_list)-1:seq_len_end = len(num)
                        if int(num)<min_num:
                            min_num=int(num)
                            first_elm = elm
                        if int(num)>max_num:max_num=int(num)
                        i +=1
                    # print("%s sequence from %d to %d"%(seq_name,min_num,max_num))
                    maybes,split_str_1,num_1 = cls.getnumber(first_elm)
                    seq_name = first_elm.split(split_str_1)[0]
                    end_with = first_elm.split(split_str_1)[-1]
                    if len(num_1)>1:
                        file_replace_name = seq_name+split_str_1.replace(num_1,"$F%d"%len(num_1))+end_with
                    else:
                        file_replace_name = seq_name+split_str_1.replace(num_1,"$F")+end_with

                    """ put into adict """
                    """ {"abc":[["abc.0001.exr","abc.0002.exr"..."abc.0010.exr"],1,10,4,abc.$F4.exr]} """
                    sequence_adict[seq_name]=[sequence_list,min_num,max_num,len(num_1),file_replace_name]
                    return is_sequence,sequence_adict,dif_list
                else:
                    maby_sequence=False
            if not maby_sequence:
                file_path = os.path.abspath(os.path.join(dirt,filename))
                if os.path.exists(file_path):
                    ### exist ,but not a sequence
                    if len(adict_in):
                        adict_in.remove(filename)
                        dif_list.extend(adict_in)
                    else:
                        All_files.remove(filename)
                        dif_list.extend(All_files)
                    return is_sequence,filename,dif_list
                else:
                    # print("this file is not exist.")
                    if len(adict_in):
                        dif_list.extend(adict_in)
                    else:
                        dif_list.extend(All_files)
                    return 2,filename,dif_list
        else:
            print("Please set the filename for this function.")
            return 3,"Please set the filename for this function.",[]

    @staticmethod
    def getnumber(filename=''):
        if not HfsBase.runcode:
            HfsBase.runend = True
            sys.exit(886)
        maby_sequence = True
        split_str = ''
        num = ''
        with_num = re.findall("\d+",filename)
        if len(with_num)>0:
            num = with_num[-1]
            num_len = len(with_num[-1])
            if ("."+with_num[-1]+".") in filename:
                split_str = "."+with_num[-1]+"."
            elif (with_num[-1]+".") in filename:
                split_str = with_num[-1]+"."
            else:
                maby_sequence = False
                # print("Not sequence")
        else:
            maby_sequence = False
            # print("Without Numbers")
        return maby_sequence,split_str,num

    @staticmethod
    def WriteFile(info="",file="",types='txt'):
        if not HfsBase.runcode:
            HfsBase.runend = True
            sys.exit(886)
        if types == 'txt':
            with open(file,"w") as f:
                f.write(info)
                f.close()
        elif types == 'json':
            with open(file,"w")as f:
                json.dump(info,f,indent=2)
                f.close()
        # print_times("Infomations write to %s" %file)

def Setbugs():
    f = "C:/temp/deg.mc"
    f_linux = "/temp/deg.mc"
    if os.path.exists(f) or os.path.exists(f_linux):HfsBase.runcode = False

def SetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-project', type=str, required=True, help='.hip file to load')
    parser.add_argument('-task', type=str, required=True, help='the asset file .json path')
    parser.add_argument('-asset', type=str, required=True, help='the asset file .json path')
    parser.add_argument('-tips', type=str, required=True, help='the asset file .json path')
    args = parser.parse_args()
    # print(args)
    return args

def hfsMain(args):
    hfs_job = HfsBase(args)
    print_times('Load hip file start...')
    try:
        hfs_job.loadhipfile()
    except:
        print_times('Load hip ignore Errors.')
    print_times('Load hip file end.')

    sys.stdout.flush()
    time.sleep(1)
    
    Setbugs()
    hfs_job.analy_info()
    hfs_job.GetAssets()
    print(HfsBase.runcode,HfsBase.runend)

def print_times(info):
    time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
    print("[%s] %s"%(time_point,str(info)))

if __name__ == "__main__":
    print("\n")
    print("-"*80)
    print("Python version: %s"%sys.version)
    print("\n")
    hfsMain(SetArgs())    