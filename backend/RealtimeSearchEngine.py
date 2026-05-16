# Impoet the googlesearch libray to use the search function.
from googlesearch import search

# Importing the Groq library to use its API.
from groq import Groq

# Importing functions to read and write JSON files.  
from json import load, dump 

# Importing the datetime module for real-time date and time information.
import datetime 

# Importing dotenv_values to read environment variables from a .env file. 
from dotenv import dotenv_values

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve specific environment variables for username, assistant name, and API key.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using the provided API key.
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages.
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior.
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# Attempt to load the chat log from a JSON file.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)  # Load existing messages from the chat log.
except FileNotFoundError:
    # If the file doesn't exist, create an empty JSON file to store chat logs.
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

# Funtion to perform a Google search and format the results. 
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search result for {query} are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer 

# Function to modify the chatbot's response for better formatting.
def AnswerModifier(Answer):
    lines = Answer.split('\n') # Split the response into lines.
    non_empty_lines = [line for line in lines if line.strip()] # Remove empty lines.
    modified_answer = '\n'.join(non_empty_lines) # Join the cleaned lines back together.
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "system", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I be of assistance?"}
]

#Function to get real-time date and time information.        
def Information():
    data = ""
    current_date_time = datetime.datetime.now() # Get the current date and time.
    day = current_date_time.strftime("%A") # Day of the week.
    date = current_date_time.strftime("%d") # Day of the month.
    month = current_date_time.strftime("%B") # Full month name.
    year = current_date_time.strftime("%Y") # Year.
    hour = current_date_time.strftime("%H") # Hour in 24-hour format.
    minute = current_date_time.strftime("%M") # Minute.
    second = current_date_time.strftime("%S") # Second.

    # Format the information into a string.
    data = f"Use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data

# Fucntion to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    #Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})    

    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role" : "system", "content" :  GoogleSearch(prompt)})

    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = " "

    # Concatenate response chunks  from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "" )
    messages.append({"role": "assistant", "content": Answer})

    # Save the updates chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

# Main entry pint of the program for interractive querrying.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))