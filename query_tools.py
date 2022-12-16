def precedence(token):
    ''' returns precedence of logical operators'''
    __precedence = { "&":2, "|":1 }
    try:
        return __precedence[token]
    # cartch index out of range exception
    except KeyError:
        return -1

def get_type_of_token(token):
    """ gets type of token
    :param token: a token ('(',')','&','|', term)
    :returns token_type: type of token ('(':1 , ')':2 , '&':3 , '|':3 , term:4 )
    """
    if token == '(':
        return 1
    if token == ')':
        return 2
    if token == '&':
        return 3
    if token == '|':
        return 3
    return 4

def infix_to_postfix(infix):
    """ converts infix to postfix
    :param infix: a list of tokens
    :returns postfix: a list of tokens
    """
    stack = []
    postfix = []
    for token in infix:
        token = token.lower()
        
        token_type = get_type_of_token(token)
        if token_type == 1:
            stack.append(token)
        
        elif token_type == 2:
            while len(stack) > 0 and stack[-1] != '(' :
                postfix.append(stack.pop())
            stack.pop()
        elif token_type == 3:
            while len(stack) > 0 and precedence(token) <= precedence(stack[-1]):
                postfix.append(stack.pop(-1))
            stack.append(token)
        else:
            postfix.append(token) 
    while len(stack) > 0:
        postfix.append(stack.pop())
    return postfix
