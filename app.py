import streamlit as st
import os
from agents import AgentRegistry
from comment_engine import CommentEngine
from new_agent import show_agent_creator
from utils import format_content_preview, calculate_heat_rating, get_toxicity_level
import time

import chromadb

# Force Chroma to use DuckDB instead of SQLite
import chromadb

client = chromadb.Client() 


# Configure page
st.set_page_config(
    page_title="YapYard - Comment Arena",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.comment-box {
    background-color: #0c0c12;
    border-left: 4px solid #007bff;
    padding: 12px;
    margin: 8px 0;
    border-radius: 4px;
}

.comment-author {
    font-weight: bold;
    color: #007bff;
    margin-bottom: 4px;
}

.comment-text {
    margin-bottom: 4px;
    line-height: 1.4;
}

.comment-timestamp {
    font-size: 0.8em;
    color: #6c757d;
}

.heat-rating {
    font-size: 1.2em;
    font-weight: bold;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    background: linear-gradient(45deg, #ff6b6b, #ffa500);
    color: white;
}

.stAlert > div {
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

def main():
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.switch_page("pages/login.py")
        return

    # Initialize session state
    if 'agent_registry' not in st.session_state:
        st.session_state.agent_registry = AgentRegistry()
    
    if 'comment_engine' not in st.session_state:
        st.session_state.comment_engine = CommentEngine(st.session_state.agent_registry)
    
    if 'generated_comments' not in st.session_state:
        st.session_state.generated_comments = []
    if 'current_content' not in st.session_state:
        st.session_state.current_content = ""
    
    # Header
    st.title("🗣️ YapYard")
    st.markdown("*A simulated comment arena for creators to overcome posting anxiety.*")
    

    
    # Sidebar
    with st.sidebar:

        # Logout button
        if st.button("Logout"):
            st.session_state.clear()
            st.switch_page("pages/login.py")
        st.divider()
        
        
        st.header("🎛️ Controls")
        
        # Agent selection
        st.subheader("Select Commenters")
        available_agents = st.session_state.agent_registry.get_agent_names()
        
        selected_agents = st.multiselect(
            "Choose personality types:",
            available_agents,
            default=["The Critic", "The Supportive Friend", "The Analyst","The Nigerian"],
            help="Select which types of commenters you want to simulate"
        )
        
        # Number of comments
        num_comments = st.slider(
            "Number of Comments",
            min_value=1,
            max_value=20,
            value=5,
            help="How many comments to generate"
        )
        
        st.divider()
        
        # Custom agent creator
        show_agent_creator(st.session_state.agent_registry)
        st.markdown("Note that more custom agents consume more tokens.")

        

        st.divider()

        # Display custom agents
        st.subheader("Your Custom Agents")
        if st.session_state.agent_registry.custom_agents:
            for agent_name, agent_obj in st.session_state.agent_registry.custom_agents.items():
                st.write(f"- {agent_name}")
        else:
            st.info("No custom agents spawned yet.")

        st.divider()

        # Clear all comments button
        if st.button("Clear All Comments", help="Removes all generated comments from display."):
            st.session_state.generated_comments = []
            st.session_state.current_content = ""
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Your Content")
        
        # Content input
        st.session_state.current_content = st.text_area(
            "Paste your content here:",
            value=st.session_state.current_content,
            placeholder="Enter your tweet, caption, script, or any content you want feedback on...",
            height=150,
            help="This is the content that will be commented on"
        )
        content = st.session_state.current_content
        
        # Generate button
        if st.button("🚀 Generate Comments", type="primary", disabled=not st.session_state.current_content or not selected_agents):
            if st.session_state.current_content and selected_agents:
                with st.spinner("Generating comments... This may take a moment."):
                    try:
                        comments = st.session_state.comment_engine.generate_comments(
                            st.session_state.current_content, selected_agents, num_comments
                        )
                        st.session_state.generated_comments = comments
                        st.success(f"Generated {len(comments)} comments!")
                    except Exception as e:
                        st.error(f"Error generating comments: {str(e)}")
        
        # Display comments
        if st.session_state.generated_comments:
            st.header("💬 Simulated Comments")
            
            for i, comment in enumerate(st.session_state.generated_comments):
                st.markdown(f"""
                <div class="comment-box">
                    <div class="comment-author">{comment['author']}</div>
                    <div class="comment-text">{comment['text']}</div>
                    <div class="comment-timestamp">{comment['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Reply section
                with st.expander(f"Reply to {comment['author']}"):
                    user_reply_key = f"user_reply_{i}"
                    reply_button_key = f"reply_button_{i}"

                    user_reply_text = st.text_area(
                        "Your reply:",
                        key=user_reply_key,
                        placeholder="Type your reply here..."
                    )
                    if user_reply_text:
                        st.session_state.generated_comments[i]['user_reply'] = user_reply_text

                    if st.button("Send Reply", key=reply_button_key, disabled=not user_reply_text):
                        with st.spinner("Generating agent's reply..."):
                            try:
                                # Assuming the agent who made the original comment will reply
                                agent_to_reply = comment['author']
                                
                                reply = st.session_state.comment_engine.generate_reply(
                                    st.session_state.current_content, 
                                    comment['author'], 
                                    comment['text'], 
                                    user_reply_text, 
                                    agent_to_reply
                                )
                                if 'replies' not in comment:
                                    comment['replies'] = []
                                comment['replies'].append(reply)
                                st.success("Reply generated!")
                                # Store the user's reply in the comment object
                                st.session_state.generated_comments[i]['user_reply'] = user_reply_text
                                # Clear the text area after sending
                                st.session_state[user_reply_key] = ""
                            except Exception as e:
                                st.error(f"Error generating reply: {str(e)}")
                        st.rerun()

                # Display replies if any
                if 'replies' in comment and comment['replies']:
                    # Display user's reply if it exists
                    if 'user_reply' in comment and comment['user_reply']:
                        st.markdown(f"""
                        <div class="comment-box" style="margin-left: 20px; border-left: 4px solid #6c757d;">
                            <div class="comment-author">You (Your Reply)</div>
                            <div class="comment-text">{comment['user_reply']}</div>
                            <div class="comment-timestamp">Just now</div>
                        </div>
                        """, unsafe_allow_html=True)

                    for reply in comment['replies']:
                        st.markdown(f"""
                        <div class="comment-box" style="margin-left: 20px; border-left: 4px solid #6c757d;">
                            <div class="comment-author">{reply['author']} (Reply)</div>
                            <div class="comment-text">{reply['text']}</div>
                            <div class="comment-timestamp">{reply['timestamp']}</div>
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.current_content:
            st.header("📊 Content Preview")
            st.info(format_content_preview(st.session_state.current_content, 200))
            
            if st.session_state.generated_comments:
                st.header("🔥 Heat Rating")
                heat_rating = calculate_heat_rating(st.session_state.generated_comments)
                toxicity_level = get_toxicity_level(heat_rating)
                
                st.markdown(f"""
                <div class="heat-rating">
                    {heat_rating}/10<br>
                    {toxicity_level}
                </div>
                """, unsafe_allow_html=True)
                
                st.header("📈 Stats")
                st.metric("Total Comments", len(st.session_state.generated_comments))
                st.metric("Avg Comment Length", 
                         f"{sum(len(c['text']) for c in st.session_state.generated_comments) // len(st.session_state.generated_comments)} chars")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 20px;'>
        <p><strong>YapYard</strong> - Face the yard. Own the yap. Post anyway.</p>
        <p>Created by Samson Agboola © 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
