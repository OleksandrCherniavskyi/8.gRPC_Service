import grpc
import similarity_pb2
import similarity_pb2_grpc
import sqlite3
import threading
from concurrent import futures

class SimilaritySearchService(similarity_pb2_grpc.SimilaritySearchServiceServicer):
    def __init__(self):
        self.connection_pool = threading.local()

    def get_connection(self):
        if not hasattr(self.connection_pool, 'connection'):
            self.connection_pool.connection = sqlite3.connect('similarity.sqlite3')
        return self.connection_pool.connection

    def AddItem(self, request, context):
        print('AddItem:')
        print(request)

        connection = self.get_connection()
        cursor = connection.cursor()
        #item_id = request.id
        description = request.description

        try:

            # Create the "items" table if it doesn't exist
            create_db_query = '''CREATE TABLE IF NOT EXISTS items (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   description VARCHAR)'''
            cursor.execute(create_db_query)
            connection.commit()

            insert_query = "INSERT INTO items (description) VALUES (?)"
            cursor.execute(insert_query, (request.description,))
            connection.commit()

            add_item_response = similarity_pb2.AddItemResponse()
            add_item_response.status = 200
            add_item_response.message = 'Item added successfully'
            #print('Response:', response)


            return add_item_response
        except sqlite3.Error as e:
            error_response = similarity_pb2.AddItemResponse()
            error_response.status = 500
            error_response.message = 'Error adding item to the database: {}'.format(str(e))

            return error_response

    def SearchItems(self, request, context):
        connection = self.get_connection()
        cursor = connection.cursor()
        query = request.query

        try:
            # Execute the search query
            search_query = "SELECT id, description FROM items WHERE description LIKE ?"
            cursor.execute(search_query, ('%' + query + '%',))
            search_results = cursor.fetchall()

            # Create the SearchItemsResponse message
            response = similarity_pb2.SearchItemsResponse()
            for result in search_results:
                search_result = response.results.add()
                search_result.id = result[0]
                search_result.description = result[1]

            return response
        except sqlite3.Error as e:
            error_response = similarity_pb2.SearchItemsResponse()
            # Set the error status and message
            error_response.status = 500
            error_response.message = 'Error searching items in the database: {}'.format(str(e))

            return error_response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    similarity_pb2_grpc.add_SimilaritySearchServiceServicer_to_server(SimilaritySearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started, listening on 50051 ")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


#import sqlite3
#from concurrent import futures
#import grpc
#from sqlalchemy import create_engine, Column, String, Integer
#import similarity_pb2
#import similarity_pb2_grpc
#import psycopg2
#import time
#
#
#engine = create_engine('sqlite:///similarity.sqlite3', echo=True)
#
#class SimilaritySearchServicer(similarity_pb2_grpc.SimilaritySearchServiceServicer):
#    def __init__(self):
#        self.conn = sqlite3.connect('similarity.sqlite3')
#        self.cursor = self.conn.cursor()
#
#        # Create the "items" table if it doesn't exist
#        self.create_db_query = '''CREATE TABLE IF NOT EXISTS items (
#                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                    description VARCHAR)'''
#        self.cursor.execute(self.create_db_query)
#        self.conn.commit()
#
#    def AddItem(self, request, context):
#        response = similarity_pb2.AddItemResponse()
#
#        # Insert the item into the "items" table
#        insert_query = "INSERT INTO items (description) VALUES (?)"
#        self.cursor.execute(insert_query, (request.description,))
#        self.conn.commit()
#
#        response.status = 200
#        response.message = "Item added successfully"
#
#        return response
#
##    def SearchItems(self, request, context):
##        response = similarity_pb2.SearchItemsResponse()
##        # Implement the logic to search items
##        for i in range(3):
##
##            response.search_id = f"12345{i + 1}"
##            yield response
##            time.sleep(1)
##
##
##    def GetSearchResults(self, request, context):
##        response = similarity_pb2.GetSearchResultsResponse()
##        # Implement the logic to get search results
##        result1 = response.results.add()
##        result1.id = "1"
##        result1.description = "Sample result 1"
##        result2 = response.results.add()
##        result2.id = "2"
##        result2.description = "Sample result 2"
##        return response
#
#def run_server():
#    port = "50051"
#    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#    similarity_pb2_grpc.add_SimilaritySearchServiceServicer_to_server(SimilaritySearchServicer(), server)
#    server.add_insecure_port("[::]:" + port)
#    server.start()
#    print("Server started, listening on " + port)
#    server.wait_for_termination()
#
#if __name__ == "__main__":
#    run_server()
#