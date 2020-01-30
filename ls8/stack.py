class Stack:
    def __init__(self):
        self.data = []
        self.sp = -1

    def push(self,val):
        self.sp -= 1
        self.data.append(val)
        return self.data[-1]

    def pop(self):
        self.sp += 1
        return self.data.pop()
    
    def __repr__(self):
        return str(self.data)

