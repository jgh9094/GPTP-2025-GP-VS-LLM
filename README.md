# GPTP 2025 - GP and LLMs for Program Synthesis: No Clear Winners

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15171303.svg)](https://doi.org/10.5281/zenodo.15171303)
[![data](https://img.shields.io/badge/go_to-data-9807FF)](https://osf.io/s7vhj/)

## Abstract

> Genetic programming (GP) and large language models (LLMs) differ in how program specifications are provided: GP uses input-output examples, and LLMs use text descriptions.
In this work, we compared the ability of PushGP and GPT-4o to synthesize computer programs for tasks from the PSB2 benchmark suite.
We used three prompt variants with GPT-4o: input-output examples (data-only), textual description of the task (text-only), and a combination of both textual descriptions and input-output examples (data-text).
Additionally, we varied the number of input-output examples available for building programs.
For each synthesizer and task combination, we compared success rates across all program synthesizers, as well as the similarity between successful GPT-4o synthesized programs.
We found that the combination of PushGP and GPT-4o with data-text prompting led to the greatest number of tasks solved (23 of the 25 tasks), even though several tasks were solved exclusively by only one of the two synthesizers.
We also observed that PushGP and GPT-4o with data-only prompting solved fewer tasks with the decrease in the training set size, while the remaining synthesizers saw no decrease.
We also detected significant differences in similarity between the successful programs synthesized for GPT-4o with text-only and data-only prompting.
With there being no dominant program synthesizer, this work highlights the importance of different optimization techniques used by PushGP and LLMs to synthesize programs.

## Repository guide

Datasets used in the experiments. The `Task ID' refers to the identifier used to extract the dataset from OpenML. The other columns denote the number of rows, columns, and classes for each dataset.

- `Data-Tools/`: all scripts related to data checking, collecting, and visualizing
  - `GPT-4o-Similarity/`: all scripts related to analyzing data for the similarity results
  - `Paper-Results/`: scripts for the results found within the paper
- `GPT-4o-Source/`: all scripts related to generating results for GPT-4o
  - For questions regarding this folder, please contact Gabriel Ketron at gabrielketron@gmail.com
- `PushGP-Source/`: all scripts related to generating results for PushGP