#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import sys
import typing
import os
import subprocess
import time
import functools
from loguru import logger

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))

XRECORD = PATH('./xrecord')


def proc_output(cmd: str, decode=True):
    """subprocess.check_output()
    """
    try:
        res = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        logger.error(e)
        raise
    if decode:
        return res.decode()
    return res


def proc(cmd: str):
    """subprocess
    """
    return subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def start(proc_name: str, cmd: str, pre_kill: bool = True):
    """start a proc

    proc_name: proc_name keywords
    cmd: cmd
    pre_kill: before start whether kill or not, default True
    """
    if pre_kill:
        sigint(proc_name)
    logger.info(f'\n========== START RECORD ==========')
    return proc(cmd)


def stop(proc_name: str, _proc: subprocess.Popen):
    """stop a proc

    proc_name: proc_name keywords
    """
    try:
        assert _proc.poll() is None, f"run command failed"
        if sys.platform == "win32":
            _proc.terminate()
        else:
            _proc.send_signal(signal.SIGINT)
        logger.info(f'\n========== STOP RECORD ==========')
    except Exception as e:
        logger.error(e)
        sigint(proc_name)


def process_is_exist(process_name: str):
    cmd = "ps -ef | grep '%s' | grep -v 'grep' | awk '{print $2}'" % process_name
    if proc_output(cmd):
        return True
    else:
        return False


def sigint(process_name: str):
    """kill a specified proc by `kill -2 pid` == `os.kill(pid, signal.SIGINT)`,
    what you don't know proc pid

    `kill -9 pid` maybe cause saves error
    needed 1s after kill process
    """
    if process_is_exist(process_name):
        kill_cmd = "ps -ef | grep '%s' | grep -v 'grep' | awk '{print $2}' | xargs kill -2" % process_name
        proc(kill_cmd)
        time.sleep(1)
        logger.info(f'=== KILL PROCESS: {process_name} ===')


def _cmd(platform: str, **kwargs):
    """build cmd according to platform
    """
    platform = platform.lower()
    assert platform in ('a', 'android', 'i', 'ios'), f"platform should in ('a', 'android', 'i', 'ios')"
    if platform in ('a', 'android'):
        cmd = 'scrcpy -s "{device}" --render-expired-frames -Nr "{fp}"'.format(**kwargs)
        proc_name = 'scrcpy'
    else:
        cmd = '"{xrecord}" -q -i="{device}" -o="{fp}" -f'.format(xrecord=XRECORD, **kwargs)
        proc_name = 'xrecord'
    logger.info(
        f'\n===== CMD INFO ====='
        f'\nplatform: {platform}'
        f'\nname: {proc_name}'
        f'\ncmd: {cmd}'
        f'\n===================='
    )
    return proc_name, cmd


def _update_offset(
    offset: typing.Union[typing.Tuple[int], typing.Tuple[int, int]]
):

    assert isinstance(offset, tuple), 'offset type should be tuple'
    assert len(offset) <= 2, 'len(offset) should <= 2'
    offset = offset or (1, 1)
    offset = offset if len(offset) == 2 else (offset[0], 0)
    logger.info(f'current case offset: {offset}')
    return offset


def record(
        platform: typing.Union[str],
        device: typing.Union[str],
        file_path: typing.Union[str, os.PathLike],
        offset: typing.Tuple[int] = (1, 1),
        pre_kill: typing.Union[bool] = True
):
    """record wrapper

    platform: 'a', 'android', 'i', 'ios'
    device: platform of android device is device_id, platform of iOS device is device_name
    file_path: mp4 file path
    offset: default (1, 1), mean of: before record sleep 1s and after record sleep 1s
    pre_kill: before start whether kill or not, default True
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ofs = _update_offset(offset)
            proc_name, cmd = _cmd(platform, device=device, fp=file_path)
            p = start(proc_name, cmd, pre_kill)
            try:
                time.sleep(ofs[0])
                func(*args, **kwargs)
                time.sleep(ofs[1])
            except Exception as e:
                logger.error(e)
            finally:
                stop(proc_name, p)
        return wrapper
    return decorator
