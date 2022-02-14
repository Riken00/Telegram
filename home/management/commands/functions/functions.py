from home.models import avds
import subprocess, logging
from pathlib import Path
from log import Log
import time

from log import Log
from conf import PRJ_PATH
from conf import LOG_LEVEL, LOG_DIR, LOG_IN_ONE_FILE


def set_log(prj_path, file_obj, name_obj, log_level=logging.DEBUG,
            log_dir='', log_suffix='.log'):
    _log_name = Path(file_obj).stem if name_obj == '__main__' else name_obj
    if not log_dir:
        _log_file = prj_path / (Path(file_obj).stem + log_suffix)
    else:
        _log_file = prj_path / log_dir / (Path(file_obj).stem + log_suffix)
    logger = Log(log_name=_log_name, log_level=log_level,
                 log_file=_log_file).logger

    return logger


def port_device():
    ports = list(
            filter(
                lambda y: not avds.objects.filter(port=y).exists(),
                map(
                    lambda x: 5550 + x, range(1, 500)
                )
            )
        )
    devices = list(
        filter(
            lambda y: not avds.objects.filter(name=y).exists(),
            map(
                lambda x: f"tiktok_avd_{x}", range(1, 500)
            )
        )
    )
    return ports,devices

LOGGER = set_log(PRJ_PATH, __file__, __name__, log_level=LOG_LEVEL,
        log_dir=LOG_DIR)

def log_activity(avd_id, action_type, msg, error):
    try:
        details = {
            "avd_id": avd_id,
            "action_type": action_type,
            "action": msg,
            "error": error,
        }
        LOGGER.debug(f'Log Activity: {details}')
    except Exception as e:
        print(e)


def run_cmd(cmd, verbose=True):
    """Run shell commands, and return the results

    ``cmd`` should be a string like typing it in shell.
    """
    try:
        if verbose:
            LOGGER.debug(f'Command: {cmd}')

        r = subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, shell=True, text=True)
        print(r)
        if verbose:
            if r.returncode == 0:
                LOGGER.debug(f'Successful to run the command: {cmd}')
                LOGGER.debug(f'Result of the command: {r.stdout}')
            else:
                LOGGER.warning(f'Failed to run the command: {cmd}')
                LOGGER.debug(f'Result of the command: {r.stdout}')

        return (r.returncode, r.stdout)
    except Exception as e:
        LOGGER.error(e)



def pkill_process_after_waiting(pname, success_code=0, retry_times=3,
                                sleep_time=1, verbose=True):
    """Using process name to kill a process"""
    # if the process exits normally, then kill it forcely
    search_pid_cmd = f'pgrep {pname}'
    if not run_cmd_loop(search_pid_cmd, success_code=success_code,
                        verbose=verbose):
        kill_cmd = f'pkill -9 {pname}'
        LOGGER.debug(f'Kill the process forcely: {pname}')
        run_cmd(kill_cmd, verbose=verbose)

def run_cmd_loop(cmd, success_code=0, retry_times=3, sleep_time=1,
                 verbose=True):
    """Run the command until beyond the retry times or successfully"""
    times = 0
    while times <= retry_times:
        result = run_cmd(cmd, verbose=verbose)
        if result:
            (status, output) = result
        else:
            times += 1
            if sleep_time > 0:
                time.sleep(sleep_time)
            LOGGER.debug(f'Retry to run the command: {cmd}')
            continue

        if status == success_code:
            return True
        else:
            times += 1
            if sleep_time > 0:
                time.sleep(sleep_time)
            LOGGER.debug(f'Retry to run the command: {cmd}')
            continue

    return False