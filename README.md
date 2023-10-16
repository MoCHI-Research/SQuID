# SQuID
Research for a qualitative analysis system

# Introduction
This system aims to help with qualitative data analysis, or more specifically, making affinity diagrams. With the assistance of LLMs(Large Language Models), which currently includes GPT-3.5 and GPT-4 by OpenAI, the system helps to group pieces of qualitative data and gives a label to each of the group. The motivation behind this system is that, although the existing LLMs are capable of grouping and labeling data, they have a few limitations, the most significant of which being that the models cannot handle realistically sized datasets due to token limits of the LLMs. 

The basic idea of SQuID is to give the LLM a batch of data within its token limit at a time, asking the model to group and label the data. After all individual data points in a dataset are labeled, the system uses the Girvan-Newman algorithm to find similar labels, and merges the groups with similar labels. This would resolve the token-limit issue as well as avoid having an unnecessary large number of groups, which is not helpful in an affinity diagram.

# Dependencies
SQuID is written mainly in Python and requires the following Python libraries. Built-in Python packages are not in this list.

- openai
- networkx
- pandas
- matplotlib
- plotly
- python-dotenv
- customtkinter
- scikit-learn

We are planning on writing a script that helps the user install all these packages at once. In addition, for future developers please feel free to add to this list if you find a required library that we have missed in this list.

# Other prerequisites
Because SQuID uses the API service provided by OpenAI, you need to have access to OpenAI APIs in order to use the system.

With a registered OpenAI account, go to https://platform.openai.com/account/api-keys to create a secret key for you or your organization.
Create a file in the SQuID folder named ".env", which sets up an environment for the program. In the file, you should enter "OPENAI_API_KEY = " followed by your OpenAI secret key. You might need to create the file using a text editor, if you are on MacOS.

With these prerequisites set up, you should be good to go for running SQuID to analyze data!
