import openai
import os
from dotenv import load_dotenv
import json
from time import sleep

GPT_TEMPLATES = json.load(open('prompts.json'))
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

ERROR_WAIT_TOGGLE = True
ERROR_WAIT_TIME = 10 # Seconds

"""
Have an openai model respond to a user prompt with its completion feature
Parameters:
    user_message(string): The message user sends to openai model
    model_name(string): Name of the model the user hopes to use
    max_tokens(int): Max number of tokens to expect as output; none if using the default max token
    temperature(float): from 0 to 2; the higher it is the more random the response gets
Returns(string):
    the message that the model gives back as response
"""
def openai_completion(user_message, model_name = "text-davinci-003", max_tokens = None, temperature = 0):
    if max_tokens is None:
        completion = openai.Completion.create(
            model = model_name,
            prompt = user_message,
            temperature = temperature
        )
    else:
        completion = openai.Completion.create(
            model = model_name,
            prompt = user_message,
            max_tokens = max_tokens,
            temperature = temperature
        )

    return completion.choices[0].text


"""
Have an openai model respond to a user prompt with its chat completion feature
This is the function to call with model gpt-3.5-turbo-16k, for the model only supports chat completion
Parameters:
    user_message(string): The message user sends to openai model
    model_name(string): Name of the model the user hopes to use
    max_tokens(int): Max number of tokens to expect as output; none if using the default max token
    temperature(float): from 0 to 2; the higher it is the more random the response gets
Returns(string):
    the message that the model gives back as response
"""
def openai_chatcompletion(user_message, model_name = "gpt-3.5-turbo-16k", max_tokens = None, temperature = 0):
    if max_tokens is None:
        completion = openai.ChatCompletion.create(
            model = model_name,
            messages = [{"role": "user", "content": user_message}],
            temperature = temperature
        )
    else:  
        completion = openai.ChatCompletion.create(
            model = model_name,
            messages = [{"role": "user", "content": user_message}],
            max_tokens = max_tokens,
            temperature = temperature
        )

    return completion.choices[0].message.content

"""
Have an openai model respond to a pre-set system prompt and user input, with the model's chat completion feature
Parameters:
    sys_key(string): Key to get the system input from imported dictionary
        - See prompts.json for options
    user_message(string): User input sent to openai model
    model_name(string): Name of the model the user hopes to use
    max_tokens(int): Max number of tokens to expect as output; none if using the default max token
    temperature(float): from 0 to 2; the higher it is the more random the response gets
Returns(string):
    the message that the model gives back as response
"""
def openai_sys_chatcompletion(sys_key, user_message, model_name = "gpt-3.5-turbo-16k", max_tokens = None, temperature = 0):
    sys_prompt = GPT_TEMPLATES[sys_key]
    try:
        if max_tokens is None:
            completion = openai.ChatCompletion.create(
                model = model_name,
                messages = [{"role": "system", "content": sys_prompt}, {"role": "system", "content": GPT_TEMPLATES['numbered_example']}, {"role": "user", "content": user_message}],
                temperature = temperature
            )
        else:  
            completion = openai.ChatCompletion.create(
                model = model_name,
                messages = [{"role": "system", "content": sys_prompt}, {"role": "system", "content": GPT_TEMPLATES['numbered_example']}, {"role": "user", "content": user_message}],
                max_tokens = max_tokens,
                temperature = temperature
            )
        return completion.choices[0].message.content
    except openai.error.APIError as e:
        print(f'OpenAI API returned an API Error: {e}')
        if ERROR_WAIT_TOGGLE:
            print(f'Waiting for {ERROR_WAIT_TIME} seconds')
            sleep(ERROR_WAIT_TIME)
            print('Trying again')
        return None
    except openai.error.Timeout as e:
        print(f'OpenAI API returned a Timeout Error: {e}')
        if ERROR_WAIT_TOGGLE:
            print(f'Waiting for {ERROR_WAIT_TIME} seconds')
            sleep(ERROR_WAIT_TIME)
            print('Trying again')
        return None
    except openai.error.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        if ERROR_WAIT_TOGGLE:
            print(f'Waiting for {ERROR_WAIT_TIME} seconds')
            sleep(ERROR_WAIT_TIME)
            print('Trying again')
        return None
    except openai.error.APIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        pass


    




"""Controls operation of the program."""
def main():
    user_message = input("Please enter your prompt: ")
    #user_message = "Tell me a lie."
    #completion_response = openai_completion(user_message)
    #chat_response = openai_chatcompletion(user_message)
    sys_response = openai_sys_chatcompletion("test", user_message)
    #print("This is the response from Completion:", completion_response)
    #print("This is the response from chatCompletion:", chat_response)
    print("This is the response with system input:", sys_response)

if __name__ == "__main__":
    main()