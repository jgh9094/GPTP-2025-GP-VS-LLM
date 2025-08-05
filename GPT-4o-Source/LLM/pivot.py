# need to run this to get csv results for our paper

import os
import pandas as pd
import concurrent.futures
from multiprocessing import Process, Queue
import numpy as np
import csv
import json
from api_handler import AzureAPIHandler
import llmutils
from itertools import groupby
from operator import itemgetter
import logging
import json
import argparse
import copydetect as cdc
import sys
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

second_path = ['200', '100', '50']#llmutils.list_folders(problem_folder+"/basement")
prompt_types = ["Prompt", "IO", "PromptIO", "GP"]

out = pd.DataFrame(columns=["prompt_type", "training_case_size", "psb2_task", "k", "similarity"])
#df_index.to_csv(f"results/{train_count}/{prompt_type}/{train_count}_{prompt_type}_analysis_new.csv")
for prompt_type in prompt_types:
    for train_count in second_path:
        try:
            df = pd.read_csv(f"results/{train_count}/{prompt_type}/{train_count}_{prompt_type}_analysis_new.csv", index_col=0)
        except:
            continue
        df.index.name='psb2_task'
        df.reset_index(inplace=True)
        df.drop(['Success_Rate', 'Avg_Lines', 'Unique_Solns'], axis=1, inplace=True)
        #print(df.head())

        melted_df = df.melt(id_vars=['psb2_task'], var_name='k', value_name='similarity')
        print(melted_df.head())
        melted_df['training_case_size'] = int(train_count)
        melted_df['prompt_type'] = prompt_type
        out = pd.concat([out,melted_df], ignore_index=True)
out = out.sort_values(by=['prompt_type', 'training_case_size', 'psb2_task', 'k'])
out.to_csv(f"results/jose_table.csv")