from mmengine.config import read_base
from opencompass.partitioners import NaivePartitioner,SizePartitioner
from opencompass.runners.local_api import LocalAPIRunner
from opencompass.tasks import OpenICLInferTask
from opencompass.models import Internlm2
from opencompass.summarizers import AssistantInternLM2Summarizer



with read_base():
    from configs.datasets.subjective_cmp.subjective_st import assistant50_v202301_r1



datasets = [*assistant50_v202301_r1]

models = [
    dict(
        abbr='sensellm-20b-0205-tools_4ksftpt_4kdata_spe_pack',
        type=Internlm2,
        path='sensellm-20b-0205-tools_4ksftpt_4kdata_spe_pack',
        url='http://101.230.144.204:12410/generate',
        max_seq_len=4096,
        batch_size=1,
    )
]


infer = dict(
    partitioner=dict(type=NaivePartitioner),
    runner=dict(
        type=LocalAPIRunner,
        max_num_workers=10,
        concurrent_users=10,
        task=dict(type=OpenICLInferTask)),
)


summarizer = dict(
    type=AssistantInternLM2Summarizer,
)
