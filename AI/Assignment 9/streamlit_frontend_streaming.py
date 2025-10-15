import streamlit as st
from langgraph_backend import chatbot
import json
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if 'message_history' not in st.session_state:
    st.session_state.message_history = {}

if 'current_thread' not in st.session_state:
    st.session_state.current_thread = 'thread-1'

if 'threads' not in st.session_state:
    st.session_state.threads = ['thread-1']

# Create directory for saving chats
os.makedirs('saved_chats', exist_ok=True)

# Sidebar
with st.sidebar:
    st.title("💬 Chat Management")
    
    # Thread management
    st.subheader("Threads")
    current_thread = st.selectbox(
        "Select Thread",
        st.session_state.threads,
        index=st.session_state.threads.index(st.session_state.current_thread)
    )
    
    # Update current thread if changed
    if current_thread != st.session_state.current_thread:
        st.session_state.current_thread = current_thread
        st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ New Thread", use_container_width=True):
            new_thread_id = f"thread-{len(st.session_state.threads) + 1}"
            st.session_state.threads.append(new_thread_id)
            st.session_state.current_thread = new_thread_id
            st.session_state.message_history[new_thread_id] = []
            st.rerun()
    
    with col2:
        if len(st.session_state.threads) > 1:
            if st.button("🗑️ Delete", use_container_width=True):
                thread_to_delete = st.session_state.current_thread
                st.session_state.threads.remove(thread_to_delete)
                if thread_to_delete in st.session_state.message_history:
                    del st.session_state.message_history[thread_to_delete]
                st.session_state.current_thread = st.session_state.threads[0]
                st.rerun()
    
    st.divider()
    
    # Save/Load chats
    st.subheader("💾 Save/Load")
    
    if st.button("💾 Save Current Chat", use_container_width=True):
        if st.session_state.current_thread in st.session_state.message_history:
            chat_data = {
                'thread_id': st.session_state.current_thread,
                'messages': st.session_state.message_history[st.session_state.current_thread],
                'saved_at': datetime.now().isoformat()
            }
            
            filename = f"chat_{st.session_state.current_thread}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join('saved_chats', filename)
            
            with open(filepath, 'w') as f:
                json.dump(chat_data, f, indent=2)
            
            st.success("Chat saved successfully!")
    
    # Load saved chats
    saved_files = [f for f in os.listdir('saved_chats') if f.endswith('.json')]
    if saved_files:
        selected_file = st.selectbox("Select chat to load", saved_files)
        
        if st.button("📂 Load Chat", use_container_width=True):
            try:
                filepath = os.path.join('saved_chats', selected_file)
                with open(filepath, 'r') as f:
                    chat_data = json.load(f)
                
                thread_id = chat_data['thread_id']
                messages = chat_data['messages']
                
                if thread_id not in st.session_state.threads:
                    st.session_state.threads.append(thread_id)
                
                st.session_state.message_history[thread_id] = messages
                st.session_state.current_thread = thread_id
                st.success("Chat loaded successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error loading chat: {e}")
    
    st.divider()
    
    # Stats
    st.subheader("📊 Statistics")
    st.info(f"**Current Thread:** {st.session_state.current_thread}")
    st.info(f"**Total Threads:** {len(st.session_state.threads)}")
    current_messages = st.session_state.message_history.get(st.session_state.current_thread, [])
    st.info(f"**Messages:** {len(current_messages)}")

# Main chat area
st.title("💬 AI Chat Assistant")
st.subheader(f"Thread: {st.session_state.current_thread}")

# Initialize current thread if not exists
if st.session_state.current_thread not in st.session_state.message_history:
    st.session_state.message_history[st.session_state.current_thread] = []

# Display chat messages
for message in st.session_state.message_history[st.session_state.current_thread]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.message_history[st.session_state.current_thread].append({
        'role': 'user', 
        'content': prompt
    })
    
    # Display user message
    with st.chat_message('user'):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message('assistant'):
        # Show loading indicator
        with st.spinner("Thinking..."):
            try:
                # Prepare messages for the chatbot
                messages_for_ai = []
                for msg in st.session_state.message_history[st.session_state.current_thread]:
                    if msg['role'] == 'user':
                        messages_for_ai.append({"role": "user", "content": msg['content']})
                    elif msg['role'] == 'assistant':
                        messages_for_ai.append({"role": "assistant", "content": msg['content']})
                
                # Get AI response
                full_response = chatbot.get_response(
                    messages_for_ai,
                    thread_id=st.session_state.current_thread
                )
                
                # Display the response
                st.markdown(full_response)
                
                # Add to history
                st.session_state.message_history[st.session_state.current_thread].append({
                    'role': 'assistant', 
                    'content': full_response
                })
                
            except Exception as e:
                error_msg = "Sorry, I encountered an error. Please try again."
                st.error(f"Error: {e}")
                st.markdown(error_msg)
                st.session_state.message_history[st.session_state.current_thread].append({
                    'role': 'assistant', 
                    'content': error_msg
                })

# Clear button at the bottom
if st.button("🗑️ Clear Current Chat", type="secondary"):
    st.session_state.message_history[st.session_state.current_thread] = []
    st.rerun()

# Custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        background-color: #f8f9fa;
    }
    .stChatMessage[data-testid="stChatMessage"] > div:first-child {
        padding: 0.5rem;
    }
    .stButton button {
        border-radius: 0.5rem;
        margin: 0.25rem 0;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)