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
            add_item_response.message = f'Item added successfully {request.description}'



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
        print('SearchItems:')

        try:
            # Execute the search query
            search_query = "SELECT id, description FROM items WHERE description LIKE ?"
            cursor.execute(search_query, ('%' + query + '%',))
            search_results = cursor.fetchall()

            # Create the SearchItemsResponse message
            search_items_response = similarity_pb2.SearchItemsResponse()

            rows = []
            for row in search_results:

                item_id = row[0]

                rows.append(item_id)



            search_items_response.search_id = f'ID: {rows}'


            return search_items_response
        except sqlite3.Error as e:
            error_response = similarity_pb2.SearchItemsResponse()
            # Set the error status and message
            error_response.status = 500
            error_response.message = 'Error searching items in the database: {}'.format(str(e))

            return error_response

    def GetSearchResults(self, request, context):
        connection = self.get_connection()
        cursor = connection.cursor()
        search_id = request.search_id
        print('GetSearchResults:')
        print(search_id)

        try:
            # Execute the search query
            search_query = "SELECT id, description FROM items WHERE id = ?"
            cursor.execute(search_query, (search_id,))

            search_results = cursor.fetchall()

            # Create the GetSearchResultsResponse message
            get_search_results_response = similarity_pb2.GetSearchResultsResponse()

            for search_result in get_search_results_response.results:
                print('Description:', search_result.description)
                get_search_results_response.SearchResult = f'Description: {search_result.description}'



            return get_search_results_response
        except sqlite3.Error as e:
            error_response = similarity_pb2.GetSearchResultsResponse()
            error_response.status = 500
            error_response.message = 'Error retrieving search results from the database: {}'.format(str(e))

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