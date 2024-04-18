import datetime
import json
import os
import os.path as osp
import random
import re
import subprocess
import sys
import time
from functools import partial
from typing import Any, Dict, List, Optional, Tuple

import mmengine
from mmengine.config import ConfigDict
from mmengine.utils import track_parallel_progress

from opencompass.registry import RUNNERS, TASKS
from opencompass.utils import get_logger

from .base import BaseRunner


@RUNNERS.register_module()
class DLCRunner(BaseRunner):
    """Distributed runner based on Alibaba Cloud Deep Learning Cluster (DLC).
    It will launch multiple tasks in parallel with 'dlc' command. Please
    install and configure DLC first before using this runner.

    Args:
        task (ConfigDict): Task type config.
        aliyun_cfg (ConfigDict): Alibaba Cloud config.
        max_num_workers (int): Max number of workers. Default: 32.
        retry (int): Number of retries when job failed. Default: 2.
        debug (bool): Whether to run in debug mode. Default: False.
        lark_bot_url (str): Lark bot url. Default: None.
    """

    def __init__(self,
                 task: ConfigDict,
                 aliyun_cfg: ConfigDict,
                 max_num_workers: int = 32,
                 eval_with_gpu: list = ['plugin_eval'],
                 retry: int = 2,
                 debug: bool = False,
                 lark_bot_url: str = None):
        super().__init__(task=task, debug=debug, lark_bot_url=lark_bot_url)
        self.aliyun_cfg = aliyun_cfg
        self.max_num_workers = max_num_workers
        self.retry = retry

        self.eval_with_gpu = eval_with_gpu

        logger = get_logger()
        logger.warning(
            'To ensure the integrity of the log results, the log displayed '
            f'by {self.__class__.__name__} has a 10-second delay.')

    def launch(self, tasks: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
        """Launch multiple tasks.

        Args:
            tasks (list[dict]): A list of task configs, usually generated by
                Partitioner.

        Returns:
            list[tuple[str, int]]: A list of (task name, exit code).
        """

        if not self.debug:
            status = track_parallel_progress(self._launch,
                                             tasks,
                                             nproc=self.max_num_workers,
                                             keep_order=False)
        else:
            status = [self._launch(task, random_sleep=False) for task in tasks]
        return status

    def _launch(self, cfg: ConfigDict, random_sleep: Optional[bool] = None):
        """Launch a single task.

        Args:
            cfg (ConfigDict): Task config.
            random_sleep (bool): Whether to sleep for a random time before
                running the command. When Aliyun has many tasks to schedule,
                its stability decreases. Therefore, when we need to submit a
                large number of tasks at once, we adopt the "random_sleep"
                strategy. Tasks that would have been submitted all at once are
                now evenly spread out over a 10-second period. Default: None.

        Returns:
            tuple[str, int]: Task name and exit code.
        """
        if random_sleep is None:
            random_sleep = (self.max_num_workers > 32)

        task = TASKS.build(dict(cfg=cfg, type=self.task_cfg['type']))
        num_gpus = task.num_gpus
        task_name = task.name

        is_eval_task = 'OpenICLEval' in task_name
        if is_eval_task and num_gpus == 0:
            for check_name in self.eval_with_gpu:
                if check_name in task_name:
                    num_gpus = 1
                    break

        # Dump task config to file
        mmengine.mkdir_or_exist('tmp/')
        param_file = f'tmp/{os.getpid()}_params.py'
        pwd = os.getcwd()
        try:
            cfg.dump(param_file)
            if self.aliyun_cfg.get('bashrc_path') is not None:
                # using user's conda env
                bashrc_path = self.aliyun_cfg['bashrc_path']
                assert osp.exists(bashrc_path)
                assert self.aliyun_cfg.get('conda_env_name') is not None
                conda_env_name = self.aliyun_cfg['conda_env_name']
                shell_cmd = (f'source {bashrc_path}; '
                             f'conda activate {conda_env_name}; ')
            else:
                # using public conda env
                # users can also set `python_env_path` to their
                # own env python path
                assert self.aliyun_cfg.get('python_env_path') is not None
                shell_cmd = (
                    f'export PATH={self.aliyun_cfg["python_env_path"]}/bin:$PATH; '  # noqa: E501
                    f'export PYTHONPATH={pwd}:$PYTHONPATH; ')

            huggingface_cache = self.aliyun_cfg.get('huggingface_cache')
            if huggingface_cache is not None:
                # HUGGINGFACE_HUB_CACHE is a Legacy env variable, here we set
                # `HF_HUB_CACHE` and `HUGGINGFACE_HUB_CACHE` for bc
                shell_cmd += f'export HF_HUB_CACHE={huggingface_cache}; '
                shell_cmd += f'export HUGGINGFACE_HUB_CACHE={huggingface_cache}; '  # noqa: E501

            torch_cache = self.aliyun_cfg.get('torch_cache')
            if torch_cache is not None:
                shell_cmd += f'export TORCH_HOME={torch_cache}; '

            hf_offline = self.aliyun_cfg.get('hf_offline', True)
            if hf_offline:
                shell_cmd += 'export HF_DATASETS_OFFLINE=1; export TRANSFORMERS_OFFLINE=1; export HF_EVALUATE_OFFLINE=1; '  # noqa: E501

            http_proxy = self.aliyun_cfg.get('http_proxy')
            if http_proxy is not None:
                shell_cmd += f'export http_proxy={http_proxy}; export https_proxy={http_proxy}; '  # noqa: E501
                shell_cmd += f'export HTTP_PROXY={http_proxy}; export HTTPS_PROXY={http_proxy}; '  # noqa: E501

            hf_endpoint = self.aliyun_cfg.get('hf_endpoint')
            if hf_endpoint is not None:
                shell_cmd += f'export HF_ENDPOINT={hf_endpoint}; '

            shell_cmd += f'cd {pwd}; '
            shell_cmd += '{task_cmd}'

            tmpl = ('dlc create job'
                    f" --command '{shell_cmd}'"
                    f' --name {task_name[:512]}'
                    ' --kind BatchJob'
                    f" -c {self.aliyun_cfg['dlc_config_path']}"
                    f" --workspace_id {self.aliyun_cfg['workspace_id']}"
                    ' --worker_count 1'
                    f' --worker_cpu {max(num_gpus * 8, 32)}'
                    f' --worker_gpu {num_gpus}'
                    f' --worker_memory {max(num_gpus * 128, 256)}'
                    f" --worker_image {self.aliyun_cfg['worker_image']}")
            get_cmd = partial(task.get_command,
                              cfg_path=param_file,
                              template=tmpl)
            cmd = get_cmd()

            logger = get_logger()
            logger.debug(f'Running command: {cmd}')

            # Run command with retry
            if self.debug:
                stdout = sys.stdout
            else:
                out_path = task.get_log_path(file_extension='out')
                mmengine.mkdir_or_exist(osp.split(out_path)[0])
                stdout = open(out_path, 'w', encoding='utf-8')

            if random_sleep:
                time.sleep(random.randint(0, 10))

            def _run_within_retry():
                output = subprocess.getoutput(cmd)
                match = re.search(r'\|\s+(dlc[0-9a-z]+)\s+\|', output)
                if match is None:
                    raise RuntimeError(
                        f'Failed to launch dlc job for {output}')
                else:
                    job_id = match.group(1)
                stdout.write(output)

                pod_create_time = None
                pri_time = None
                initial_time = datetime.datetime.now()
                while True:
                    # 1. Avoid to request dlc too frequently.
                    # 2. DLC job may not be ready immediately after creation.
                    for _ in range(5):
                        time.sleep(2)
                        try:
                            job_info = json.loads(
                                subprocess.getoutput(f'dlc get job {job_id}'))
                            break
                        except:  # noqa: E722
                            pass
                    else:
                        raise RuntimeError(
                            f'Failed to get job info for {job_id}')

                    status = job_info['Status']
                    if status == 'Failed':
                        return -1
                    elif status == 'Succeeded':
                        return 0
                    elif status != 'Running':
                        continue

                    # The pod time could be different from the real time.
                    # Therefore we need to extract the pod start time from
                    # the `job_info` and calculate the `start_time` and
                    # `end_time` in pod.
                    if pod_create_time is None:
                        pod_create_time = job_info['GmtCreateTime']
                        pri_time = pod_create_time
                        pod_create_time = datetime.datetime.strptime(
                            pod_create_time, '%Y-%m-%dT%H:%M:%SZ')
                    elasped_time = datetime.datetime.now() - initial_time
                    cur_time = (pod_create_time +
                                elasped_time).strftime('%Y-%m-%dT%H:%M:%SZ')
                    logs_cmd = ('dlc logs'
                                f' {job_id} {job_id}-worker-0'
                                f" -c {self.aliyun_cfg['dlc_config_path']}"
                                f' --start_time {pri_time}'
                                f' --end_time {cur_time}')
                    log_output = subprocess.getoutput(logs_cmd)

                    if '[WARN] No logs found for the pod' not in log_output:
                        pri_time = cur_time
                        stdout.write(log_output)
                        stdout.flush()

            return_code = _run_within_retry()
            retry = self.retry
            output_paths = task.get_output_paths()
            while self._job_failed(return_code, output_paths) and retry > 0:
                retry -= 1
                cmd = get_cmd()
                return_code = _run_within_retry()
        finally:
            # Clean up
            os.remove(param_file)

        return task_name, return_code

    def _job_failed(self, return_code: int, output_paths: List[str]) -> bool:
        return return_code != 0 or not all(
            osp.exists(output_path) for output_path in output_paths)
