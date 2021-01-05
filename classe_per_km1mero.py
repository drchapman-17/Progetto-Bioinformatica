class Km1Mer:
    def __init__(self, label):
        self.label = label
        
    def __hash__(self):
        return hash(self.label)  
    
    def __eq__ (self, other):
        if other is None:
            return False
        elif type(self)!=type(other):
            return False
        else:
            return (self.label == other.label)


    def __str__(self):
        return self.label
