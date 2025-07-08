from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from datetime import datetime
from database import Base

class AgentInteraction(Base):
    __tablename__ = 'agent_interactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_type = Column(String(50), nullable=False)
    user_input = Column(Text, nullable=False)
    agent_response = Column(JSON, nullable=False)
    sources_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AgentInteraction {self.id}: {self.agent_type}>'

class GeneratedQuiz(Base):
    __tablename__ = 'generated_quizzes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(255), nullable=False)
    quiz_data_json = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GeneratedQuiz {self.id}: {self.topic}>'