#!/usr/bin/env python
# -*-coding: utf-8 -*-

import os
import sys
import time
from .compat import *
from .RayvisionException import RayvisionError


class RayvisionAnalyse(object):
    def __init__(self, cg_id, cg_file, job_info, exe_path=None):
        self.cg_id = cg_id
        self.cg_file = cg_file
        self.job_info = job_info
        self.custom_exe_path = exe_path
        self.cg_instance = self.create_instance()

    def create_instance(self):
        if not os.path.exists(self.cg_file):
            raise RayvisionError(1000000, "Cg file does not exist: {0}".format(self.cg_file))

        if self.custom_exe_path is not None:
            if not os.path.isabs(self.custom_exe_path):
                raise RayvisionError(1000000, "Please specify the exe full path")
            if not os.path.isfile(self.custom_exe_path):
                raise RayvisionError(1000000, "The specified exe path does not exist")

        cg_instance = None
        cg_id = self.cg_id
        param_dict = {
            'cg_id': self.cg_id,
            'cg_file': self.cg_file,
            'job_info': self.job_info,
            'custom_exe_path': self.custom_exe_path
        }
        
        if cg_id == '2000':
            from .CG.cg_maya.cg import Maya
            cg_instance = Maya(**param_dict)
        elif cg_id == '2001':
            from .CG.cg_max.cg import Max
            cg_instance = Max(**param_dict)
        elif cg_id == '2002':
            from .CG.cg_lightwave.cg import Lightwave
            cg_instance = Lightwave(**param_dict)
        elif cg_id == '2003':
            from .CG.cg_arnold.cg import Arnold
            cg_instance = Arnold(**param_dict)
        elif cg_id == '2004':
            from .CG.cg_houdini.cg import Houdini
            cg_instance = Houdini(**param_dict)
        elif cg_id == '2005':
            from .CG.cg_c4d.cg import C4D
            cg_instance = C4D(**param_dict)
        elif cg_id == '2006':
            from .CG.cg_softimage.cg import Softimage
            cg_instance = Softimage(**param_dict)
        elif cg_id == '2007':
            from .CG.cg_blender.cg import Blender
            cg_instance = Blender(**param_dict)
        elif cg_id == '2008':
            from .CG.cg_vray.cg import Vray
            cg_instance = Vray(**param_dict)
        elif cg_id == '2009':
            from .CG.cg_mrstand.cg import Mrstand
            cg_instance = Mrstand(**param_dict)
        elif cg_id == '2010':
            from .CG.cg_sketchup.cg import SketchUp
            cg_instance = SketchUp(**param_dict)
        elif cg_id == '2011':
            from .CG.cg_vue.cg import VUE
            cg_instance = VUE(**param_dict)
        elif cg_id == '2012':
            from .CG.cg_keyshot.cg import Keyshot
            cg_instance = Keyshot(**param_dict)
        elif cg_id == '2013':
            from .CG.cg_clarisse.cg import Clarisse
            cg_instance = Clarisse(**param_dict)
        elif cg_id == '2014':
            from .CG.cg_octane.cg import Octane
            cg_instance = Octane(**param_dict)
        elif cg_id == '2015':
            from .CG.cg_nuke.cg import Nuke
            cg_instance = Nuke(**param_dict)
        elif cg_id == '2016':
            from .CG.cg_katana.cg import Katana
            cg_instance = Katana(**param_dict)
        else:
            raise RayvisionError(1000000, "The cg_id does not exist!")
        
        return cg_instance

    @classmethod
    def execute(cls, cg_id, cg_file, job_info, exe_path=None):
        """
        Entrance.
        :param str cg_id: see RayvisionUtil
        :param cg_file: scene file
        :param job_info: 
        :param exe_path: The user can manually specify the exe path of the cg software. If you have one, use this path directly, if not, find it yourself. # TODO "Use this path directly" (1/4)
        :return:
        """
        self = cls(cg_id, cg_file, job_info, exe_path)
        self.run()

    def run(self):
        """The whole process"""
        self.cg_instance.run()

    def analyse_cg_file(self):
        self.cg_instance.analyse_cg_file()

    def analyse(self):
        self.cg_instance.analyse()


def init_argparse():
    pass


def main():
    init_argparse()


if __name__ == '__main__':
    main()
