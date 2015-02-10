"""
      TwitInMyFace
      
Authors:
    Jason Tran
    Steven Tan
"""

import unittest
import io
import random


######################### Helper Functions ####################################
def nodes_names(lst: list) -> list:
    '''Convert a list of nodes to a list of names of friends. Return the list
    of name of friends.'''
    
    result = []
    for node in lst:
        result.append(node.get_name())
    return result


def nodes_emails(lst: list) -> list:
    '''Convert a list of nodes to a list of emails associated with each
    node. Return the list of emails'''
    
    result = []
    for node in lst:
        result.append(node.get_email())
    return result


def list_to_string(lst: list) -> str:
    """ 
    Sorts the list and the converts the sorted list of strings into a 
    single string. Return the string.
    """
    
    lst.sort()
    output = ' '.join(lst)
    return output    


def construct_network(file: 'file to be read') -> 'SocialNetwork':
    """
    Returns a SocialNetwork object given a file.
    """
    network = SocialNetwork()
    network.load_from_file(file)
    return network
    
    
######################### Exception Class #####################################
class EmptyFileError(Exception):
    pass


######################### Node Class ##########################################
class Node(object):
    '''Node object that contains a person's name, email, school and friends.'''
    def __init__(self, name: str, email: str, schools: str=None, 
                 friends: str=None):
        '''Initializes the Node object containing a person's name, 
        email, school(s) and friend(s) where school(s) and friend(s)
        can be None'''
        
        self._name = name                  
        self._email = email 
        self._schools = []
        if schools:
            for school in schools.split(','):
                self._schools.append(school)       
        self._friends = []
        if friends:
            for friend in friends.split(','):
                self._friends.append(friend)
    
    def get_email(self) -> str:
        return self._email
    
    def get_name(self) -> str:
        return self._name
    
    def get_friends(self) -> list:
        return self._friends
    
    def get_schools(self) -> list:
        return self._schools


