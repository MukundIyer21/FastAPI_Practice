from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

engine = create_engine('sqlite:///todo.db', echo=True)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship('Task', back_populates='user', cascade='all, delete-orphan')

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    is_completed = Column(Boolean, default=False)
    priority = Column(Integer, default=0)  # 0=low, 1=medium, 2=high
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship('User', back_populates='tasks')

if __name__=="__main__":
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # user1 = User(
    #     username='john_doe',
    #     email='john@example.com',
    #     password_hash='hashed_password_123'
    # )
    
    # user2 = User(
    #     username='jane_smith',
    #     email='jane@example.com',
    #     password_hash='hashed_password_456'
    # )
    
    # session.add(user1)
    # session.add(user2)
    # session.commit()
    
    
    # task1 = Task(
    #     user_id=user1.id,
    #     title='Buy groceries',
    #     description='Milk, eggs, bread, and fruits',
    #     priority=1,
    #     is_completed=False
    # )
    
    # task2 = Task(
    #     user_id=user1.id,
    #     title='Complete project report',
    #     description='Finish Q4 report and submit',
    #     priority=2,
    #     due_date=datetime(2025, 11, 20),
    #     is_completed=False
    # )
    
    # task3 = Task(
    #     user_id=user1.id,
    #     title='Call dentist',
    #     description='Schedule appointment for next week',
    #     priority=0,
    #     is_completed=True
    # )
    
    
    # task4 = Task(
    #     user_id=user2.id,
    #     title='Prepare presentation',
    #     description='Create slides for Monday meeting',
    #     priority=2,
    #     due_date=datetime(2025, 11, 18),
    #     is_completed=False
    # )
    
    # task5 = Task(
    #     user_id=user2.id,
    #     title='Review code',
    #     description='Review pull requests',
    #     priority=1,
    #     is_completed=False
    # )
    
    # session.add_all([task1, task2, task3, task4, task5])
    # session.commit()
    
    print("Database initialized with sample data!")
    print(f"Created {session.query(User).count()} users")
    print(f"Created {session.query(Task).count()} tasks")
    
    session.close()