First Year assignment with basic graph theory components.

QUERIES

All emails provided are located in example.timf

Commands issued via keyboard:

friends x: list all friends of person x (where x is an e-mail address). Output this list on its own line, separated by spaces. For example,
    >>> friends harold@alias.me
    
    >>> friends hl@imaeatchu.com
    Annie Dr. Evil
    >>> friends andy@toronto.edu
    Brian Law

degree x y: print the degree of separation between person x and person y (where people are specified by e-mail address). In the network graph, the degree of separation between x and y corresponds to the number of edges on the shortest path between x and y. If there is no path between x and y, then the degree of separation is undefined. A person has 0 degrees of separation with him/herself. Output an integer on its own line. For example,
    >>> degree liudavid@cdf.toronto.edu henry@hyde.net
    2
    >>> degree harold@alias.me andy@toronto.edu
    inf
    >>> degree harold@alias.me harold@alias.me
    0

degrees x d: list all people separated from person x by exactly d degrees of separation (where x is an e-mail address). Outputs a list on its own line, separated by spaces. The list is sorted in alphabetical order (using the standard string ordering). For example,
    >>> degrees harold@alias.me 100
    
    >>> degrees annie@mgo.org 0
    Annie
    >>> degrees annie@mgo.org 1
    Hannibal Lecter Henry Jekyll
    >>> degrees annie@mgo.org 2
    Anya Tafliovich Dr. Evil

mutual x y: list mutual friends of x and y, i.e. people who are friends with both x and y (where people are specified by e-mail address). Outputs a list on its own line, separated by spaces. The list is sorted in alphabetical order. For example,
    >>> mutual harold@alias.me andy@toronto.edu
    
    >>> mutual dr@evil.net annie@mgo.org
    Hannibal Lecter Henry Jekyll 
    >>> mutual lungj@cdf.toronto.edu sengels@cdf.toronto.edu
    David Liu

likely x: suggest missing friends for person x by listing the likeliest missing friends (where x is an e-mail address). The likeliest missing friend is a person who shares the most mutual friends with person x and who is not already a friend of x. Outputs a list on its own line, separated by spaces. The list issorted in alphabetical order. For example,
    >>> likely dfinn2003@gmail.com
    
    >>> likely lungj@cdf.toronto.edu
    Anya Tafliovich

classmates x d: list all people within d degrees of separation of x who went to the same school (where x is an e-mail address). Outputs a list on its own line, separated by spaces. The list is sorted in alphabetical order. For example,
    >>> classmates harold@alias.me 5

    >>> classmates dfinn2003@gmail.com 3
    Rosalie Mullins

    >>> classmates sengels@cdf.toronto.edu 3
    Andy Hwang Brian Law David Liu Dr. Evil Jonathan Lung

quit: quit the program


