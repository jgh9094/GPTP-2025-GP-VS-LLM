# check to make sure all successes are generated for PSB2 tasks
# this script checks the number of files in the success directories for each task

import os
import argparse
import success_dicts as sd

# find all tasks that overlap between push_gp_success_200 and gpt4o_dt_success_200
# task success must be greater than 0 in both dictionaries
def overlap_200_pushgp_gpt4o_dt():
    count = 0
    gpt = 0
    push = 0
    print('GPT-4o-DT and PushGP 200 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 and sd.gpt4o_dt_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.gpt4o_dt_success_200[task] - sd.push_gp_success_200[task]}")
            if sd.push_gp_success_200[task] > sd.gpt4o_dt_success_200[task]:
                push += 1
            else:
                gpt += 1
    print()
    print(f"PushGP has greater success in {push} tasks.")
    print(f"GPT-4o-DT has greater success in {gpt} tasks.")
    print(f"Total tasks with success in both: {count}")

# find all tasks between push_gp_success_200 and gpt4o_dt_success_200
# where gpt4o_dt_success_200 has success greater than 0 and push_gp_success_200 has 0 success
def pushgp_zero_gpt4o_dt_200():
    count = 0
    print('GPT-4o-DT and PushGP 200 Cases Overlap Successes (GPT-4o-DT > 0, PushGP = 0)')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] == 0 and sd.gpt4o_dt_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.gpt4o_dt_success_200[task]}")
    print()
    print(f"Total tasks with success in GPT-4o-DT: {count}")

# find all tasks between push_gp_success_200 and gpt4o_dt_success_200
# where gpt4o_dt_success_200 0 success and push_gp_success_200 has success greater than 0
def gpt4o_dt_zero_pushgp_200():
    count = 0
    print('GPT-4o-DT and PushGP 200 Cases Overlap Successes (GPT-4o-DT = 0, PushGP > 0)')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 and sd.gpt4o_dt_success_200[task] == 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.push_gp_success_200[task]}")
    print()
    print(f"Total tasks with success in PushGP: {count}")

# find all tasks between push_gp_success_200 and gpt4o_dt_success_200 where both have success greater than 0
def union_gpt4o_dt_pushgp_200():
    count = 0
    print('GPT-4o-DT and PushGP 200 Cases Overlap Successes (Union)')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 or sd.gpt4o_dt_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.push_gp_success_200[task]} - {sd.gpt4o_dt_success_200[task]}")
    print()
    print(f"Total tasks with success in either: {count}")

# find all tasks that overlap between push_gp_success_200 and gpt4o_d_success_200
# task success must be greater than 0 in both dictionaries
def overlap_200_pushgp_gpt4o_d():
    count = 0
    gpt = 0
    push = 0
    print('GPT-4o-D and PushGP 200 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 and sd.gpt4o_d_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.gpt4o_d_success_200[task] - sd.push_gp_success_200[task]}")
            if sd.push_gp_success_200[task] > sd.gpt4o_d_success_200[task]:
                push += 1
            else:
                gpt += 1
    print()
    print(f"Total tasks with success in both: {count}")
    print(f"PushGP has greater success in {push} tasks.")
    print(f"GPT-4o-D has greater success in {gpt} tasks.")

# find all tasks between push_gp_success_200 and gpt4o_d_success_200
# where gpt4o_d_success_200 has success greater than 0 and push_gp_success_200 has 0 success
def pushgp_zero_gpt4o_d_200():
    count = 0
    print('GPT-4o-D and PushGP 200 Cases Overlap Successes (GPT-4o-D > 0, PushGP = 0)')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] == 0 and sd.gpt4o_d_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.gpt4o_d_success_200[task]}")
    print()
    print(f"Total tasks with success in GPT-4o-D: {count}")

# find all tasks between push_gp_success_200 and gpt4o_d_success_200
# where gpt4o_d_success_200 has 0 success and push_gp_success_200 has success greater than 0
def gpt4o_d_zero_pushgp_200():
    count = 0
    print('GPT-4o-D and PushGP 200 Cases Overlap Successes (GPT-4o-D = 0, PushGP > 0)')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 and sd.gpt4o_d_success_200[task] == 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.push_gp_success_200[task]}")
    print()
    print(f"Total tasks with success in PushGP: {count}")

# find all tasks between push_gp_success_200 or gpt4o_dt_success_200 where both have success greater than 0
def union_gpt4o_d_pushgp_200():
    count = 0
    print('GPT-4o-D and PushGP 200 Cases Overlap Successes (Union)')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 or sd.gpt4o_d_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.push_gp_success_200[task]} - {sd.gpt4o_d_success_200[task]}")
    print()
    print(f"Total tasks with success in either: {count}")

