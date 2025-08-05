import pandas as pd
import argparse
import success_dicts as sd
import copydetect as cdc
import numpy as np
import os
import ray


def generate_successes_csv(result_dir):
    # iterate through all all success dictionaries and save them to a CSV file
    push_list = []
    task_list = []
    data_list = []
    text_list = []
    dt_list = []
    size_list = []

    # collect data for 200 cases dictionaries
    for task in sd.psb2_tasks:
        task_list.append(task)
        push_list.append(sd.push_gp_success_200[task])
        data_list.append(sd.gpt4o_d_success_200[task])
        text_list.append(sd.gpt4o_t_success_200[task])
        dt_list.append(sd.gpt4o_dt_success_200[task])
        size_list.append(200)

    # collect data for 50 cases dictionaries
    for task in sd.psb2_tasks:
        task_list.append(task)
        push_list.append(sd.push_gp_success_50[task])
        data_list.append(sd.gpt4o_d_success_50[task])
        text_list.append(sd.gpt4o_t_success_50[task])
        dt_list.append(sd.gpt4o_dt_success_50[task])
        size_list.append(50)

    # save to CSV
    df = pd.DataFrame({
        'task': task_list,
        'push_gp': push_list,
        'data': data_list,
        'data-text': dt_list,
        'text': text_list,
        'size': size_list
    })
    df.to_csv(f'{result_dir}/psb2_successes.csv', index=False)

def generate_latex_table():
    print('Table for 200 cases:')
    for task in sd.psb2_tasks:
        print(f"{sd.table_name_key[task]} & {sd.push_gp_success_200[task]} & {sd.gpt4o_d_success_200[task]} & "
              f"{sd.gpt4o_dt_success_200[task]} & {sd.gpt4o_t_success_200[task]} \\\\")

    print('\nTable for 50 cases:')
    for task in sd.psb2_tasks:
        print(f"{sd.table_name_key[task]} & {sd.push_gp_success_50[task]} & {sd.gpt4o_d_success_50[task]} & "
              f"{sd.gpt4o_dt_success_50[task]} & {sd.gpt4o_t_success_50[task]} \\\\")

@ray.remote
def ray_calc_similarity(list_of_successes, kgrams, filtering, task, case, prompt_type):
    overall_similarity = []
    for i,anchor in enumerate(list_of_successes):
        anchor_fp = cdc.CodeFingerprint(anchor, k=kgrams, win_size=kgrams, filter=filtering)
        similarity_list = []
        for j, slider in enumerate(list_of_successes):
            if i == j:
                continue
            slider_fp = cdc.CodeFingerprint(slider,k=kgrams, win_size=kgrams, filter=filtering)
            _, similarities, _ = cdc.compare_files(anchor_fp, slider_fp)
            similarity_list.append(similarities[0])

        assert len(similarity_list) == len(list_of_successes) - 1, "Similarity list length mismatch."
        overall_similarity.append(np.mean(similarity_list))

    assert len(overall_similarity) == len(list_of_successes), "Overall similarity length mismatch."
    return np.mean(overall_similarity), task, case, prompt_type, kgrams

