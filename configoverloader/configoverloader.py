# -*- coding:utf-8 -*-

""" [NAME] ConfigOverLoader

[DESCRIPTION]
This module helps your management of configuration, when you would like to change it depends on env, role, node.

"""
import os
import socket
import logging


def default_node_detector():
    """
    try to get hostname
    :return: node name for check.
    """
    ret = []
    try:
        hostname = socket.gethostname()
        ret.append(hostname)
    except socket.error:
        pass

    try:
        fqdn = socket.getfqdn()
        if fqdn not in ret:
            ret.append(fqdn)
    except socket.error:
        pass

    if any(ret):
        return ret
    else:
        return None


def register_context(**default_dct):
    """
    :param default_dct: context to use
    """
    if default_dct.has_key("env"):
        _OveroaderCore.ov_default_context["env"] = default_dct["env"]

    if default_dct.has_key("role"):
        _OveroaderCore.ov_default_context["role"] = default_dct["role"]

    if default_dct.has_key("node"):
        _OveroaderCore.ov_default_context["node"] = default_dct["node"]


def get_context(env=None, role=None, node=None):
    misc = dict()
    if not env:
        if _OveroaderCore.ov_default_context["env"]:
            if callable(_OveroaderCore.ov_default_context["env"]):
                env = _OveroaderCore.ov_default_context["env"]()
            else:
                env = _OveroaderCore.ov_default_context["env"]
        else:
            env = None

    if not role:
        if _OveroaderCore.ov_default_context["role"]:
            if callable(_OveroaderCore.ov_default_context["role"]):
                role = _OveroaderCore.ov_default_context["role"]()
            else:
                role = _OveroaderCore.ov_default_context["role"]
        else:
            role = None
    if node is None:
        if _OveroaderCore.ov_default_context["node"]:
            if callable(_OveroaderCore.ov_default_context["node"]):
                if _OveroaderCore.ov_default_context["node"] == default_node_detector:
                    misc[_OveroaderCore._MISC_DEFAULT_NODE_DETECTOR_KEY] = True
                node = _OveroaderCore.ov_default_context["node"]()
            else:
                node = _OveroaderCore.ov_default_context["node"]
        else:
            node = None

    return {"env": env, "role": role, "node": node, "misc":misc}

def get_filenames(filename, env=None, role=None, node=None):
    """

    :param filename:  filename or file to process
    :param env:
    :param role:
    :param node:
    :return:
    """

    if isinstance(filename, file):
        filename = filename.name
        ov_files = [filename]
        context = get_context(env=env, role=role, node=node)
        ov_files.extend(_OveroaderCore.detect_override_files(filename, context))
        return ov_files

    elif isinstance(filename, list):
        context = get_context(env=env, role=role, node=node)
        ov_files = []
        for fname in filename:
            ov_files.append( fname)
            ov_files.extend(_OveroaderCore.detect_override_files(fname, context))
        return ov_files

    else:
        ov_files = [filename]
        context = get_context(env=env, role=role, node=node)
        ov_files.extend(_OveroaderCore.detect_override_files(filename, context))
        return ov_files


class _OveroaderCore:
    """
    Core class of this module
    """
    _OV_ENV_DIRNAME = 'env'
    _OV_ROLE_DIRNAME = 'role'
    _OV_NODE_DIRNAME = 'node'
    _OV_FORCE_DIRNAME = 'force'
    ov_default_context = {"env": None, "role": None, "node": default_node_detector}

    _MISC_DEFAULT_NODE_DETECTOR_KEY  = "default_node_detector"

    @classmethod
    def detect_override_files(cls, fpath, context):
        """
        :param fpath: original file-path
        :param context:
        :return: list of filepath to read
        """
        config_list = list()
        # detect file under env
        if context["env"]:
            env_file = cls._file_exists(fpath, _OveroaderCore._OV_ENV_DIRNAME, context["env"])
            if env_file:
                config_list.append(env_file)

        # multiple roles supported
        if context["role"]:
            if not isinstance(context["role"], list):
                roles = [context["role"]]
            else:
                roles = context["role"]
            for role in roles:
                role_file = cls._file_exists(fpath, _OveroaderCore._OV_ROLE_DIRNAME, role)
                if role_file:
                    config_list.append(role_file)

        # only 1st available file is read
        if context["node"]:
            if not isinstance(context["node"], list):
                node_names = [context["node"]]
            else:
                node_names = context["node"]

            for node_name in node_names:
                node_file = _OveroaderCore._file_exists(fpath, _OveroaderCore._OV_NODE_DIRNAME, node_name)
                if node_file:
                    if context["misc"].has_key(cls._MISC_DEFAULT_NODE_DETECTOR_KEY):
                        logging.getLogger(__name__).info("automatic node detection work. append:%s" % node_file)
                    config_list.append(node_file)
                    break

        force_file = _OveroaderCore._file_exists(fpath, _OveroaderCore._OV_FORCE_DIRNAME, None)
        if force_file:
            config_list.append(force_file)
            logging.getLogger(__name__).warn("force included file:%s" % force_file)

        return config_list

    @staticmethod
    def _file_exists(filename, dir_name, context_value):
        if context_value:
            override_file = os.path.join(os.path.dirname(filename), dir_name, context_value, os.path.basename(filename))
        else:
            override_file = os.path.join(os.path.dirname(filename), dir_name, os.path.basename(filename))
        if os.path.exists(override_file):
            return override_file
        else:
            return None

    @staticmethod
    def _dir_exists(fpath, dir_name, context_value):
        override_dir = os.path.join(os.path.dirname(fpath), dir_name, context_value)
        if os.path.isdir(override_dir):
            return True
        else:
            return False