######################### SocialNetwork Class #################################
class SocialNetwork(object):
    def __init__(self):
        '''Initializes the SocialNetwork class which contains a map of graph
        of nodes in the form of a dictionary {nodes: list of nodes}
        self._network, a list of emails self._emails and a list of nodes that 
        corresponds to the list self._emails.'''
        self._network = {}
        self._emails = []
        self._nodes = []
        
    ############################# Helper Methods #############################
    def convert_to_lists(self, file: 'file to be read') -> None:
        '''Modify self._emails so that it contains all the emails from the 
        file and modify self._nodes into a list of nodes that are associated
        with each email. No duplicates may exist in both lists.'''
        
        if isinstance(file, str):
            opened_file = open(file, 'r')
        else:
            opened_file = file
        for line in opened_file:
            if not line.strip():
                continue
            line = line.strip()
            # The first element of two_elements list is the name of person.
            two_elements = line.split('<')
            name = two_elements[0]
            # First element of two_sub_elements list is person's email
            # and the second element is person's friends as a string.
            two_sub_elements = two_elements[1].split('>(')
            email = two_sub_elements[0]
            rest = two_sub_elements[1].split('):')
            schools = rest[0]
            friends = rest[1]
            self._emails.append(email)
            self._nodes.append(Node(name, email, schools, friends))
    
    def email_index(self: 'SocialNetwork', email: str) -> int:
        '''Return the index of the email in the list self._emails'''
        
        return self._emails.index(email)
    
    def get_node(self: 'SocialNetwork', idx: int) -> 'Node':
        '''Return the node in self._nodes at given index idx.'''
        
        return self._nodes[idx]
    
    def email_to_name(self: 'SocialNetwork', lst: list) -> list:
        """
        Return a list of the names of people which corresponds to 
        the list of given emails.
        """
        
        result = []
        for email in lst:
            idx = self.email_index(email)
            result.append(self._nodes[idx].get_name())
        return result

    def find_node_by_email(self: 'SocialNetwork', email: str) -> 'Node':
        """
        Return the node associated with the email address email.
        """
        found_idx = self.email_index(email)
        return self.get_node(found_idx)    
    
    def emails_to_node(self: 'SocialNetwork', lst: list) -> list:
        '''Convert a list of emails lst to a list of nodes associated with each
        email. Return the list.'''
        
        result = []
        for email in lst:
            node = self.find_node_by_email(email)
            result.append(node)
        return result
    
    def read_from_file(self: 'SocialNetwork', file: 'file to be read') -> None:
        """ Reads the file given and constructs a dictionary of everyone
        If one person lists someone as their friend, but not the other way
        around, we'll make them both considered friends with each other.
        """
        
        self.convert_to_lists(file)
        if len(self._emails) == 0:
            raise EmptyFileError()         
        # Construct the dictionary of everyone.
        # Node of person: node of person's friends
        for node in self._nodes:
            list_friends = node.get_friends()
            friends_nodes = []
            for email in list_friends:
                idx = self.email_index(email)
                friends_nodes.append(self._nodes[idx])
            for person in self._network:
                i = self.email_index(person.get_email())
                item = self._nodes[i]
                if (node in self._network[person]) and (item not in 
                                                        friends_nodes):
                    friends_nodes.append(item)
            self._network[node] = friends_nodes
    
    def people_with_degree_list(self, x: str, d: int) -> list:
        """
        Returns a list of emails that corresponds to every person within 
        'd' degrees from person x.
        """
        list_of_people_with_seperation = []
        
        for i in range(len(self._emails)):
            depth = self.degree_between(x, self._emails[i])
            if depth == int(d):
                list_of_people_with_seperation.append(self._emails[i])
        
        return list_of_people_with_seperation   
        
    def mutual_friends_list(self, x: str, y: str) -> list:
        """
        Returns a list of names of people who are mutual friends with person
        x and person y.
        """
        
        node1 = self.find_node_by_email(x)
        node2 = self.find_node_by_email(y)
        lst_1 = node1.get_friends()
        lst_2 = node2.get_friends()
        lst_1_friends = self.email_to_name(lst_1)
        lst_2_friends = self.email_to_name(lst_2)
        set_1 = set(lst_1_friends)
        set_2 = set(lst_2_friends)
        # Find the emails that appear in both set_1 and set_2.
        intersect = set.intersection(set_1, set_2)
        result_lst = list(intersect)
        result_lst.sort()  
        return result_lst    
    
    def get_people_within_degrees(self: 'SocialNetwork', x: str, 
                                  d: int) -> list:
        """
        Returns a list of emails within a degree of separation of 'd' 
        from person x.
        """
        if int(d) <= 0:
            return []
        lst = self.people_with_degree_list(x, int(d))
        for i in range(1, int(d)):
            lst.extend(self.people_with_degree_list(x, int(d) - i))
        return lst
    
    ############################## Main Methods ##############################
    def load_from_file(self: 'SocialNetwork', file: 'file to be read') -> None:
        """
        Retrieves data from file and puts the data in 
        self._network in the form of a dictionary. The dictionary format will
        be {node: list of nodes} where each key of the dictionary is the node
        of each person in the file and the value associated with each key is
        the list of nodes that correspond to the person's friends.
        """
        
        # Handles the exception where the file is empty.
        try:
            self.read_from_file(file)
        except EmptyFileError:
            print('The File Is Empty')
        # Ensure each friendship made is mutual, i.e A purports B is a friend,
        # then A will automatically be listed as B's friend.
        for key in self._network:
            for item in self._network:
                if item != key:
                    if (key in self._network[item]) and (item not in 
                                                         self._network[key]):
                        self._network[key].append(item)
        # Update the attribute _friends for each node in the dictionary, 
        # if there is one.       
        for key in self._network:
            if (self._network[key] == key.get_friends()):
                pass
            else:
                key._friends[:] = self._network[key]
                # Do the same for the nodes in the list self._nodes
                email = key.get_email()
                idx = self.email_index(email)
                lst = nodes_emails(self._network[key])
                self._nodes[idx]._friends[:] = lst
                
    def friends(self: 'SocialNetwork', email: str) -> str:
        """
        Return a string that contains the names of every friend of the
        person that has the email email.
        """
        
        idx = self.email_index(email)
        lst_nodes = self._network[self._nodes[idx]]
        lst_friends = nodes_names(lst_nodes)
        output = list_to_string(lst_friends)
        return output

    def degree_between(self: "SocialNetwork", x: str, y: str) -> int:
        """
        Return the degree of separation between person x and person y 
        (where people are specified by their e-mail address). 
        In the network graph, the degree of separation between x and y 
        corresponds to the number of edges on the shortest path between x 
        and y. Return inf if no path is found between x and y.
        """
        
        count = 0
        # lst used to keep track of emails already looked at
        lst = []
        to_pass_through = []
        # temp_list stores all the friends of nth iteration email 
        # to be used for later
        temp_list = []
        # hold_values takes temp's contents and puts back into to_pass_through
        hold_values = []
        if y == x:
            return count
        # start off we use the initial email, which is [[email_of_x]]
        to_pass_through.append([x])
        while to_pass_through != [[]]:
            temp_list[:] = []
            emails = to_pass_through.pop(0) 
            for email in emails:
                # Do not traverse through these nodes
                lst.append(email)
            for email in emails:
                cur_node = self.find_node_by_email(email)
                friends = cur_node.get_friends()
                if cur_node.get_email() == y:
                    return count
                for friend in friends:
                    if friend not in lst:
                        temp_list.append(friend)
            # replace hold_values with the contents of temp list
            hold_values[:] = temp_list
            # to_pass_through is [['email1'...]] or [[]] if we checked
            # all friends possible already
            to_pass_through[:] = [hold_values] 
            count = count + 1
        return float('inf')
           
    def people_with_degree(self, x: str, d: int) -> str:
        """
        Return a string that contains the names of every person separated from 
        person x by exactly d degrees of separation(where x is an 
        e-mail address). The names will be sorted in an alphabetical order. 
        """
        
        lst_email = self.people_with_degree_list(x, int(d))
        lst_people = self.email_to_name(lst_email)
        output = list_to_string(lst_people)
        return output
        
    def mutual_friends(self, x: str, y: str) -> str:
        """
        Return a string that contains the names of people who are friends with 
        person x and person y where both parameters are the emails to both
        persons respectively. The names are sorted in alphabetical order. 
        """
        
        lst = self.mutual_friends_list(x, y)
        output = list_to_string(lst)
        return output
    
    def likely_friends(self, person: str) -> str:
        """
        Return a string that contains the names of missing friends for a
        person by listing the likeliest missing friends where 
        x is the person's email address. 
        """
        
        # Max mutual will start as 1 because if it's 0, then it will assume
        # that since x has zero mutual friends with y, we'll say that y is a
        # likely candidate, even though x probably doesn't know y. By putting
        # max_mutual = 1, we ensure that you have to at least have 1 friend in
        # common.
        max_mutual = 1
        missing_friends = []
        visited = []
        visited.append(person)
        node = self.find_node_by_email(person)
        for friend in node.get_friends():
            visited.append(friend)
        for i in range(len(self._emails)):
            # Search through every email that's avaliable in the graph
            if self._emails[i] in visited:
                continue
            # list of people who have mutual friends with current person
            lst_mutual = self.mutual_friends_list(person, self._emails[i])
            num_mutual = len(lst_mutual)
            # If the amount of mutual friends this person has with the other
            # Exceeds the current friend that has a lot of mutual friends
            # with the person, then we will replace the existing max with the
            # new candidate, if they're equal we'll add those two people.
            if num_mutual > max_mutual:
                max_mutual = num_mutual
                email = self._emails[i]
                missing_friends[:] = [email]
            elif num_mutual == max_mutual:
                missing_friends.append(self._emails[i])
        result_lst = self.email_to_name(missing_friends)
        result = list_to_string(result_lst)
        return result
        
    def classmates(self: 'SocialNetwork', x: str, d: int) -> str:
        """
        Return a string that contains the names of every person within 
        d degrees of separation of a person x who went to the 
        same school as the person x and x is an email address of the person. 
        """
        
        classmates = []
        x_node = self.find_node_by_email(x)
        lst_emails = self.get_people_within_degrees(x, int(d))
        lst_nodes = self.emails_to_node(lst_emails)
        # Check every node in lst_nodes to see if any person went
        # to the same school as person x.
        for node in lst_nodes:
            for school in node.get_schools():
                # If the person is not already in the list classmates and 
                # go to the same schooll as x, then append the person to
                # classmates.
                if school in x_node.get_schools() and \
                   node.get_name() not in classmates:
                    classmates.append(node.get_name())
        result = list_to_string(classmates)
        return result
    

