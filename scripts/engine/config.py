
"""
 PLUS
 -- min_N
 -- no_cover
 -- max_dist
 SEARCH
 -- no_skip_atom
 -- no_skip_any
 -- max_dist


"""

class Config:

    def __init__(self):
        self.atom_plus = {"min_N":1, "no_cover":1, "max_dist": 0 }
        self.var_plus  = {"min_N":1, "no_cover":1, "max_dist": 3 }
        self.search  = {"no_skip_atom": 0, "no_skip_any": 0, "max_dist": 3 }
        self.MAX_DIST = 2
        self.ATOM_PLUS_MAX_DIST = 0
        self.VAR_PLUS_MAX_DIST = 2

    def reset(self, a, b, c, d, e):
        pass
 

class NodeConfig:

    def __init__(self):
        self.max_dist = 3
        self.slot_len = [0, 0]
        self.slot_not_beginswith = ( )
        self.slot_beginswith = ( )


    def equal(self, r):
        return False
