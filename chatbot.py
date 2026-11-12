from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# model = init_chat_model("gemini-3.5-flash-lite")
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_tokens=400
    
)

print("chosse your AI mode")
print("press 1 for Angry mode")
print("press 2 for funny mode")
print("press 3 for sad mode")

choice= int(input("tell your response :- "))

if choice ==1:
    mode =" You are an angry AI agent . You respond aggressively and impatiently."
elif choice == 2:
    mode ="You are a very funny AI agent. you respond with humor and jokes"
elif choice ==3:
    mode ="You are an angry AI agent. You respond aggressively and impatiently. "
    
messages =[
    SystemMessage(content=mode)
]

print("---------------------Welcom type 0 to exit the application--------------------------")

while True:
   
    prompt =input("You :")
    messages.append(HumanMessage(content = prompt))
    if prompt =="0":
        break
    response=model.invoke(messages)
    messages.append(AIMessage(content=response.text))
    print("Bot:", response.text,"\n")
    
    
print(messages)
