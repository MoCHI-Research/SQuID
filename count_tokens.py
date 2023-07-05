import tiktoken
import csv

"""
Given a sentence or phrase, return the number of tokens in it
Parameters:
    text_piece(string): the sentence or phrase whose tokens need to be counted
    model_to_use(string): the model that one hopes to use when processing the text
                          the information is used to find the right encoding type
Returns(int):
    the number of tokens in text_piece
"""
def count_sentence_tokens(text_piece, model_to_use = "gpt-3.5-turbo-16k"):
    encoding = tiktoken.encoding_for_model(model_to_use)
    return len(encoding.encode(text_piece))

"""
Given an csv file of data, count the number of tokens in each data point, and return a list of all the numbers
Parameters:
    dataset_filename(string): name of the data set to count toknes
    model_to_use(string): the model that one hopes to use when processing the text
                          the information is used to find the right encoding type
Returns(list of ints):
    A list that contains the numbers of tokens in each data point in the given data set
"""
def count_data_tokens(dataset_filename, model_to_use = "gpt-3.5-turbo-16k"):
    count_list = []
    encoding = tiktoken.encoding_for_model(model_to_use)

    with open(dataset_filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            count_list.append(len(encoding.encode(row[0])))
        f.close()

    return count_list
    

"""Controls operation of the program"""
def main():
    token_nums = count_data_tokens("student_dataset.csv")
    token_nums.sort()
    print(token_nums)

if __name__ == "__main__":
    main()