########################### Unittest Test Cases ###############################
class TestDegree(unittest.TestCase):
        
    def test_one_person_no_friend(self: 'TestDegree') -> None:
        """
        One person in the graph. Test to see if the degree between the start
        and itself, is zero(0).
        """
        file = io.StringIO('person 1<one@toronto.ca>(Uni of Toronto): \n')
        network = construct_network(file)
        input_val = network.degree_between('one@toronto.ca', 'one@toronto.ca')
        expected_output = 0
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
    
    def test_two_people_all_friends(self: 'TestDegree') -> None:
        """
        Two Nodes in the graph, both friends with each other. Test to see if
        the degree between the two is 1.
        """
        file = io.StringIO('A Kirby<kirby@toronto.ca>(Uni of Toronto):'
                           'metaknight@toronto.ca\n'
                         
                           'M Knight<metaknight@toronto.ca>(Uni of Toronto):'
                           'kirby@toronto.ca\n')
        network = construct_network(file)
        input_val = network.degree_between('kirby@toronto.ca',
                                           'metaknight@toronto.ca')
        expected_output = 1
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
        
    def test_triangle_shaped_graph(self: 'TestDegree') -> None:
        """
        A graph with 3 nodes are generated. Every node in the graph is
        connected to each other.
        """
        file = io.StringIO('Kyon<kyon@toronto.ca>(Uni of Toronto):'
                           'Haruhi@toronto.ca\n'
                   
                        'Suzumiya Haruhi<Haruhi@toronto.ca>(Uni of Toronto):'
                        'YukiN@toronto.ca\n'
                        
                        'Nagato Yuki<YukiN@toronto.ca>(Uni of Toronto):'
                        'kyon@toronto.ca\n')
        network = construct_network(file)
        input_val = network.degree_between('kyon@toronto.ca',
                                           'Haruhi@toronto.ca')
        expected_output = 1
        self.assertEqual(input_val, expected_output, 'Wrong degree between')        
    
    def test_two_people_no_path(self: 'TestDegree') -> None:
        """
        Two Nodes in the graph, testing degree_between one node and other,
        with no path in between the nodes. Test to see if it returns inf
        """
        file = io.StringIO('A Kirby<kirby@toronto.ca>(Uni of Toronto): \n'
                        'M Knight<metaknight@toronto.ca>(Uni of Toronto): \n')
        network = construct_network(file)
        input_val = network.degree_between('kirby@toronto.ca',
                                           'metaknight@toronto.ca')
        expected_output = float('inf')
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
    
    def test_one_friend_multiple_path_length(self: 'TestDegree') -> None:
        """
        Six Nodes in the graph.
        Tests to see that degree of one node to another takes the shortest
        path. First node only has one path then branches off 
        converging to target.
        """
        file = io.StringIO('C Falcon<showmeyamoves@toronto.ca>'
                           '(Uni of Toronto):'
                           'FZero@toronto.ca\n'
                   
                           'F Zero<FZero@toronto.ca>(Uni of Toronto):'
                           'kirby@toronto.ca,finn@toronto.ca\n'
                   
                           'A Kirby<kirby@toronto.ca>(Uni of Toronto):'
                           'FZero@toronto.ca,king@princess.ca\n'
                   
                           'Finn<finn@toronto.ca>(Uni of Toronto):'
                           'iceking@princess.ca\n'
                   
                           'Simon<iceking@princess.ca>(Uni of Toronto):'
                           'king@princess.ca,finn@toronto.ca\n'
                           
                           'king<king@princess.ca>(Uni of Toronto): \n')
        network = construct_network(file)
        input_val = network.degree_between('showmeyamoves@toronto.ca',
                                           'king@princess.ca')
        expected_output = 3
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
    
    def test_one_path_one_friend(self: 'TestDegree') -> None:
        """
        Seven Nodes in the graph. Everyone has at most 1 friend.
        Tests to see if it follows the path given.
        looks like: X-o-o-o-o-Y-o
        Where x is the start and y is the end
        """
        file = io.StringIO('C Falcon<showmeyamoves@toronto.ca>'
                           '(Uni of Toronto):'
                           'FZero@toronto.ca\n'
                   
                           'F Zero<FZero@toronto.ca>(Uni of Toronto):'
                           'kirby@toronto.ca\n'
                   
                           'A Kirby<kirby@toronto.ca>(Uni of Toronto):'
                           'cooguy@toronto.ca\n'
                   
                           'Coo Guy<cooguy@toronto.ca>(Uni of Toronto):'
                           'iceking@princess.ca\n'
                   
                           'Simon<iceking@princess.ca>(Uni of Toronto):'
                           'king@princess.ca\n'
                           
                           'king<king@princess.ca>(Uni of Toronto):'
                           'meepo@geomancer.ca\n'
                           
                           'Meepo<meepo@geomancer.ca>(Uni of Toronto): \n')
        network = construct_network(file)
        input_val = network.degree_between('showmeyamoves@toronto.ca',
                                           'king@princess.ca')
        expected_output = 5
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
    
    def test_multiple_friends_multiple_path_length(self: 'TestDegree') -> None:
        """
        10 nodes in graph. Every person has more than 3 friends
        Tests to see if degree between X and Y returns the shortest one.
        """
        file = io.StringIO('C Falcon<showmeyamoves@toronto.ca>'
                           '(Uni of Toronto):'
                           'FZero@toronto.ca,kirby@toronto.ca,'
                           'cooguy@toronto.ca\n'
                   
                           'F Zero<FZero@toronto.ca>(Uni of Toronto):'
                           'kirby@toronto.ca,showmeyamoves@toronto.ca,'
                           'meepo@geomancer.ca\n'
                   
                           'A Kirby<kirby@toronto.ca>(Uni of Toronto):'
                           'cooguy@toronto.ca,iceking@princess.ca,'
                           'king@princess.ca,meepo@geomancer.ca,'
                           'showmeyamoves@toronto.ca,FZero@toronto.ca\n'
                   
                           'Coo Guy<cooguy@toronto.ca>(Uni of Toronto):'
                           'iceking@princess.ca,axe@axed.ca\n'
                   
                           'Simon<iceking@princess.ca>(Uni of Toronto):'
                           'king@princess.ca,axe@axed.ca,'
                           'cooguy@toronto.ca,dk@dragon.ca\n'
                           
                           'king<king@princess.ca>(Uni of Toronto):'
                           'meepo@geomancer.ca,dk@dragon.ca,'
                           'kirby@toronto.ca,iceking@princess.ca\n'
                           
                           'Meepo<meepo@geomancer.ca>(Uni of Toronto):'
                           'dk@dragon.ca,king@princess.ca,kirby@toronto.ca,'
                           'FZero@toronto.ca\n'
                           
                           'axe<axe@axed.ca>(Uni of Toronto):'
                           'cooguy@toronto.ca,alistar@moo.ca,'
                           'iceking@princess.ca\n'
                           
                           'alistar<alistar@moo.ca>(Uni of Toronto):'
                           'dk@dragon.ca,axe@axed.ca,iceking@princess.ca\n'
                           
                           'Knight Davian<dk@dragon.ca>(Uni of Toronto):'
                           'alistar@moo.ca,meepo@geomancer.ca,'
                           'king@princess.ca,iceking@princess.ca\n')
        network = construct_network(file)
        input_val = network.degree_between('showmeyamoves@toronto.ca',
                                           'king@princess.ca')
        expected_output = 2
        self.assertEqual(input_val, expected_output, 'Wrong degree between')

    def test_a_lot_people_no_friends(self: 'TestDegree') -> None:
        """
        10 nodes in graph. No one is friends with one another
        target is not itself. Test to see if degree_between returns 
        infinity with a large set.
        """
        file = io.StringIO('C Falcon<showmeyamoves@toronto.ca>'
                           '(Uni of Toronto): \n'
                   
                           'F Zero<FZero@toronto.ca>(Uni of Toronto): \n'
                   
                           'A Kirby<kirby@toronto.ca>(Uni of Toronto): \n'
                   
                           'Coo Guy<cooguy@toronto.ca>(Uni of Toronto): \n'
                   
                           'Simon<iceking@princess.ca>(Uni of Toronto): \n'
                           
                           'king<king@princess.ca>(Uni of Toronto): \n'
                           
                           'Meepo<meepo@geomancer.ca>(Uni of Toronto): \n'
                           
                           'axe<axe@axed.ca>(Uni of Toronto): \n'
                           
                           'alistar<alistar@moo.ca>(Uni of Toronto): \n'
                           
                           'Knight Davian<dk@dragon.ca>(Uni of Toronto): \n')
        network = construct_network(file)
        input_val = network.degree_between('showmeyamoves@toronto.ca',
                                           'king@princess.ca')
        expected_output = float('inf')
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
        
    def test_multiple_friends_same_path_length(self: 'TestDegree') -> None:
        """
        A graph with 6 nodes are created. Then 2 specific nodes will be
        selected such that every path between these 2 nodes will yield
        the same number of edges.
        """
        
        file = io.StringIO('A Dylan<a@dra.net>(Uni of Toronto):c@dra.net,'
                           'b@dra.net\nB Ba<b@dra.net>():e@dra.net\n'
                           'E Ea<e@dra.net>():z@dra.net\nZ Za<z@dra.net>'
                           '():d@dra.net\nD Da<d@dra.net>():c@dra.net\n'
                           'C Ca<c@dra.net>():')
        network = construct_network(file)
        input_val = network.degree_between('a@dra.net', 'z@dra.net')
        expected_output = 3
        self.assertEqual(input_val, expected_output, 'Wrong degree between')       
        
    def test_multiple_friends_no_path(self: 'TestDegree') -> None:
        """
        A graph with 7 nodes are created. Then 2 specific nodes will be
        selected such that no path exists between these two nodes.
        """
        file = io.StringIO('A Dylan<a@dra.net>(Uni of Toronto):c@dra.net,'
                   'b@dra.net\nB Ba<b@dra.net>():\n'
                   'E Ea<e@dra.net>():z@dra.net\nZ Za<z@dra.net>'
                   '():d@dra.net\nD Da<d@dra.net>():\n'
                   'C Ca<c@dra.net>():\nS Ta<s@dra.net>():')
        network = construct_network(file)
        input_val = network.degree_between('a@dra.net', 'z@dra.net')
        expected_output = float('inf')
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
    
    def test_multiple_friends_one_path(self: 'TestDegree') -> None:
        """
        A graph with 9 nodes are created. Then 2 specific nodes will be 
        selected such that only one path exists between the two nodes. 
        Some paths will lead to a deadend. Test to see if even if it are 
        deadends in the graph, degree_between can still find the path 
        to target node from the beginning node.
        """
        
        file = io.StringIO('A Dylan<a@dra.net>(Uni of Toronto):b@dra.net\n'
                   'B Ba<b@dra.net>():c@dra.net,e@dra.net,g@dra.net\n'
                   'C Ca<c@dra.net>():d@dra.net\n'
                   'D Da<d@dra.net>():\n'
                   'E Ea<e@dra.net>():f@dra.net\n'
                   'F Fa<f@dra.net>():\n'
                   'G Ga<g@dra.net>():h@dra.net,i@dra.net\n'
                   'H Ha<h@dra.net>():\n'
                   'I Ia<i@dra.net>():\n')
        network = construct_network(file)
        input_val = network.degree_between('a@dra.net', 'i@dra.net')
        expected_output = 3
        self.assertEqual(input_val, expected_output, 'Wrong degree between')                 
    
    def test_one_person_with_friends_same_person(self: 'TestDegree') -> None:
        """
        Graph contains 6 nodes. 5 nodes are connected to the same node. That 
        same node is our target node. Test if the degree_between is still 0.
        """
        
        file = io.StringIO('A Dylan<a@dra.net>(Uni of Toronto):\n'
           'B Ba<b@dra.net>():a@dra.net\n'
           'C Ca<c@dra.net>():a@dra.net\n'
           'D Da<d@dra.net>():a@dra.net\n'
           'E Ea<e@dra.net>():a@dra.net\n'
           'F Fa<f@dra.net>():a@dra.net\n')
        network = construct_network(file)
        input_val = network.degree_between('a@dra.net', 'a@dra.net')
        expected_output = 0
        self.assertEqual(input_val, expected_output, 'Wrong degree between') 
    
    def test_long_graph_multiple_routes(self: 'TestDegree') -> None:
        """
        Graph with 20 are created. 2 specific nodes will be selected such that
        multiple paths exist between those 2 nodes.
        Test to see if the degree_between function can still find the shortest 
        path.
        """
        
        file = io.StringIO('A Dylan<a@dra.net>(Uni of Toronto):b@dra.net,'
                           'e@dra.net,f@dra.net\n'
                   'B Ba<b@dra.net>():c@dra.net,g@dra.net\n'
                   'C Ca<c@dra.net>():h@dra.net\n'
                   'D Da<d@dra.net>():e@dra.net\n'
                   'E Ea<e@dra.net>():i@dra.net\n'
                   'F Fa<f@dra.net>():j@dra.net\n,g@dra.net,i@dra.net'
                   'G Ga<g@dra.net>():k@dra.net\n'
                   'H Ha<h@dra.net>():g@dra.net,l@dra.net\n'
                   'I Ia<i@dra.net>():m@dra.net\n'
                   'J Ja<j@dra.net>():k@dra.net,m@dra.net,n@dra.net\n'
                   'K Ka<k@dra.net>():n@dra.net\n'
                   'L La<l@dra.net>():k@dra.net,n@dra.net\n'
                   'M Ma<m@dra.net>():n@dra.net\n'
                   'N Na<n@dra.net>():\n')
        network = construct_network(file)
        input_val = network.degree_between('a@dra.net', 'n@dra.net')
        expected_output = 3
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
        
    def test_starter_no_connected_nodes(self: 'TestDegree') -> None:
        """
        Graph with 3 nodes, the starting node is not connected to any node
        The other 2 nodes along with the target node is connected to each other
        """
        file = io.StringIO('Kyon<kyon@toronto.ca>(Uni of Toronto): \n'
                   
                        'Suzumiya Haruhi<Haruhi@toronto.ca>(Uni of Toronto):'
                        'YukiN@toronto.ca\n'
                        
                        'Nagato Yuki<YukiN@toronto.ca>(Uni of Toronto):'
                        'Haruhi@toronto.ca\n')
        network = construct_network(file)
        input_val = network.degree_between('kyon@toronto.ca',
                                           'Haruhi@toronto.ca')
        expected_output = float('inf')
        self.assertEqual(input_val, expected_output, 'Wrong degree between')

    def test_starter_no_connected_nodes(self: 'TestDegree') -> None:
        """
        Graph with 3 nodes, the starting node is connected to all nodes
        avaliable except for the target node.
        """
        file = io.StringIO('Kyon<kyon@toronto.ca>(Uni of Toronto): \n'
                   
                        'Suzumiya Haruhi<Haruhi@toronto.ca>(Uni of Toronto):'
                        'YukiN@toronto.ca\n'
                        
                        'Nagato Yuki<YukiN@toronto.ca>(Uni of Toronto):'
                        'Haruhi@toronto.ca\n')
        network = construct_network(file)
        input_val = network.degree_between('Haruhi@toronto.ca',
                                           'kyon@toronto.ca')
        expected_output = float('inf')
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
    
    def test_275_people(self: 'TestDegree') -> None:
        """
        Graph with 275 nodes are randomly generated. One node and node adjacent
        to that one node are selected. Test to see if degree_between is 1.
        """
        
        lst = []
        lst_email = []
        alph = 'abcdefghijklmnopqrstuvwxyz'
        for i in range(275):
            string = ''
            last = ''
            for n in range(5):
                string += alph[random.randint(0, 25)]
                last += alph[random.randint(0, 25)]
            name = string + ' ' + last
            email = string + '@user.net'
            school = 'University of Kawaii'
            if lst_email:
                friends = lst_email[random.randint(0, len(lst_email) - 1)]
            else:
                friends = ''
            final = name + '<' + email + '>(' + school + '):' + friends + '\n'
            if email not in lst_email:
                lst_email.append(email)
                lst.append(final)
        final_file = ''.join(lst)
        file = io.StringIO(final_file)
        network = construct_network(file)
        starting_email = network._emails[150]
        end_email = network.find_node_by_email(starting_email).get_friends()
        input_val = network.degree_between(starting_email, end_email[0])
        expected_output = 1
        self.assertEqual(input_val, expected_output, 'Wrong degree between')
     
     
################################ Unittest end #################################      
if __name__ == '__main__':
    unittest.main(exit=False)
