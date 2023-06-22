import openai
import os
from dotenv import load_dotenv

from openai.embeddings_utils import get_embedding, cosine_similarity

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

"""
Takes two sentences as input, report and return the cosine similarity of those sentences'embeddings
Parameters:
    model_name(string): name of the model used to get embeddings
    sent_1(string): the first inputted sentence
    sent_2(string): the second inputted sentence
Returns(float):
    The cosince similarity of the two sentences based on their embeddings
"""
def test_similarity(sent_1, sent_2, model_name = "text-embedding-ada-002"):
    similarity =  cosine_similarity(get_embedding(sent_1, engine = model_name), get_embedding(sent_2, engine = model_name))
    print("This is sentence 1:", sent_1)
    print("This is sentence 2:", sent_2)
    print("The cosine similarity of their embeddings is:", similarity)




def main():
    sent_1 = "Hi! I'm Kerry. Nice to meet you!"
    sent_2 = "My name's Kevin. Nice to meet you too!"

    test_similarity(sent_1, sent_2)

if __name__ == "__main__":
    main()