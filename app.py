import os, json
import smtplib
from email.message import EmailMessage
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASSWORD")

client = Groq(api_key=GROQ_API_KEY)

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, How can I help you today?"}]
if "conversation_state" not in st.session_state:
        st.session_state["conversation_state"] = [{"role": "assistant", "content": "Hi, How can I help you today?"}]

def send_email(to, subject, message):

    # create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to
    msg.set_content(message)
    try:
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
        return json.dumps({"status": "success", "message": "Emails sent successfully"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

tools = [
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "This function will send an email to a client",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Receiver's email address",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Subject of email",
                        },
                        "message": {
                            "type": "string",
                            "description": "Main content of email",
                        },
                    },
                    "required": ["to", "subject", "message"],
                },
            },
        }
    ]

def chat_interface():
    st.title("GROQ-Llama-3-70b")
    for message in st.session_state.messages:
        image = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=image):
            st.markdown(message["content"])
    
    system_prompt = f'''You are a helpful assistant, who is capable of doing anything that th user asks. You are great at writing code, solving math, debugging errors, sending emails and many more.
    Let me tell you about user:
    Name: Likhith V
    working at PG-AGI as AI/ML intern
    Also studying Bachelors of Engineering in Artificial and Machine Learning
    Currently in my last semester.
    Loved learn more about AI and ML.
    Looking for a JOB.
'''
    # print("System Prompt: ", system_prompt)
    if prompt := st.chat_input("User input"):
        st.chat_message("user", avatar=USER_AVATAR).markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        conversation_context = st.session_state["conversation_state"]
        conversation_context.append({"role": "user", "content": prompt})
        context = []
         # Add system prompt to context if desired
        context.append({"role": "system", "content": system_prompt})
         # Add conversation context to context
        context.extend(st.session_state["conversation_state"])
        # Use the extracted data directly instead of performing inference again
        # print(context)
        response = client.chat.completions.create(
            messages=context,  # Pass conversation context directly
            model="llama3-70b-8192",
            tools=tools,
            tool_choice="auto", 
            temperature=2,
            max_tokens=8192,
            top_p=1,
            stop=None,
            # stream=True,
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            print("Function Call has been made")
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "send_email": send_email,
            }  # only one function in this example, but you can have multiple
            conversation_context.append(response_message)  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    to=function_args.get("to"),
                    subject=function_args.get("subject"),
                    message=function_args.get("message")
                )
                conversation_context.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=context
            )  # get a new response from the model where it can see the function response
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                st.markdown(second_response.choices[0].message.content)
            st.session_state.messages.append({"role": "assistant", "content": second_response.choices[0].message.content})
            conversation_context.append({"role": "assistant", "content": second_response.choices[0].message.content})
        else:
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                st.markdown(response.choices[0].message.content)
                # result = ""
                # res_box = st.empty()
                # for chunk in response:
                #     if chunk.choices[0].delta.content:
                #         new_content = chunk.choices[0].delta.content
                #         result += new_content   # Add a space to separate words
                #         res_box.markdown(f'{result}')
            # assistant_response = result
            st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
            conversation_context.append({"role": "assistant", "content": response.choices[0].message.content})
        
def main():
    chat_interface()
        
if __name__ == '__main__':
    main()
    # send_email("likhithv02@gmail.com", "None", "Hi")