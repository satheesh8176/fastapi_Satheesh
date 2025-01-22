import pandas as pd # type: ignore
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the base class
Base = declarative_base()

# Read the CSV file
csv_file_path = 'users.csv'
df = pd.read_csv(csv_file_path)

# Dynamically create a model based on the CSV columns
class DynamicUser(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    locals().update({col: Column(String) for col in df.columns})

    def __repr__(self):
        return f"<DynamicUser(id={self.id}, {', '.join([col for col in df.columns])})>"

# Create an engine and connect to the database (SQLite in this example)
engine = create_engine('sqlite:///example.db')

# Create the users table
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Insert entries from the CSV file into the database
users = [
    DynamicUser(**{col: row[col] for col in df.columns}) for index, row in df.iterrows()
]

# Add all users to the session in one go
session.add_all(users)

# Commit the transaction to the database
session.commit()

# Query to verify the insertion
users = session.query(DynamicUser).all()
for user in users:
    print(user)
