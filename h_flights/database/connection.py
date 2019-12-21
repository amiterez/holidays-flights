from pymongo import MongoClient

class DBConnection():
    client_instace = None

    def get_single_document(self, database_name, collection_name):
        database = self.client_instace.get_database(database_name)

        collection = database[collection_name]

        return collection.find_one()

    def get_Collection(self, database_name, collection_name, filter_query={}):
        if not self.client_instace:
            return

        database = self.client_instace.get_database(database_name)

        collection = database[collection_name]

        for document in collection.find(filter_query):
            yield document

    def connect_to_db(self, connction_str):
        try:
            if not self.client_instace:
                self.client_instace = MongoClient(connction_str)

            connection_succeeded = True
        except:
            connection_succeeded = False


        return connection_succeeded