def generate_similarity(data_dir, results_dir):
    ray_jobs = []
    results_dict = {}
    for task in sd.psb2_tasks:
        for cases in [50, 200]:
            for prompt_type in ['GP', 'IO', 'Prompt', 'PromptIO']:
                if prompt_type == 'GP' and cases == 200 and sd.push_gp_success_200[task] < 2:
                    continue
                elif prompt_type == 'IO' and cases == 200 and sd.gpt4o_d_success_200[task] < 2:
                    continue
                elif prompt_type == 'Prompt' and cases == 200 and sd.gpt4o_t_success_200[task] < 2:
                    continue
                elif prompt_type == 'PromptIO' and cases == 200 and sd.gpt4o_dt_success_200[task] < 2:
                    continue
                elif prompt_type == 'GP' and cases == 50 and sd.push_gp_success_50[task] < 2:
                    continue
                elif prompt_type == 'IO' and cases == 50 and sd.gpt4o_d_success_50[task] < 2:
                    continue
                elif prompt_type == 'Prompt' and cases == 50 and sd.gpt4o_t_success_50[task] < 2:
                    continue
                elif prompt_type == 'PromptIO' and cases == 50 and sd.gpt4o_dt_success_50[task] < 2:
                    continue

                # add entry for the results dictionary
                results_dict[(task, cases, prompt_type)] = {2: None, 5: None, 10: None}

                cur_dir = f"{data_dir}/{task}/{cases}/{prompt_type}"
                files = os.listdir(cur_dir)
                success_dir_list = [f'{cur_dir}/{file}' for file in files]

                filter_bool = False if prompt_type == 'GP' else True
                ray_jobs.append(ray_calc_similarity.remote(success_dir_list, kgrams=2, filtering=filter_bool, task=task, case=cases, prompt_type=prompt_type))
                ray_jobs.append(ray_calc_similarity.remote(success_dir_list, kgrams=5, filtering=filter_bool, task=task, case=cases, prompt_type=prompt_type))
                ray_jobs.append(ray_calc_similarity.remote(success_dir_list, kgrams=10, filtering=filter_bool, task=task, case=cases, prompt_type=prompt_type))

    results_list = []
    while len(ray_jobs) > 0:
        finished, ray_jobs = ray.wait(ray_jobs)
        sim, task, case, prompt_type, kgrams = ray.get(finished)[0]
        results_list.append((sim, task, case, prompt_type, kgrams))
        print(f"Task: {task}, Case: {case}, Prompt Type: {prompt_type}, Kgrams: {kgrams}")

    assert len(results_list) == len(results_dict) * 3, "Results list length mismatch."
    for sim, task, case, prompt_type, kgrams in results_list:
        if kgrams == 2:
            results_dict[(task, case, prompt_type)][2] = sim
        elif kgrams == 5:
            results_dict[(task, case, prompt_type)][5] = sim
        elif kgrams == 10:
            results_dict[(task, case, prompt_type)][10] = sim

    # make sure none of the results are None
    for key, value in results_dict.items():
        assert value[2] is not None, f"2-gram similarity for {key} is None."
        assert value[5] is not None, f"5-gram similarity for {key} is None."
        assert value[10] is not None, f"10-gram similarity for {key} is None."

    # generate lists for the CSV file
    synthesizer_list = []
    task_list = []
    case_list = []
    k_2_list = []
    k_5_list = []
    k_10_list = []
    for (task, case, prompt_type), similarities in results_dict.items():
        task_list.append(task)
        synthesizer_list.append(prompt_type)
        case_list.append(case)
        k_2_list.append(similarities[2])
        k_5_list.append(similarities[5])
        k_10_list.append(similarities[10])

    print('synthesizer_list:', len(synthesizer_list))
    print('task_list:', len(task_list))
    print('case_list:', len(case_list))
    print('k_2_list:', len(k_2_list))
    print('k_5_list:', len(k_5_list))
    print('k_10_list:', len(k_10_list))

    # update synthesizer_list with the following switch:
    # 'GP' -> 'PushGP'
    # 'IO' -> 'GPT-4o (D)'
    # 'Prompt' -> 'GPT-4o (T)'
    # 'PromptIO' -> 'GPT-4o (D-T)'
    synthesizer_list = [
        'PushGP' if s == 'GP' else
        'GPT-4o (D)' if s == 'IO' else
        'GPT-4o (T)' if s == 'Prompt' else
        'GPT-4o (D-T)' if s == 'PromptIO' else
        s
        for s in synthesizer_list
    ]

    assert len(task_list) == len(synthesizer_list) == len(k_2_list) == len(k_5_list) == len(k_10_list), "Length mismatch in similarity lists."
    df = pd.DataFrame({
        'task': task_list,
        'synthesizer': synthesizer_list,
        'case': case_list,
        'k_2': k_2_list,
        'k_5': k_5_list,
        'k_10': k_10_list
    })
    df.to_csv(f'{results_dir}/psb2_similarity.csv', index=False)
    return


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Generate successes for PSB2 tasks.')
    args.add_argument('--results_dir', type=str, help='Directory to save the results.')
    args.add_argument('--data_dir', type=str, help='Directory to load the data.')
    args = args.parse_args()

    # initialize ray
    ray.init(num_cpus=12, include_dashboard=True)

    results_dir = args.results_dir
    data_dir = args.data_dir

    # go through all success dictionaries and count how many success are greater than 1
    count = 0
    for k,v in sd.push_gp_success_200.items():
        if v > 1:
            count += 1
    for k,v in sd.gpt4o_d_success_200.items():
        if v > 1:
            count += 1
    for k,v in sd.gpt4o_t_success_200.items():
        if v > 1:
            count += 1
    for k,v in sd.gpt4o_dt_success_200.items():
        if v > 1:
            count += 1
    for k,v in sd.push_gp_success_50.items():
        if v > 1:
            count += 1
    for k,v in sd.gpt4o_d_success_50.items():
        if v > 1:
            count += 1
    for k,v in sd.gpt4o_t_success_50.items():
        if v > 1:
            count += 1
    for k,v in sd.gpt4o_dt_success_50.items():
        if v > 1:
            count += 1
    print(f'Expected number of successes: {count}')

    # generate the CSV file for data analysis
    generate_successes_csv(results_dir)

    # generate the LaTeX table for documentation
    generate_latex_table()

    # generate similarity metrics for the success cases
    generate_similarity(data_dir, results_dir)

    # close ray
    ray.shutdown()