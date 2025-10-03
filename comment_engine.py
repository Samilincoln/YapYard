import time
import random
import traceback
from typing import List, Dict
from agents import AgentRegistry
from crewai import Agent, Task, Crew
from textwrap import shorten



class CommentEngine:
    """Generates realistic comments using CrewAI agents"""
    
    def __init__(self, agent_registry: AgentRegistry):
        self.agent_registry = agent_registry

        self.summarizer_agent = Agent(
            name="Summarizer",
            role="Condenses long content",
            goal="Summarize input into <=200 words while preserving key ideas",
            backstory="Expert at summarizing long text into digestible summaries"
        )

    def _prepare_content(self, content: str, max_chars: int = 800) -> str:
        """Summarize or truncate overly long content"""
        if len(content) > max_chars:
            try:
                summary_task = Task(
                    description=f"Summarize this text into <=200 words:\n\n{content}",
                    agent=self.summarizer_agent,
                    expected_output="Concise summary of the text"
                )
                crew = Crew(agents=[self.summarizer_agent], tasks=[summary_task], verbose=False)
                summary = str(crew.kickoff()).strip()
                return summary if summary else shorten(content, width=max_chars, placeholder="... [truncated]")
            except Exception:
                # fallback: safe truncation
                return shorten(content, width=max_chars, placeholder="... [truncated]")
        return content
    
    def generate_comments(self, content: str, selected_agents: List[str], num_comments: int) -> List[Dict]:
        """Generate comments from selected agents"""
        comments = []
        agents = self.agent_registry.get_all_agents()
        
        # Create a pool of selected agent names
        selected_agent_names_pool = [name for name in selected_agents if name in agents]
        
        if not selected_agent_names_pool:
            return []

        # 🔹 ensure safe content
        safe_content = self._prepare_content(content)
        
        for i in range(num_comments):
            # Randomly select an agent name from the pool
            selected_agent_name = random.choice(selected_agent_names_pool)
            selected_agent = agents[selected_agent_name] # Get the Agent object using the name
            
            # Create a task for the agent
            comment_task = Task(
                description=f"""
                You are commenting on this content: "{safe_content}"
                
                Write a short realistic social media comment that reflects your personality and goals.
                The comment should be:
                - Authentic to your character
                - 1-3 sentences long
                - Written in casual social media style
                - Engaging and realistic
                
                Do not include any meta-commentary or explanations, just write the comment as if you're responding directly to the content.
                """,
                agent=selected_agent,
                expected_output="A single social media comment responding to the content"
            )
            
            # Create a crew with just this agent
            crew = Crew(
                agents=[selected_agent],
                tasks=[comment_task],
                verbose=False
            )
            
            try:
                # Generate the comment
                result = crew.kickoff()
                comment_text = str(result).strip()
                
                # Clean up the comment (remove any unwanted formatting)
                comment_text = self._clean_comment(comment_text)
                
                comments.append({
                    'author': selected_agent_name,
                    'text': comment_text,
                    'timestamp': f"{random.randint(1, 60)}m ago"
                })
                
            except Exception as e:
                # Log the actual error with traceback
                traceback_str = traceback.format_exc()
                print(traceback_str)  # Log the traceback for debugging

                # Fallback comment if generation fails
                comments.append({
                    'author': selected_agent_name,
                    'text': "[Comment generation failed: An error occurred]",
                    'timestamp': f"{random.randint(1, 60)}m ago"
                })
        
        return comments

    def generate_reply(self, original_content: str, original_comment_author: str, original_comment_text: str, user_reply: str, agent_to_reply: str) -> Dict:
        """Generate a reply from a specific agent to a user's comment"""
        agents = self.agent_registry.get_all_agents()
        selected_agent = agents.get(agent_to_reply)

        if not selected_agent:
            raise ValueError(f"Agent '{agent_to_reply}' not found.")

        safe_content = self._prepare_content(original_content)

        reply_task = Task(
            description=f"""
            You are participating in a social media discussion.
            Original content: "{safe_content}"
            Original comment from {original_comment_author}: "{original_comment_text}"
            User's reply to the original comment: "{user_reply}"

            Your task is to generate a realistic social media reply from your persona ({agent_to_reply}) to the user's reply.
            The reply should be:
            - Authentic to your character and consistent with your previous comment (if any).
            - 1-2 sentences long.
            - Written in casual social media style.
            - Engaging and realistic.
            - Directly address the user's reply.

            Do not include any meta-commentary or explanations, just write the reply as if you're responding directly to the user.
            """,
            agent=selected_agent,
            expected_output="A single social media reply to the user's comment"
        )

        crew = Crew(
            agents=[selected_agent],
            tasks=[reply_task],
            verbose=False
        )

        try:
            result = crew.kickoff()
            reply_text = str(result).strip()
            reply_text = self._clean_comment(reply_text)

            return {
                'author': agent_to_reply,
                'text': reply_text,
                'timestamp': f"{random.randint(1, 60)}s ago" # Replies are more recent
            }
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return {
                'author': selected_agent.name,
                'text': f"[Reply generation failed: {str(e)}",
                'timestamp': f"{random.randint(1, 60)}s ago"
            }

    def _clean_comment(self, comment: str) -> str:
        """Clean up generated comment text"""
        # Remove common unwanted prefixes/suffixes
        unwanted_phrases = [
            "Here's my comment:",
            "Comment:",
            "My response:",
            "Response:",
            "As ",
            "I think",
            "In my opinion",
        ]
        
        comment = comment.strip()
        
        # Remove quotes if the entire comment is wrapped in them
        if comment.startswith('"') and comment.endswith('"'):
            comment = comment[1:-1]
        
        return comment[:600]  # Limit length like Twitter