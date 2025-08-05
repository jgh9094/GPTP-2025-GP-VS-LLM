# check to make sure all successes are generated for PSB2 tasks
# this script checks the number of files in the success directories for each task

import os
import argparse
import success_dicts as sd

def gp_checker(task, size, data_dir):
    res_dir = f'{data_dir}/GP'
    # count number of files in the directory
    if not os.path.exists(res_dir):
        return False
    files = os.listdir(res_dir)

    if size == 200:
        return len(files) == sd.push_gp_success_200[task]
    elif size == 50:
        return len(files) == sd.push_gp_success_50[task]
    else:
        raise ValueError("Size must be either 200 or 50.")

def io_checker(task, size, data_dir):
    res_dir = f'{data_dir}/IO'
    # count number of files in the directory
    if not os.path.exists(res_dir):
        return False
    files = os.listdir(res_dir)

    if size == 200:
        return len(files) == sd.gpt4o_d_success_200[task]
    elif size == 50:
        return len(files) == sd.gpt4o_d_success_50[task]
    else:
        raise ValueError("Size must be either 200 or 50.")

def prompt_checker(task, size, data_dir):
    res_dir = f'{data_dir}/Prompt'
    # count number of files in the directory
    if not os.path.exists(res_dir):
        return False
    files = os.listdir(res_dir)

    if size == 200:
        return len(files) == sd.gpt4o_t_success_200[task]
    elif size == 50:
        return len(files) == sd.gpt4o_t_success_50[task]
    else:
        raise ValueError("Size must be either 200 or 50.")

def prompt_io_checker(task, size, data_dir):
    res_dir = f'{data_dir}/PromptIO'
    # count number of files in the directory
    if not os.path.exists(res_dir):
        return False
    files = os.listdir(res_dir)

    if size == 200:
        return len(files) == sd.gpt4o_dt_success_200[task]
    elif size == 50:
        return len(files) == sd.gpt4o_dt_success_50[task]
    else:
        raise ValueError("Size must be either 200 or 50.")

def check_successes(data_dir):
    # iterate through all tasks
    for task in sd.psb2_tasks:
        # iterate through both sizes of cases
        for size in [200, 50]:
            print(f'Checking task: {task}, size: {size}')
            # iterate through 4 program synthesis methods and make sure all checks pass
            assert gp_checker(task, size, f'{data_dir}/{task}/{size}')
            assert io_checker(task, size, f'{data_dir}/{task}/{size}')
            assert prompt_checker(task, size, f'{data_dir}/{task}/{size}')
            assert prompt_io_checker(task, size, f'{data_dir}/{task}/{size}')

if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Generate successes for PSB2 tasks.')
    args.add_argument('--data_dir', type=str, help='Directory to save the results.')
    args = args.parse_args()
    check_successes(args.data_dir)