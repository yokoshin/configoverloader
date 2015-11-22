# -*- coding:utf-8 -*-

""" [NAME] OverrideConfigParser

[DESCRIPTION] S
"""
import ConfigParser
import os
import socket
import logging


def default_node_detector():
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


def register_default_context(default_dct):
    if default_dct.has_key("env"):
        _OverloadCore.ov_default_context["env"] = default_dct["env"]

    if default_dct.has_key("role"):
        _OverloadCore.ov_default_context["role"] = default_dct["role"]

    if default_dct.has_key("node"):
        _OverloadCore.ov_default_context["node"] = default_dct["node"]


def get_default_context():
    if _OverloadCore.ov_default_context["env"]:
        if callable(_OverloadCore.ov_default_context["env"]):
            env = _OverloadCore.ov_default_context["env"]()
        else:
            env = _OverloadCore.ov_default_context["env"]
    else:
        env = None

    if _OverloadCore.ov_default_context["role"]:
        if callable(_OverloadCore.ov_default_context["role"]):
            role = _OverloadCore.ov_default_context["role"]()
        else:
            role = _OverloadCore.ov_default_context["role"]
    else:
        role = None

    if _OverloadCore.ov_default_context["node"]:
        if callable(_OverloadCore.ov_default_context["node"]):
            node = _OverloadCore.ov_default_context["node"]()
        else:
            node = _OverloadCore.ov_default_context["node"]
    else:
        node = None

    return {"env": env, "role": role, "node": node}


def glob(filenames, env=None, role=None, node=None):
    """first RawConfigParser.read
    Return list of successfully read files.
    """
    if isinstance(filenames, basestring):
        filenames = [filenames]

    if isinstance(filenames, file):
        raise IOError("bad args:%s. please pass filenames" % filenames)
    ov_filename = []
    context = _OverloadCore.merge_context(env=env, role=role, node=node)
    for filename in filenames:
        ov_filename.append(filename)
        ov_filename.extend(_OverloadCore.detect_override_files(filename, context))
    return ov_filename


def globfp(fp, filename=None, env=None, role=None, node=None):
    """process detected files after SafeConfigParser.fp
    """
    if filename is None:
        try:
            filename = fp.name
        except AttributeError:
            filename = None
    if filename:
        context = _OverloadCore.merge_context(env=env, role=role, node=node)
        ov_files = _OverloadCore.detect_override_files(filename, context)
    else:
        ov_files = []
    return ov_files


def glob_file(fp, source=None, env=None, role=None, node=None):
    return globfp(fp, filename=source)


class _OverloadCore:
    """
    TinyWrapper of Safe ConfigParser

    """
    _OV_ENV_DIRNAME = 'env'
    _OV_ROLE_DIRNAME = 'role'
    _OV_NODE_DIRNAME = 'node'
    _OV_FORCE_DIRNAME = 'force'

    ov_default_context = {"env": None, "role": None, "node": default_node_detector}

    @staticmethod
    def merge_context(env=None, role=None, node=None):
        context = get_default_context()
        if env:
            context["env"] = env
        if role:
            context["role"] = role
        if node:
            context["node"] = node
        return context

    @classmethod
    def detect_override_files(cls, fpath, context):
        config_list = list()
        # detect file under env
        if context["env"]:
            env_file = cls._file_exists(fpath, _OverloadCore._OV_ENV_DIRNAME, context["env"])
            if env_file:
                config_list.append(env_file)

        # multiple roles supported
        if context["role"]:
            if not isinstance(context["role"], list):
                roles = [context["role"]]
            else:
                roles = context["role"]
            for role in roles:
                role_file = cls._file_exists(fpath, _OverloadCore._OV_ROLE_DIRNAME, role)
                if role_file:
                    config_list.append(role_file)

        # only 1st available file is read
        if context["node"]:
            if not isinstance(context["node"], list):
                node_names = [context["node"]]
            else:
                node_names = context["node"]

            for node_name in node_names:
                node_file = _OverloadCore._file_exists(fpath, _OverloadCore._OV_NODE_DIRNAME, node_name)
                if node_file:
                    config_list.append(node_file)
                    break

        force_file = _OverloadCore._file_exists(fpath, _OverloadCore._OV_FORCE_DIRNAME, None)
        if force_file:
            config_list.append(force_file)
            logging.getLogger(__name__).warn("overrideconfig read:%s" % force_file)

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
