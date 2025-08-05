# will save results files in ../results/*_analysis_new.csv

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

parser = argparse.ArgumentParser(description="Connect to your API using an LLM.")
parser.add_argument('--test', type=bool, default='False')
parser.add_argument('--problemfolder', type=str)
parser.add_argument('--codefolder', type=str)


# Parse arguments
args = parser.parse_args()
test = args.test
problem_folder = args.problemfolder
code_folder = args.codefolder

first_path = ['basement', 'bouncing-balls', 'bowling', 'camel-case',
                 'coin-sums', 'cut-vector', 'dice-game', 'find-pair',
                 'fizz-buzz', 'fuel-cost', 'gcd',  'indices-of-substring',
                 'leaders'] #llmutils.list_folders(problem_folder)  # Current directory
second_path = ['200', '50']#llmutils.list_folders(problem_folder+"/basement")
# todo: only kept GP bc we only need this data left
prompt_types = ["GP"]
# prompt_types = ["GP", "IO", "Prompt", "PromptIO"]
iterations = 100
'''
# Example usage:
if not test:
    first_path = llmutils.list_folders(problem_folder)  # Current directory
    second_path = ['200','100','50']#llmutils.list_folders(problem_folder+"/basement")
    prompt_types = ["Prompt", "IO", "PromptIO"]
    iterations = 100
else:
    first_path = ['shopping-list'] # Current directory
    second_path = ['200', '50']
    prompt_types = ["Prompt", "IO", "PromptIO"]
    iterations = 100
'''
def main(problem_names, train_length, prompt_types, iterations):
    """Direct arguments from a script and give to the loop function."""
    print(problem_names)
    print(train_length)
    print(prompt_types)
    analysis_loop(problem_names, train_length, prompt_types, iterations)
    print('Analysis Finished')

