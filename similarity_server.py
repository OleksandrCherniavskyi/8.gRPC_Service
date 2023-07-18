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


        connection = self.get_connection()
        cursor = connection.cursor()

        description = request.description
        print(f'AddItem:{description}')

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
            add_item_response.message = f'\nItem added successfully: {request.description}'



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


    def GetSearchResults(self, request, context):
        connection = self.get_connection()
        cursor = connection.cursor()
        search_id = request.search_id
        print(f'GetSearchResults, ID: {search_id}')


        # Execute the search query
        search_query = "SELECT id, description FROM items WHERE id = ?"
        cursor.execute(search_query, (search_id,))
        search_results = cursor.fetchall()

        # Convert search results to gRPC message format
        get_search_results_response = similarity_pb2.GetSearchResultsResponse()
        for result in search_results:
            search_result = get_search_results_response.results.add()
            search_result.id = str(result[0])
            search_result.description = result[1]

        return get_search_results_response




def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor())
    similarity_pb2_grpc.add_SimilaritySearchServiceServicer_to_server(SimilaritySearchService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

