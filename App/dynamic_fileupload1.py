import pandas as pd # type: ignore
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the base class
Base = declarative_base()

# Define the DynamicModel class with 50 columns
class DynamicModel(Base):
    __tablename__ = 'dynamic_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    col_1 = Column(String)
    col_2 = Column(String)
    col_3 = Column(String)
    col_4 = Column(String)
    col_5 = Column(String)
    col_6 = Column(String)
    col_7 = Column(String)
    col_8 = Column(String)
    col_9 = Column(String)
    col_10 = Column(String)
    col_11 = Column(String)
    col_12 = Column(String)
    col_13 = Column(String)
    col_14 = Column(String)
    col_15 = Column(String)
    col_16 = Column(String)
    col_17 = Column(String)
    col_18 = Column(String)
    col_19 = Column(String)
    col_20 = Column(String)
    col_21 = Column(String)
    col_22 = Column(String)
    col_23 = Column(String)
    col_24 = Column(String)
    col_25 = Column(String)
    col_26 = Column(String)
    col_27 = Column(String)
    col_28 = Column(String)
    col_29 = Column(String)
    col_30 = Column(String)
    col_31 = Column(String)
    col_32 = Column(String)
    col_33 = Column(String)
    col_34 = Column(String)
    col_35 = Column(String)
    col_36 = Column(String)
    col_37 = Column(String)
    col_38 = Column(String)
    col_39 = Column(String)
    col_40 = Column(String)
    col_41 = Column(String)
    col_42 = Column(String)
    col_43 = Column(String)
    col_44 = Column(String)
    col_45 = Column(String)
    col_46 = Column(String)
    col_47 = Column(String)
    col_48 = Column(String)
    col_49 = Column(String)
    col_50 = Column(String)

    def __repr__(self):
        return f"<DynamicModel(id={self.id}, col_1={self.col_1}, ..., col_50={self.col_50})>"

# Create an engine and connect to the database (SQLite in this example)
engine = create_engine('sqlite:///example.db')

# Create the table based on the dynamic model
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)
session = Session()

# Read the CSV file
csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# Ensure that the DataFrame column names match the model's column names
if set(df.columns) != set([f"col_{i}" for i in range(1, 51)]):
    raise ValueError("CSV columns do not match the model's columns")

# Insert entries from the CSV file into the database
entries = [
    DynamicModel(**{col: row[col] for col in df.columns}) for index, row in df.iterrows()
]

# Add all entries to the session in one go
session.add_all(entries)

# Commit the transaction to the database
session.commit()

# Query to verify the insertion
results = session.query(DynamicModel).all()
for result in results:
    print(result)



# This list comprehension iterates over each row in the DataFrame (df.iterrows()) and creates an instance of DynamicModel for each row.

# The **{col: row[col] for col in df.columns} part constructs a dictionary for each row, where keys are column names and values are the corresponding values in the row.

# The DynamicModel(**{col: row[col] for col in df.columns}) creates a DynamicModel instance by unpacking this dictionary.