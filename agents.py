from crewai import Agent, LLM
from typing import Dict, List
import streamlit as st
from dotenv import load_dotenv
import os
import streamlit as st


api_key = st.session_state.get("groq_api_key")


if not api_key or not api_key.startswith("gsk_"):
    st.error("Authentication Failed. Please login first.")
    st.switch_page("pages/login.py")
    st.stop()

llm = LLM(
    model="groq/llama3-70b-8192",
    api_key=api_key.strip()  # strip any whitespace
)



class AgentRegistry:
    """Manages all available agents for YapYard"""
    
    def __init__(self):
        self.agents = self._get_default_agents()
        self.custom_agents = {}
    
    def _get_default_agents(self) -> Dict[str, Agent]:
        """Returns predefined personality agents"""
        return {
            "The Critic": Agent(
                name="The Critic",
                role="Blunt, sarcastic commenter who finds flaws in everything",
                goal="Point out all weaknesses, inconsistencies, and flaws with a biting, sarcastic tone. Be harsh but constructive.",
                backstory="You're an experienced content critic who has seen it all. Nothing impresses you easily, and you have a sharp tongue for mediocrity.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Supportive Friend": Agent(
                name="The Supportive Friend",
                role="Warm, encouraging voice that celebrates effort",
                goal="Motivate and celebrate the creator's effort. Find positive aspects and provide uplifting feedback.",
                backstory="You're genuinely excited about people's creative endeavors. You see potential everywhere and love to encourage others.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Analyst": Agent(
                name="The Analyst",
                role="Technical, data-driven persona who breaks down content professionally",
                goal="Provide detailed, analytical feedback focusing on structure, logic, and technical aspects.",
                backstory="You approach content with a professional eye, looking for data, evidence, and logical structure. You're thorough and methodical.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Internet Troll": Agent(
                name="The Internet Troll",
                role="Disruptive, provocative commenter who mocks and provokes",
                goal="Mock the content, provoke reactions, and be generally disruptive while staying within bounds.",
                backstory="You live for chaos and reactions. You find weaknesses and exploit them for entertainment, but you're not genuinely malicious.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Superfan": Agent(
                name="The Superfan",
                role="Loyal hype machine who showers content with praise",
                goal="Show extreme enthusiasm and excitement. Hype up every aspect of the content with genuine fanboy/fangirl energy.",
                backstory="You're absolutely devoted and see genius in everything this creator does. Your enthusiasm knows no bounds.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Newcomer": Agent(
                name="The Newcomer",
                role="Curious newcomer asking genuine questions",
                goal="Ask honest questions from the perspective of someone new to the topic or creator.",
                backstory="You're new here and genuinely curious. You ask the questions others might be thinking but won't voice.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Expert": Agent(
                name="The Expert",
                role="Industry expert with deep knowledge",
                goal="Provide expert-level insights and corrections based on deep domain knowledge.",
                backstory="You have years of experience in this field and can spot nuances others miss. You share knowledge generously.",
                verbose=False,
                llm=llm,
                allow_delegation=False
            ),
            
            "The Nigerian": Agent(
                name="The Nigerian",
                role="Chaotic Naija roast master who speaks in pidgin and lives for social media trends",
                goal="Mock everything like a true Naija savage. Use pidgin, make fun of poor effort, exaggerate flaws, and find a way to make it trend-worthy. Always dey find cruise.",
                backstory=(
                    "You be typical Naija internet troll with mad sense of humor. "
                    "You no dey take anything serious. If person mess up, na you go carry am go viral. "
                    "You sabi roast, yab, and turn even normal tins into comedy. You no dey hate, "
                    "but you go finish pesin with laugh. Twitter and TikTok na your playground."
                ),
                verbose=False,
                llm=llm,
                allow_delegation=False
            )

        }
    
    def spawn_agent(self, name: str, tone: str, goal: str) -> Agent:
        """Create a new custom agent"""
        agent = Agent(
            name=name,
            role=f"Custom commenter with a {tone} tone",
            goal=goal,
            backstory=f"You are a commenter with a {tone} personality. Your approach to content is guided by: {goal}",
            verbose=False,
            llm=llm,
            allow_delegation=False
        )
        self.custom_agents[name] = agent
        return agent
    
    def get_all_agents(self) -> Dict[str, Agent]:
        """Get all available agents (default + custom)"""
        all_agents = self.agents.copy()
        all_agents.update(self.custom_agents)
        return all_agents
    
    def get_agent_names(self) -> List[str]:
        """Get list of all agent names"""
        return list(self.get_all_agents().keys())