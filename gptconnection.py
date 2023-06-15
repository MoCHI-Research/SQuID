import openai

openai.api_key = "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"

"""
Have an openai model respond to a user prompt with its completion feature
Parameters:
    user_message(string): The message user sends to openai model
    model_name(string): Name of the model the user hopes to use
    temperature(float): from 0 to 2; the higher it is the more random the response gets
Returns(string):
    the message that the model gives back as response
"""
def openai_completion(user_message, model_name = "text-davinci-003", temperature = 0):
    completion = openai.Completion.create(
        model = model_name,
        prompt = user_message,
        max_tokens = 1000,
        temperature = temperature
    )

    return completion.choices[0].text


"""
Have an openai model respond to a user prompt with its chat completion feature
This is the function to call with model gpt-3.5-turbo-16k, for the model only supports chat completion
Parameters:
    user_message(string): The message user sends to openai model
    model_name(string): Name of the model the user hopes to use
    temperature(float): from 0 to 2; the higher it is the more random the response gets
Returns(string):
    the message that the model gives back as response
"""
def openai_chatcompletion(user_message, model_name = "gpt-3.5-turbo-16k", temperature = 0):
    completion = openai.ChatCompletion.create(
        model = model_name,
        messages = [{"role": "user", "content": user_message}],
        max_tokens = 1000,
        temperature = temperature
    )

    return completion.choices[0].message.content


"""Controls operation of the program."""
def main():
    user_message = input("Please enter your prompt: ")
    #user_message = "Tell me a lie."
    completion_response = openai_completion(user_message)
    chat_response = openai_chatcompletion(user_message)
    print("This is the response from Completion:", completion_response)
    print("This is the response from chatCompletion:", chat_response)

if __name__ == "__main__":
    main()
