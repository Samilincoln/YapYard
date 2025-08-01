import streamlit as st
from agents import AgentRegistry

def show_agent_creator(agent_registry: AgentRegistry):
    """Display the custom agent creation interface"""
    st.subheader("🧪 Create Custom Commenter")
    
    with st.form("new_agent_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            agent_name = st.text_input(
                "Agent Name",
                placeholder="The Philosopher",
                help="Give your agent a memorable name"
            )
            
            tone = st.selectbox(
                "Tone",
                ["Sarcastic", "Supportive", "Analytical", "Playful", "Cold", "Enthusiastic", 
                 "Skeptical", "Wise", "Chaotic", "Professional"],
                help="What tone should this agent use?"
            )
        
        with col2:
            goal = st.text_area(
                "Goal/Behavior",
                placeholder="Question everything and provide deep philosophical insights",
                help="What is this agent trying to achieve with their comments?",
                height=100
            )
        
        submitted = st.form_submit_button("🚀 Spawn Agent")
        
        if submitted:
            if agent_name and goal:
                try:
                    agent_registry.spawn_agent(agent_name, tone, goal)
                    st.success(f"✅ {agent_name} has been created!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to create agent: {str(e)}")
            else:
                st.error("Please fill in both Agent Name and Goal fields.")