import grpc
import similarity_pb2
import similarity_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)

        print("1. Add item")
        print("2. Searching items")
        print("3. Retrieving the search results")
        rpc_call = input("Which RPC would you like to make: ")


        if rpc_call == "1":
            # Create an AddItemRequest
            description = input("Please enter description: ")
            add_item_request = similarity_pb2.AddItemRequest(description = description)

            # Call the AddItem RPC
            add_item_response = stub.AddItem(add_item_request)

            print('AddItem response:')
            print(add_item_response.message)


        elif rpc_call == "2":
            # Create a SearchItemsRequest
            search_items_request = similarity_pb2.SearchItemsRequest()
            search_items_request.query = input("Please enter search query: ")

            # Call the SearchItems RPC
            search_items_response = stub.SearchItems(search_items_request)
            print('SearchItems response:')
            for result in search_items_response.results:
                print('ID:', result.id)
                print('Description:', result.description)

        else:
            print("Invalid RPC option")

if __name__ == '__main__':
    run()





#import grpc
#import similarity_pb2
#import similarity_pb2_grpc
#import time
#
#
#
#
#def run_client():
#    with grpc.insecure_channel('localhost:50051') as channel:
#        stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)
#
#        print("1. Add item")
#        print("2. Searching items")
#        print("3. Retrieving the search results")
#        rpc_call = input("Which RPC would you like to make: ")
#        if rpc_call == "1":
#            # AddItem example
#            add_item_request = similarity_pb2.AddItemRequest()
#            add_item_request.description = input("Please enter description: ")
#
#            add_item_response = stub.AddItem(add_item_request)
#
#            print("AddItem response:", add_item_response.message)
##      if rpc_call == "2":
##          # SearchItems example
##          search_items_request = similarity_pb2.SearchItemsRequest()
##          search_items_request.query = "search query"
##          search_items_responses = stub.SearchItems(search_items_request)
##          for search_items_response in search_items_responses:
##              print("SearchItems response:", search_items_response.search_id)
##      if rpc_call == "3":
##          # GetSearchResults example
##          get_search_results_request = similarity_pb2.GetSearchResultsRequest()
##          get_search_results_request.search_id = input("Please enter a value (or nothing to stop chatting): ")
##          get_search_results_response = stub.GetSearchResults(get_search_results_request)
##          for result in get_search_results_response.results:
##              print("Search result:", result.id, result.description)
#
#
#if __name__ == "__main__":
#    run_client()
#