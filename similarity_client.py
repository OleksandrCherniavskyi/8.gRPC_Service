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
            print("3. Retrieving the search results")
            rpc_call = input("Which RPC would you like to make: ")

            if rpc_call == "":
                break
            elif rpc_call == "1":
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
                print(search_items_response.search_id)


            elif rpc_call == "3":
                # Create a GetSearchResultsRequest
                get_search_results_request = similarity_pb2.GetSearchResultsRequest()
                get_search_results_request.search_id = input("Please enter search ID: ")

                # Call the GetSearchResults RPC
                get_search_results_response = stub.GetSearchResults(get_search_results_request)
                print('GetSearchResults response:')
                #print(get_search_results_response.SearchResult)
                for search_result in get_search_results_response.results:
                    print('Description:', search_result.description)



            responses = stub.GetSearchResults(run())


            for response in responses:
                print("InteractingHello Response Received: ")
                print(response)



if __name__ == '__main__':
    run()



