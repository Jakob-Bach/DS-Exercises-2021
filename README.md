# Exercises for Data Science I, winter semester 2021/2022

This repo contains the exercises for the lecture ["Data Science I"](https://dbis.ipd.kit.edu/english/3081.php) at the Karlsruhe Institute of Technology (KIT) in winter semester 2021/2022.
The exercises of the previous year are on [GitHub as well](https://github.com/Jakob-Bach/AGD-Exercises-2020).
The primary goal of the exercises is to apply basic data-science techniques to small toy datasets.

## Structure

### Exercises

`Exercise_Concept_LaTeX_snippet.txt` introduces the exercise concept (was part of the slide set for the first session of the lecture).

There are four topics:

- Exercise 1: Fundamentals
- Exercise 2: Classification
- Exercise 3: Association Rules
- Exercise 4: Clustering and Outlier Detection

For each topic, there is a programming exercise sheet, a theory-focused exercise session, and an online test.
The repo contains:

- `LaTeX` and `PDF` files of the programming-exercise sheets, plus a Python setup guide
- `Jupyter Notebooks` and `HTML` exports of the programming-exercise solutions
- `LaTeX` and `PDF` files of the exercise-session summaries
- [ILIAS](https://www.ilias.de/en/) (v7.5) exports (`zip` and `PDF`) of the online tests

### Surveys

We conducted a welcome survey on the background of the students and two evaluations.
The corresponding exports from ILIAS (`zip` and `PDF`) are in the folder `Surveys/`.
Note that we don't provide the results of the surveys.

### Lab Qualification

The lecture in the winter semester is followed by a practical course in the summer semester.
Since the beginning of 2019, aspiring participants of the practical course have to solve a qualification task first.
The materials for the 2022 edition are in the folder `Lab_Qualification/`:

- task as `LaTeX` and `PDF`
- `prepare_dataset.py` to download dataset and prepare train-test split
- `create_demo_submission.py` to create a valid prediction file (as required by the task)
- `score_students.py` to score a folder of ILIAS submissions (i.e., folder containing sub-folders named like `<<Name>>_<<uxxxx>>_<<some number>>`)

## Python Setup

From 2021/22 on, the programming language for the exercises is Python (before, we used R).
You can find the necessary steps to create an environment with all necessary dependencies here or in the file `Setup`.
We used Python 3.8, though other versions might work as well.

### `virtualenv` Environment

You can install `virtualenv` with

```bash
python -m pip install virtualenv==20.4.7
```

To set up an environment with `virtualenv`, you need to have the right Python version somewhere on your computer.
Next, run

```bash
python -m virtualenv -p <path/to/right/python/executable> <path/to/env/destination>
```

Activate the environment in Linux with

```bash
source <path/to/env/destination>/bin/activate
```

Activate the environment in Windows (note the back-slashes) with

```cmd
<path\to\env\destination>\Scripts\activate
```

To leave the environment, run

```bash
deactivate
```

### Dependency Management

After activating the environment, you can use `python` and `pip` as usual.
To install all necessary dependencies for this repo, simply run

```bash
python -m pip install -r requirements.txt
```

If you make changes to the environment and you want to persist them, run

```bash
python -m pip freeze > requirements.txt
```

### Using the Environment for Notebooks

You need to install a kernel for the environment:

```bash
ipython kernel install --user --name=ds-2021-kernel
```

After that, you should see (and be able to select) the kernel when running `Juypter Notebook` with

```bash
jupyter notebook
```
