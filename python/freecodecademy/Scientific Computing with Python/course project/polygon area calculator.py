class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, input):
        self.width = input

    def set_height(self, input):
        self.height = input

    def get_area(self):
        return self.width * self.height
    
    def get_perimeter(self):
        return (2 * (self.width + self.height))
    
    def get_diagonal(self):
        return ((self.width ** 2 + self.height ** 2) ** .5)
    
    def get_picture(self):
        output = []
        
        if self.width > 50 or self.height > 50:
            return 'Too big for picture.'
        
        for _ in range(1, self.height+1):
            output.append("*"*(self.width)) 
        
        return '\n'.join(output) + '\n'

    def get_amount_inside(self, shape):
        # e.g. (8 // 4) * (4 // 4)  = 2
        test1 = ((self.height // shape.height) * (self.width // shape.height))
        test2 = 1 if self.height > shape.height and self.width > shape.width else 0

        return max(test1, test2)

    def __str__(self):
        return f'Rectangle(width={self.width}, height={self.height})'

class Square(Rectangle):
    def __init__(self, length):
        self.width = self.height = length

    def set_side(self, input):
        self.width = self.height = input

    def __str__(self):
        return f'Square(side={self.width})'
    
    def set_width(self, input):
        self.width = self.height = input

    def set_height(self, input):
        self.height = self.width = input