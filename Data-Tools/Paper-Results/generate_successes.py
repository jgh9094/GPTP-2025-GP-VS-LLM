# generates the text files for the successes of the PSB2 tasks for the push-gp synthesizer
# the text files are saved in the results directory

import json
import argparse
import success_dicts as sd

def generate_successes_push_gp(data_dir, result_dir, cases):
    # iterate through all tasks
    for task in sd.psb2_tasks:
        print(f'Processing task: {task}, cases: {cases}')

        success_cnt = 0
        print(f'exploring dir: {data_dir}/{task}')

        # read my_dict.json file
        my_dict = json.load(open(f'{data_dir}/{task}/my_dict.json', 'r'))
        # read successes.json file
        successes = json.load(open(f'{data_dir}/{task}/my_success.json', 'r'))

        # iterate through all keys in successes and find keys where the value is 1
        for key, value in successes.items():
            if value == 1:
                # save my_dict[key] into a file in the results directory
                with open(f'{result_dir}/{task}/{cases}/GP/success_{key}.txt', 'w') as f:
                    f.write(my_dict[key])
                success_cnt += 1

        if cases == 200:
            assert success_cnt == sd.push_gp_success_200[task]
        elif cases == 50:
            assert success_cnt == sd.push_gp_success_50[task]
        else:
            print(f"Unsupported case count: {cases}. Please use 50 or 200.")
            exit(1)

if __name__ == "__main__":
    # read json file
    args = argparse.ArgumentParser(description='Generate successes for PSB2 tasks.')
    args.add_argument('--data_dir', type=str, help='Directory containing the data files.')
    args.add_argument('--results_dir', type=str, help='Directory to save the results.')
    args.add_argument('--synthesizer', type=str, help='1: push-gp, 2: gpt(D), 3: gpt(T), 4: gpt(D-T)',)
    args.add_argument('--cases', type=int, help='Number of cases condition.')
    args = args.parse_args()

    data_dir = args.data_dir
    synthesizer = args.synthesizer
    results_dir = args.results_dir
    cases = args.cases

    if synthesizer == 'push_gp':
        generate_successes_push_gp(data_dir, results_dir, cases)
    else:
        print(f"Unsupported synthesizer: {synthesizer}. Please use 'push_gp'.")
        exit(1)