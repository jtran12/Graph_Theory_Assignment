import sys
from TwitInMyFace import SocialNetwork

def initialize_graph() -> 'SocialNetwork':
    '''Return a SocialNetwork that is loaded from a file. The name of the file
    to be loaded is provided at the command line or defaults to 'example.timf'
    '''

    # Choose a file name
    graph_filename = (sys.argv[1:] + ['example.timf'])[0]
    
    # Build and return a graph
    graph = SocialNetwork()
    graph.load_from_file(open(graph_filename))
    return graph
    

def process_input(query: 'list of str', graph: 'SocialNetwork') -> bool:
    '''Handle query commands (friends, degree, etc.) against graph and
    return True iff the 'quit' command is given.
    '''
    
    if len(query) == 2 and query[0] == 'friends':
        print(graph.friends(query[1]))

    elif len(query) == 3 and query[0] == 'degree':
        print(graph.degree_between(query[1], query[2]))

    elif len(query) == 3 and query[0] == 'degrees':
        print(graph.people_with_degree(query[1], query[2]))

    elif len(query) == 3 and query[0] == 'mutual':
        print(graph.mutual_friends(query[1], query[2]))

    elif len(query) == 2 and query[0] == 'likely':
        print(graph.likely_friends(query[1]))

    elif len(query) == 3 and query[0] == 'classmates':
        print(graph.classmates(query[1], query[2]))
                
    elif query == ['quit']:
        return False
        
    else:
        print('Invalid command or wrong number of arguments provided.')
        
    return True

def main():
    '''The main TwitInMyFace program.'''
    
    graph = initialize_graph()

    while process_input(input('>>> ').split(), graph):
        pass            
    
    
if __name__ == '__main__':
    main()
    