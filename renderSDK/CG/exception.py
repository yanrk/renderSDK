# -*- coding:utf-8 -*-
class RayvisionError(Exception):
    pass


class MaxDamageError(RayvisionError):
    pass


class MaxExeNotExistError(RayvisionError):
    pass


class CGExeNotExistError(RayvisionError):
    pass


class ProjectMaxVersionError(RayvisionError):
    pass


class GetCGVersionError(RayvisionError):
    pass


class GetRendererError(RayvisionError):
    pass


class GetCGLocationError(RayvisionError):
    pass


class MultiscatterandvrayConfilictError(RayvisionError):
    pass


class VersionNotMatchError(RayvisionError):
    pass


class CGFileNotExistsError(RayvisionError):
    pass


class CGFileZipFailError(RayvisionError):
    pass


class CGFileNameIllegalError(RayvisionError):
    pass


class AnalyseFailError(RayvisionError):
    pass


class FileNameContainsChineseError(RayvisionError):
    pass


# class FileNotFoundError(RayvisionError):
#     pass
