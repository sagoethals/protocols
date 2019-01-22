'''
Initialization scripts
'''

__all__ = ['is_model']

def is_model():
    '''
    Returns True if it runs not a rig and a model is going to be simulated.
    '''
    # This should probably rather test for the presence of an NI board
    try:
        import brian2
        return True
    except ImportError:
        return False
