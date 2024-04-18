
import os
import re
import json
import glob

import mmengine
import pandas as pd
import seaborn as sns
import os.path as osp
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from datetime import datetime
from matplotlib.colors import LinearSegmentedColormap
from opencompass.utils import dataset_abbr_from_cfg, model_abbr_from_cfg
from matplotlib.ticker import FuncFormatter



class NeedleHaystackVisualizer:
    def __init__(self, config) -> None:
        self.tasks = []
        self.cfg = config

    def summarize(self,
                time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        self.visualize(time_str)


    def visualize(self, time_str: str = datetime.now().strftime('%Y%m%d_%H%M%S')):
        dataset_cfgs = self.cfg['datasets']
        work_dir = self.cfg['work_dir']
        self.work_dir = work_dir

        self.time_str = time_str
        output_path = osp.join(self.work_dir, 'summary',
                               f'summary_{self.time_str}.png')
        output_dir = osp.join(osp.split(output_path)[0], f'{self.time_str}')
        mmengine.mkdir_or_exist(output_dir)
        
        prediction_folder = osp.join(work_dir, 'predictions')

        acc_tabel = {'context-length': [],  'doc-depth': [], 'Score': []}

        models = os.listdir(prediction_folder)

        assert(len(models) == 1), "only support one model!"

        for subdir in os.listdir(prediction_folder):
            subdir_pred_path = os.path.join(prediction_folder, subdir)
            model_abbr = subdir

            if os.path.isdir(subdir_pred_path):
                for dataset in dataset_cfgs:
                    dataset_abbr = dataset_abbr_from_cfg(dataset)
                    pred_filepath = os.path.join(subdir_pred_path, dataset_abbr + '.json')
                    preds = mmengine.load(pred_filepath)

                    for k, v in preds.items():
                        prediction = v['prediction']
                        gold = v['gold']
                        context_length = int(gold.split('-')[0])
                        doc_depth = int(gold.split('-')[1])
                        answer = int(gold.split('-')[0])

                        if "前海深港合作区前湾一路1号A栋201室" in prediction:
                            score = 100.0
                        else:
                            score = 0

                        acc_tabel['context-length'].append(context_length)
                        acc_tabel['doc-depth'].append(doc_depth)
                        acc_tabel['Score'].append(score)


        df = pd.DataFrame(acc_tabel)
        # print (df.head())

        pivot_table = pd.pivot_table(df, values='Score', index=['doc-depth', 'context-length'], aggfunc='mean').reset_index() # This will aggregate
        pivot_table = pivot_table.pivot(index="doc-depth", columns="context-length", values="Score") # This will tur


        cmap = LinearSegmentedColormap.from_list("custom_cmap", ["#F0496E", "#EBB839", "#0CD79F"])

        plt.figure(figsize=(17.5, 8))  # Can adjust these dimensions as needed
        sns.heatmap(
            pivot_table,
            annot=True,
            fmt="g",
            cmap=cmap,
            cbar_kws={'label': 'Score'}
        )


        # Set line plot data
        mean_scores = pivot_table.mean().values
        overall_score = mean_scores.mean()
        x_data = [i + 0.5 for i in range(len(mean_scores))]
        y_data = mean_scores

        ax = plt.gca()


        # # Create twin axis for line plot
        # ax2 = ax.twinx()
        # # Draw line plot
        # ax2.plot(x_data,
        #             y_data,
        #             color='white',
        #             marker='o',
        #             linestyle='-',
        #             linewidth=2,
        #             markersize=8,
        #             label='Average Depth Score')
        # # Set y-axis range
        # ax2.set_ylim(0, 100)

        # for i, j in zip(x_data, y_data):
        #     ax2.text(i,j, str(j), ha='center', va='bottom')


        # # Hide original y-axis ticks and labels
        # ax2.set_yticklabels([])
        # ax2.set_yticks([])

        # # Add legend
        # ax2.legend(loc='upper left')

        # More aesthetics
        plt.title(f'Pressure Testing "{model_abbr}" Context\nFact Retrieval Across Context Lengths ("Needle In A HayStack")')  # Adds a title
        plt.xlabel('Context Length')  # X-axis label
        plt.ylabel('Depth Percent')  # Y-axis label
        plt.xticks(rotation=45)  # Rotates the x-axis labels to prevent overlap
        plt.yticks(rotation=0)  # Ensures the y-axis labels are horizontal
        # ax.yaxis.set_major_formatter(mtick.PercentFormatter(20))
        plt.tight_layout()  # Fits everything neatly into the figure area


        plt.savefig(f"{output_dir}/needlehaystack_{model_abbr}.png", dpi=500)
        # Show the plot
        plt.show()
        plt.close()




