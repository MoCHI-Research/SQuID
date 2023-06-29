import openai
import os
import networkx
import pandas
import csv
from dotenv import load_dotenv

from openai.embeddings_utils import get_embedding, cosine_similarity

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

INTERMEDIATE_PATH = "intermediate/"

"""
Takes two sentences as input, report and return the cosine similarity of those sentences'embeddings
Parameters:
    sent_1(string): the first inputted sentence
    sent_2(string): the second inputted sentence
    model_name(string): name of the model used to get embeddings
Returns(float):
    The cosince similarity of the two sentences based on their embeddings
"""
def test_similarity(sent_1, sent_2, model_name = "text-embedding-ada-002"):
    similarity = cosine_similarity(get_embedding(sent_1, engine = model_name), get_embedding(sent_2, engine = model_name))
    print("This is sentence 1:", sent_1)
    print("This is sentence 2:", sent_2)
    print("The cosine similarity of their embeddings is:", similarity)
    return similarity


"""
Reads all grouped data from a csv file and transform into a dictionary
Parameters:
    file_name(string): name of the file to read grouped data from
Returns(dict):
    the dictionary that contains all grouped data
"""
def csv_to_dict(filename = "output.csv"):
    result_dict = {}

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            label = row[0]
            if label in result_dict:
                result_dict[label].append(row[1])
            else:
                result_dict[label] = [row[1]]
        f.close()
    
    return result_dict

"""
Get the embeddings of a list of texts; save them in a csv file
Parametgers:
    text_list(string): the list of strings to get embeddings of
    model_name(string): the model used to get embeddings   
    output_file(string): name of the file to write embedding result to 
Returns(pandas.DataFrame):
    the dataframe that saves all embeddings 
"""
def get_embeddings(text_list, model_name = "text-embedding-ada-002", output_file = INTERMEDIATE_PATH + "embeddings.csv"):
    embedding_frame = pandas.DataFrame(columns=["text"])
    embedding_frame["text"] = text_list

    embedding_frame["embedding"] = embedding_frame.text.apply(lambda x: get_embedding(x, engine = model_name))

    embedding_frame.to_csv(output_file, index=False)

    return embedding_frame

"""
Provided a dataframe containing sentences and their embeddings, find the similarity of each pair,
save them in a dataframe and save to a csv file
Parameters:
    embedding_frame(pandas.DataFrame): the dataframe that saves sentences and their embeddings
    output_file(string): name of the file to write similarity result to 
Returns(pandas.DataFrame):
    the dataframe that saves all pairs and their corresponding similarities
"""
def get_similarity(embedding_frame, output_file = INTERMEDIATE_PATH + "similarity.csv"):
    pairs = []

    for i, row1 in embedding_frame.iterrows():
        for j, row2 in embedding_frame.iterrows():
            if j > i:
                pairs.append([cosine_similarity(row1['embedding'], row2['embedding']), row1['text'], row2['text']])

    pairs.sort(reverse=True, key=lambda x: x[0])

    similarity_frame = pandas.DataFrame(pairs)
    similarity_frame.to_csv(output_file, header=False, index=False)

    return similarity_frame

"""
Given the text of an embedding list(as converted into csv format), identify all embeddings (floats) and
return them as a list
Parameters:
    list_text(string): text that contains all embeddings
    format example: "[0.98, -0.777, 0.678]" (with the brackets as string content)
Returns(list of float):
    the list of embeddings in the text
"""
def convert_text_to_list(list_text):
    list_text = list_text[1:-1]
    
    embeddings = list_text.split(', ')
    for i in range(len(embeddings)):
        embeddings[i] = float(embeddings[i])
    
    return embeddings

"""
Read label embeddings from the embedding csv file and generate a similarity data frame containing similarity
between any two labels. Save the similarities in a csv file.
Parameters:
    input_filename(string): name of the file that saves the embeddings
    output_filename(string): name of the file to save similarity
Returns(pandas.DataFrame):
    the dataframe that contains similarities of all pairs
"""
def read_generate_similarity(input_filename = INTERMEDIATE_PATH + "embeddings.csv", output_filename = INTERMEDIATE_PATH + "similarity.csv"):
    embedding_frame = pandas.read_csv(input_filename)
    for _, current_row in embedding_frame.iterrows():
        current_row['embedding'] = convert_text_to_list(current_row['embedding'])
    
    return get_similarity(embedding_frame, output_file = output_filename)

"""
Read similarity of each pair from a csv file and make a Graph that contains all pairs with similarity above 
a threshold
Parameters:
    similarity_file(string): name of the file that saves similarities
    threshold(float): only pairs with similarity above the threshold will be included in the graph
Returns(networkx.Graph):
    graph that contains all pairs with similarity above the threshold
"""
def graph_similarity(similarity_file = INTERMEDIATE_PATH + "similarity.csv", similarity_threshold = 0.905):
    result_graph = networkx.Graph()

    with open(similarity_file) as csvfile:
        readcsv = csv.reader(csvfile, delimiter=',')
        for row in readcsv:
            if len(row) > 0:
                score = float(row[0])
                i = row[1]
                j = row[2]
                if score > similarity_threshold:
                    result_graph.add_edge(i, j, weight=score)
                else:
                    break
        csvfile.close()
    return result_graph

"""
Group labels using Girvan-Newman
Parameters:
    current_graph(networkx.Graph): the graph to run Girvan-Newman on
    output_file(string): name of the file to save results
    iteration_num(int): number of iterations to run Girvan-Newman
"""
def group_labels(current_graph, output_file = INTERMEDIATE_PATH + "grouped_labels.csv", iteration_num = 2):

    communities_generator = networkx.algorithms.community.girvan_newman(current_graph)
    current_communities = []

    for i in range(0, iteration_num):
        print("One community iteration done.")
        current_communities = next(communities_generator)

    group_frame = pandas.DataFrame(sorted(map(sorted, current_communities)))
    group_frame.to_csv(output_file, header = False, index = False)

"""
Given groups of data and their labels, merge the groups based on given info about which groups to merge
Parameters:
    data_dict(dictionary): Keys are the group labels, and values are lists of data that belong to corresponding groups
    labels_to_merge(dictionary): Keys are new group labels that replace old ones, and values are lists of old labels
                                 that need to be changed
"""
def merge_labels(data_dict, labels_to_merge):
    for new_label in labels_to_merge:
        new_data = []
        for old_label in labels_to_merge[new_label]:
            if old_label in data_dict:
                new_data.extend(data_dict[old_label])
                data_dict.pop(old_label)
        data_dict[new_label] = new_data

"""
Controls operation of the program
"""
def main():
    """data_dict = csv_to_dict()
    label_list = []
    for label in data_dict:
        label_list.append(label)
    
    get_similarity(get_embeddings(label_list))"""
    #convert_text_to_list([])

    group_labels(graph_similarity())

    #print(intermediate_path)

if __name__ == "__main__":
    main()