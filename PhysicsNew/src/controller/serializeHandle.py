

''''
   serialization format : 
   
   
'''
def serializeHandle(handle, out):
    ''' Serializes a handle to some output stream. 
    Here, we backtrack a handle to it's initial position, then
    write the handle from its initial to final state. 
    
    Thus, if we have a final state handle we can serialize it easily
    and have some external program display it.
    
    handle : Handle, the handle we will serialize
    out : the output stream that we will write the handle to
    '''