def analysis_loop(problem_names, train_length, prompt_types, iterations):
    """Retrive responses, convert to functions, and determine success rates."""
    for train_count in train_length:
        for prompt_type in prompt_types:
            save_dict = {}
            if prompt_type == "GP":
                for problem_name in problem_names:
                    list_of_responses = []
                    list_of_successful = []
                    lines_of_code_avg = []
                    unique_counts = {}
                    with open(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/my_dict.json", 'r') as file:
                        hold = json.load(file)
                        list_of_responses = list(hold.values())
                    with open(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/my_success.json", 'r') as nextfile:
                        list_of_success_or_fail = json.load(nextfile)
                        list_success = list(list_of_success_or_fail.values())
                        success_rate = sum(list_success)
                    for i in range(iterations):
                        #function_response=functions[i]
                        #list_of_responses.append(function_text)
                        if list_success[i] == 1:
                            list_of_successful.append(list_of_responses[i])
                            lines_of_code_avg.append(list_of_responses[i].count('\n'))
                            if list_of_responses[i] in unique_counts:
                                unique_counts[list_of_responses[i]] += 1
                            else:
                                unique_counts[list_of_responses[i]] = 1
                        print(f"{i} Complete")
                    x = calc_similarity(list_of_successful, problem_name, train_count, prompt_type, kgrams=2, filtering=False)
                    y = calc_similarity(list_of_successful, problem_name, train_count, prompt_type, kgrams=5, filtering=False)
                    z = calc_similarity(list_of_successful, problem_name, train_count, prompt_type, kgrams=10, filtering=False)
                    lines_of_code = np.mean(lines_of_code_avg)
                    unique_soln = len(unique_counts)
                    avg_similarity = np.mean(x)
                    print("Success Rate:")
                    print(success_rate)
                    print("Avg Lines:")
                    print(lines_of_code)
                    print("Unique Solns")
                    print(unique_soln)
                    print("Similarity")
                    print(x)
                    print(f"{problem_name} Complete")
                    save_dict[problem_name] = [success_rate, lines_of_code, unique_soln, x, y, z]

            else:
                for problem_name in problem_names:
                    #print(problem_name, prompt_type, train_count)
                    list_of_responses = load_responses(problem_name, train_count, prompt_type, iterations)
                    list_of_successful= []
                    success_rate = 0
                    lines_of_code_avg = []
                    unique_counts = {}
                    list_of_similarities = []
                    for i in range(iterations):
                        print(problem_name, train_count, prompt_type)
                        success = calc_success_rate(list_of_responses[i], problem_name, train_count, i)
                        print(success)
                        success_rate += success
                        if success == 1:
                            list_of_successful.append(list_of_responses[i])
                            lines_of_code_avg.append(list_of_responses[i].count('\n'))
                            if list_of_responses[i] in unique_counts:
                                unique_counts[list_of_responses[i]] += 1
                            else:
                                unique_counts[list_of_responses[i]] = 1
                            #x = calc_similarity(problem_name, train_count, prompt_type, i)
                            #list_of_similarities.append(x)
                            #print('#' * 100)
                            #print(x)
                            #print('#' * 100)
                        print(f"{i} Complete")
                    x = calc_similarity(list_of_successful, problem_name, train_count, prompt_type, kgrams=2, filtering=True)
                    y = calc_similarity(list_of_successful, problem_name, train_count, prompt_type, kgrams=5, filtering=True)
                    z = calc_similarity(list_of_successful, problem_name, train_count, prompt_type, kgrams=10, filtering=True)

                    lines_of_code = np.mean(lines_of_code_avg)
                    unique_soln = len(unique_counts)
                    avg_similarity = np.mean(x)
                    print("Success Rate:")
                    print(success_rate)
                    print("Avg Lines:")
                    print(lines_of_code)
                    print("Unique Solns")
                    print(unique_soln)
                    print("Similarity")
                    print(x)
                    print(f"{problem_name} Complete")
                    save_dict[problem_name] = [success_rate, lines_of_code, unique_soln, x, y, z]
            df_index = pd.DataFrame.from_dict(save_dict, orient='index', columns=["Success_Rate", "Avg_Lines", "Unique_Solns", "2", "5", "10"])
            print("\nDataFrame result:\n", df_index)
            if not os.path.exists(f"results/{train_count}/{prompt_type}"):
                os.makedirs(f"results/{train_count}/{prompt_type}")
            df_index.to_csv(f"results/{train_count}/{prompt_type}/{train_count}_{prompt_type}_analysis_new.csv")
            print(f"{prompt_type} Complete")
        print(f"{train_count} Complete")

def load_training_test_data(dataset_name, portion, iteration):
    train = pd.read_csv(f"{problem_folder}/{dataset_name}/{str(portion)}/{dataset_name}_{iteration}_train.csv")
    input_cols = [col for col in train.columns if col.startswith("input")]
    X_train = train[input_cols]
    y_train = train.drop(columns=input_cols)
    test = pd.read_csv(f"{problem_folder}/{dataset_name}/{str(portion)}/{dataset_name}_{iteration}_test.csv")
    X_test = test[input_cols]
    y_test = test.drop(columns=input_cols)
    f = open(f"{problem_folder}/{dataset_name}/function.txt")
    new_line = f.readline()
    f.close()
    new_line = new_line.split(",")
    final_output = []
    for i in new_line:
        if 'input' in i:
            out = i.split(':')[1]
        else:
            out = i
        final_output.append(out)

    return X_train, y_train, X_test, y_test, final_output

def load_responses(problem_name, train_count, prompt_type, iterations):
    list_of_responses = []
    for i in range(iterations):
        data=[]
        with open(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/response_{i}.json", 'r') as f:
            for line in f:
                data.append(json.loads(line))
            function_response=(data[-1]['response'])
            confirmed, function_text = llmutils.verify_response(function_response)
            with open(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/response_{i}_final.py", "w") as file:
                file.write(function_text)
                file.close()
            list_of_responses.append(function_text)
    return list_of_responses

def calc_success_rate(function_response, problem_name, train_count, i):
    output = 0
    X_train, y_train, X_test, y_test, input_types = load_training_test_data(
                                                problem_name, train_count, i)
    print(input_types)
    print("Running:")
    print(function_response)
    print('Training Cases')
    train_success_rate = FxnExeRunspace(function_response, X_train, y_train, input_types, timeout=60)
    print("Complete")
    print('Test Cases')
    test_success_rate = FxnExeRunspace(function_response, X_test, y_test, input_types, timeout=60)
    print("Complete")
    if not (1.0-train_success_rate)>0:
        if not (1.0-test_success_rate)>0:
            output = 1
    return output


def FxnExeRunspace(function_response, X, y, input_types, timeout=60):
    queue = Queue()
    process = Process(target=execute_my_func, args=(queue, function_response, X, y, input_types))
    process.start()
    process.join(timeout)
    if process.is_alive():
        print("Process taking too long to execute. Terminating forcefully.")
        process.terminate()
        process.join()
        return 0.0
    results = queue.get() if not queue.empty() else 0.0
    return results

def execute_my_func(queue, function_response, X, y, input_types):
    """Executes my_func with a timeout."""

    inputs = [word for letter, words in groupby(sorted(list(X.columns.values)), key=itemgetter(0)) if letter == 'i' for word in words]
    outputs = [word for letter, words in groupby(sorted(list(y.columns.values)), key=itemgetter(0)) if letter != 'i' for word in words]

    y = y.astype("string")
    pred = y.copy()
    for col in pred.columns:
        pred[col].values[:] = '0'

    for col in X.columns:
        if input_types[0] == "list of floats":
            X[col] = X[col].apply(lambda s: [float(x.strip(' []')) for x in s.split(' ')])
        elif input_types[0] == "list of integers":
            X[col] = X[col].apply(lambda s: [int(x.strip(' []')) for x in s.split(' ')])
        else:
            X[col] = X[col].astype(input_types[0])
        input_types.pop(0)

        #pred[col].values[:] = '0'

    namespace = {}
    exec(function_response, namespace)

    for key in namespace.keys():
        globals().pop(key, None)
        globals()[key] = namespace.get(key)
    my_func = namespace.get('my_func')

    if not my_func:
        queue.put(0.0)
        return

    try:
        # Using apply in a lambda that applies my_func to each row
        pred[outputs] = X.apply(
            lambda row: pd.Series(my_func(*[row[i] for i in inputs]), index=outputs),
            axis=1,
            result_type='expand'
        ).astype('string')
        # Compare results and return based on equality
        #print(y.compare(pred))
        percentages = y.eq(pred).mean(axis=0).min()
        #print(percentages)
        if not np.isnan(percentages):
            queue.put(percentages)
            for key in namespace.keys():
                globals().pop(key, None)
            return
        else:
            queue.put(0.0)
            for key in namespace.keys():
                globals().pop(key, None)
            return
    except Exception as e:
        a, b, exc_trace = sys.exc_info()
        line_number = traceback.extract_tb(exc_trace)[-1][1]
        print(f"Error while executing 'my_func': {e}")
        print(f"Error found on line: {line_number}")
        queue.put(0.0)
        for key in namespace.keys():
                globals().pop(key, None)
        return

def count_string_occurrences(string_list):
    """
    Counts the occurrences of each unique string in a list.

    Args:
        string_list: A list of strings.

    Returns:
        A dictionary where keys are unique strings from the list,
        and values are their corresponding counts.
    """
    string_counts = {}
    for string in string_list:
        if string in string_counts:
            string_counts[string] += 1
        else:
            string_counts[string] = 1
    return string_counts

def calc_similarity(list_of_successes, problem_name, train_count, prompt_type, kgrams, filtering):
    similarity_list = []
    for i, items in enumerate(list_of_successes):
        with open(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/success_{i}_final.py", "w") as file:
                file.write(items)
                file.close()
    for i in range(len(list_of_successes)):
        fp1 = cdc.CodeFingerprint(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/success_{i}_final.py", k=kgrams, win_size=kgrams, filter=filtering)
        for othervals in [num for num in range(0, len(list_of_successes)) if num != i]:

            fp2 = cdc.CodeFingerprint(code_folder+f"/{problem_name}/{train_count}/{prompt_type}/success_{othervals}_final.py",k=kgrams, win_size=kgrams, filter=filtering)
            token_overlap, similarities, slices = cdc.compare_files(fp1, fp2)
            similarity_list.append(similarities[0])
    # https://github.com/blingenf/copydetect
    # https://copydetect.readthedocs.io/en/latest/api.html
    # https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf
    out = np.mean(similarity_list)
    return out
    '''
    num = 10
    detector = cdc.CopyDetector(test_dirs=[code_folder+f"/{problem_name}/{train_count}/{prompt_type}/response_{iteration}_final.py"],
                                ref_dirs=ref_dir,
                                extensions=["py"],
                                # boilerplate_dirs=['./Results_Python/Boilerplate'],
                                display_t=0.01,
                                noise_t=num,
                                guarantee_t=num,
                                )
    '''

    # detector = cdc.CopyDetector(test_dirs=["./Results_PushGP/Code_1"],
    #                             ref_dirs=['./Results_PushGP/Code_2'],
    #                             extensions=["txt"],
    #                             display_t=0.00,
    #                             noise_t=num,
    #                             guarantee_t=num,
    #                             disable_filtering=True
    #                             )

    #detector.run()

    #print('#' * 100)
   # for x in detector.get_copied_code_list():
        #out = x
        #print(x)
        #print('#' * 100)

    #return out


    #detector.generate_html_report()

if __name__ == "__main__":
    main(first_path, second_path, prompt_types, iterations)
