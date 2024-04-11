def path_with_arrows(p):
    path, len = p
    res = '[' + '->'.join([str(s) for s in path]) + ']'
    if len != None:
        res += '=' + str(len)
    return res