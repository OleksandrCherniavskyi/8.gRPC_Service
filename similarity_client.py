import grpc
import similarity_pb2
import similarity_pb2_grpc
import time



def run():
    while True:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = similarity_pb2_grpc.SimilaritySearchServiceStub(channel)

            print("1. Add item")
            print("2. Searching items")
            print("3. Retrieving the search results\n")
            rpc_call = input("Which RPC would you like to make(or nothing to stop chatting): ")

            if rpc_call == "":
                break
            elif rpc_call == "1":
                # Create an AddItemRequest
                description = input("\nPlease enter description: \n")
                add_item_request = similarity_pb2.AddItemRequest(description = description)

                # Call the AddItem RPC
                add_item_response = stub.AddItem(add_item_request)

                print(add_item_response.message)
                print(f'Status: {add_item_response.status}\n')



            elif rpc_call == "2":
                # Create a SearchItemsRequest
                search_items_request = similarity_pb2.SearchItemsRequest()
                search_items_request.query = input("\nPlease enter search query: \n")

                # Call the SearchItems RPC
                search_items_response = stub.SearchItems(search_items_request)


                print(f'\nSearchItems response: {search_items_response.search_id}\n')



            elif rpc_call == "3":
                # Create a GetSearchResultsRequest
                get_search_results_request = similarity_pb2.GetSearchResultsRequest()
                get_search_results_request.search_id = input("\nPlease enter search ID: \n")

                # Call the GetSearchResults RPC
                get_search_results_response = stub.GetSearchResults(get_search_results_request)

                for result in get_search_results_response.results:
                    print(f"\nSearch Result ID: {result.id}, Description: {result.description}\n")









if __name__ == '__main__':
    run()



