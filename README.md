# SQuID
Research for a qualitative analysis system

# Introduction
This system aims to help with qualitative data analysis, or more specifically, making affinity diagrams. With the assistance of LLMs(Large Language Models), which currently includes GPT-3.5 and GPT-4 by OpenAI, the system helps to group pieces of qualitative data and gives a label to each of the group. The motivation behind this system is that, although the existing LLMs are capable of grouping and labeling data, they have a few limitations, the most significant of which being that the models cannot handle realistically sized datasets due to token limits of the LLMs. 

The basic idea of SQuID is to give the LLM a batch of data within its token limit at a time, asking the model to group and label the data. After all individual data points in a dataset are labeled, the system uses the Girvan-Newman algorithm to find similar labels, and merges the groups with similar labels. This would resolve the token-limit issue as well as avoid having an unnecessary large number of groups, which is not helpful in an affinity diagram.

# Dependencies
**Note that currently SQuID only works with Python 3.11(and below) and openai 0.28.1(and below). We will work to keep SQuID up-to-date soon**

SQuID is written mainly in Python. **With Python 3.11 on your computer, you can easily install all the dependencies by running python on install_dependency.py.** 

`python install_dependency.py`
or
`python3 install_dependency.py`

The specific packages required are:

- openai==0.28.1
- networkx
- pandas
- matplotlib
- plotly
- python-dotenv
- customtkinter
- scikit-learn

# To Run SQuID
To run SQuID, run Python on main.py. A GUI interface will then show up.

`python main.py`
or
`python3 main.py`

# Data Format
To run SQuID, your data should be in a csv file, with each piece of data on its own line.
We have formatted sample datasets in the "datasets" directory. Your data should be in the same format.

# Running SQuID
Although we have developed a primitive GUI for SQuID, we have not adapted everything to GUI. While you are working on SQuID, the program might freeze or spend long time responding at points. This means that we are trying to get results from OpeanAI's API. If you ran SQuID through the terminal, as specified above, you can just refer to the terminal for progress information and updates.

Thank you so much for using SQuID!


