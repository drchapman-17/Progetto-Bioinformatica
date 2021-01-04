class Km1Mer:
    def __init__(self, label):
        self.label = label
        
    def __hash__(self):
        return hash(self.label)  
    
    def __str__(self):
        return self.label
