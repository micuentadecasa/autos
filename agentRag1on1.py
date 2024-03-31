# rag_assistant_agent.py

from autogen import AssistantAgent
import streamlit as st
import matplotlib.pyplot as plt

class agentRag1on1 (AssistantAgent):
    def __init__(self, custom_prompt="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_prompt = custom_prompt
        self.all_responses = []

    def _process_received_message(self, message, sender, silent):
        # Prepend the custom prompt to the message
        custom_message = f"{self.custom_prompt}\n\n{message}"
        processed_message = super()._process_received_message(custom_message, sender, silent)
        self.all_responses.append(processed_message)
        return processed_message

    def generate_rag(self):
        keywords = ['success', 'failure', 'error', 'completed']
        keyword_counts = {keyword: sum(keyword in response for response in self.all_responses) for keyword in keywords}
        fig, ax = plt.subplots()
        ax.bar(keyword_counts.keys(), keyword_counts.values())
        ax.set_ylabel('Counts')
        ax.set_title('Keyword Frequency in Responses')
        st.pyplot(fig)
