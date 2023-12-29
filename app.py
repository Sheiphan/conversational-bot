import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import time
import asyncio


class SurveyBot:
    def __init__(self, objective):
        load_dotenv()
        self.configure_logging()
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.assistant_id = os.environ.get("ASSISTANT_ID")
        self.client = OpenAI(api_key=self.api_key)
        self.objective = objective
        self.thread_id = None
        self.counter = 0

    def configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("logfile.log"),
            ],
        )

    def create_thread(self):
        try:
            thread = self.client.beta.threads.create()
            self.thread_id = thread.id
        except Exception as e:
            logging.error(f"Error creating thread: {e}")
            raise

    def send_initial_message(self):
        content = (
            f"The objective of the survey is {self.objective}. "
            "Give an introduction and purpose of the survey and invite the user to engage in a conversation. "
            "Keep the message short"
        )
        self.send_message(content)

    def send_message(self, content):
        try:
            self.client.beta.threads.messages.create(
                thread_id=self.thread_id, role="user", content=content
            )
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            raise

    def create_run(self):
        try:
            return self.client.beta.threads.runs.create(
                thread_id=self.thread_id, assistant_id=self.assistant_id
            )
        except Exception as e:
            logging.error(f"Error creating run: {e}")
            raise

    def retrieve_run(self, run_id):
        try:
            return self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run_id
            )
        except Exception as e:
            logging.error(f"Error retrieving run: {e}")
            raise

    def get_latest_message(self):
        try:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            return messages.data[0].content[0].text.value
        except Exception as e:
            logging.error(f"Error getting latest message: {e}")
            raise

    def start_conversation(self):
        self.create_thread()
        self.send_initial_message()
        run = self.create_run()
        while True:
            run = self.retrieve_run(run.id)
            if run.status == "completed":
                return self.get_latest_message()

    def start_user_question(self, user_message):
        if user_message.lower() != "exit":
            self.send_message(user_message + ". Keep it short")
            run = self.create_run()
            while True:
                run = self.retrieve_run(run.id)
                if run.status == "completed":
                    return self.get_latest_message()
        else:
            self.send_message(
                "Give a summary of the insights received through the conversation"
            )
            run = self.create_run()
            st.session_state.submit_button_state = False
            while True:
                run = self.retrieve_run(run.id)
                if run.status == "completed":
                    return "Summary: " + self.get_latest_message()


async def main():
    st.title("Conversation Chatbot")
    chat_history = st.session_state.get("chat_history", [])

    # Initialize submit_button_state if not present in the session state
    st.session_state.submit_button_state = st.session_state.get(
        "submit_button_state", False
    )

    # Check if the bot has already been created
    if "bot" not in st.session_state:
        st.session_state.bot = None

    with st.sidebar:
        objective = st.text_input("Enter the objective of the survey:")
        submit_button = st.button(
            "Submit",
            key="submit_button",
            on_click=lambda: setattr(st.session_state, "submit_button_state", True),
        )

    if st.session_state.submit_button_state:
        # Check if the bot has already been created
        if st.session_state.bot is None:
            # Create a new SurveyBot instance
            st.session_state.bot = SurveyBot(objective)

            # Initialize the thread_id in the session state
            st.session_state.thread_id = st.session_state.bot.thread_id

            # Start the conversation
            intro_message = st.session_state.bot.start_conversation()
            chat_history.append((intro_message, "assistant"))

        # Get the stored thread_id
        thread_id = st.session_state.thread_id

        prompt = st.chat_input("Response to Survey Question")
        if prompt:
            chat_history.append((prompt, "user"))
            bot_response = st.session_state.bot.start_user_question(prompt)
            chat_history.append((bot_response, "assistant"))

        # Store the updated chat_history and thread_id in the session state
        st.session_state.chat_history = chat_history
        st.session_state.thread_id = thread_id

        # Display chat history
        for message, sender in chat_history:
            with st.chat_message(sender):
                st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write("Please enter the objective of the survey before continuing.")


if __name__ == "__main__":
    asyncio.run(main())
