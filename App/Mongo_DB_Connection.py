from pymongo import MongoClient
try:
   # conn_mongo=pymongo..connect(host='localhost',database='testsatheesh',user='',password='',cursor_factory=RealDictCursor)
    #cursor=conn_mongo.cursor()
    uri="mongodb://localhost:27017/"
    client=MongoClient(uri)
    database=client.get_database("testsatheesh")
    table=database.get_collection("test1")
    query={"Name":"Satheesh1"}
    test = table.find_one(query)
    print(test)
    client.close()
    print("Mongo Database connection was successful")
    #break
except Exception as error:
    print("Connection to databse dailed")
    print("Error:",error)
    #time.sleep(10) 
    #break