# find all tasks that overlap between gpt4o_d_success_200 and gpt4o_dt_success_200
# task success must be greater than 0 in both dictionaries
def overlap_gpt4o_d_gpt4o_dt_200():
    count = 0
    print('GPT-4o-D and GPT-4o-DT 200 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.gpt4o_d_success_200[task] > 0 and sd.gpt4o_dt_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.gpt4o_dt_success_200[task] - sd.gpt4o_d_success_200[task]}")
    print()
    print(f"Total tasks with success in both: {count}")

# find all tasks that overlap between gpt4o_t_success_200 and gpt4o_dt_success_200
# task success must be greater than 0 in both dictionaries
def overlap_gpt4o_t_gpt4o_dt_200():
    count = 0
    print('GPT-4o-T and GPT-4o-DT 200 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.gpt4o_t_success_200[task] > 0 and sd.gpt4o_dt_success_200[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}: {sd.gpt4o_dt_success_200[task] - sd.gpt4o_t_success_200[task]}")
    print()
    print(f"Total tasks with success in both: {count}")

# find all tasks between gpt4o_dt_success_200 and gpt4o_d_success_200 and gpt4o_t_success_200
# where gpt4o_dt_success_200 success is greater than 0 and the others have 0 success
def gpt4o_dt_zero_gpt4o_d_t_200():
    count = 0
    print('GPT-4o-DT and GPT-4o-D and GPT-4o-T 200 Cases Overlap Successes (GPT-4o-DT > 0, others = 0)')
    for task in sd.psb2_tasks:
        if sd.gpt4o_dt_success_200[task] > 0 and sd.gpt4o_d_success_200[task] == 0 and sd.gpt4o_t_success_200[task] == 0:
            count += 1
            print(f"{task}: {sd.gpt4o_dt_success_200[task]}")
    print()
    print(f"Total tasks with success in GPT-4o-DT: {count}")

# find all tasks that overlap between gpt4o_d_success_200 and gpt4o_d_success_50
# where both have success greater than 0
def overlap_gpt4o_d_200_50():
    count = 0
    print('GPT-4o-D 200 and 50 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.gpt4o_d_success_200[task] > 0 and sd.gpt4o_d_success_50[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}")
    print()
    print(f"Total tasks with success in both: {count}")

# find all tasks that overlap between  push_gp_success_200 and  push_gp_success_50
# where both have success greater than 0
def overlap_push_gp_200_50():
    count = 0
    print('PushGP 200 and 50 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.push_gp_success_200[task] > 0 and sd.push_gp_success_50[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}")
    print()
    print(f"Total tasks with success in both: {count}")

# find all tasks that overlap between  gpt4o_t_success_200 and  gpt4o_t_success_50
# where both have success greater than 0
def overlap_gpt4o_t_200_50():
    count = 0
    print('GPT-4o-T 200 and 50 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.gpt4o_t_success_200[task] > 0 and sd.gpt4o_t_success_50[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}")
    print()
    print(f"Total tasks with success in both: {count}")

# find all tasks that overlap between  gpt4o_dt_success_200 and  gpt4o_dt_success_50
# where both have success greater than 0
def overlap_gpt4o_dt_200_50():
    count = 0
    print('GPT-4o-DT 200 and 50 Cases Overlap Successes')
    for task in sd.psb2_tasks:
        if sd.gpt4o_dt_success_200[task] > 0 and sd.gpt4o_dt_success_50[task] > 0:
            # check who has the greater success
            count += 1
            print(f"{task}")
    print()
    print(f"Total tasks with success in both: {count}")


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Generate successes for PSB2 tasks.')
    args.add_argument('--data_dir', type=str, help='Directory to save the results.')
    args = args.parse_args()

    overlap_200_pushgp_gpt4o_dt()
    print('#' * 50)
    pushgp_zero_gpt4o_dt_200()
    print('#' * 50)
    gpt4o_dt_zero_pushgp_200()
    print('#' * 50)
    union_gpt4o_dt_pushgp_200()
    print('#' * 50)
    overlap_200_pushgp_gpt4o_d()
    print('#' * 50)
    pushgp_zero_gpt4o_d_200()
    print('#' * 50)
    gpt4o_d_zero_pushgp_200()
    print('#' * 50)
    union_gpt4o_d_pushgp_200()
    print('#' * 50)
    overlap_gpt4o_d_gpt4o_dt_200()
    print('#' * 50)
    overlap_gpt4o_t_gpt4o_dt_200()
    print('#' * 50)
    gpt4o_dt_zero_gpt4o_d_t_200()
    print('#' * 50)
    overlap_gpt4o_d_200_50()
    print('#' * 50)
    overlap_push_gp_200_50()
    print('#' * 50)
    overlap_gpt4o_t_200_50()
    print('#' * 50)
    overlap_gpt4o_dt_200_50()