class Rectangle():
    def __init__(self,length,width):
        self.length = length
        self.width = width
        
    def __add__(self, other):
        width = self.width + other.width
        length = self.length + other.length
        return Rectangle(length,width)
    
    def __sub__(self,other):
        width = self.width - other.width
        length = self.length - other.length
        return Rectangle(length,width)
    
    def __mul__(self,other):
        width = self.width * other.width
        length = self.length * other.length
        return Rectangle(length,width)
    
    def __truediv__(self,other):
        width = self.width / other.width
        length = self.length / other.length
        return Rectangle(length,width)
    
    def __str__(self):
        string = ""
        if(self.width > 0 and self.length > 0):
            for i in range(0,self.width):
                for i in range(0,self.length):
                    string += "#"
            string += "\n"

def Square(Rectangle):
    def __init__(self, length):
      Rectangle.length = length
      Rectangle.width = length