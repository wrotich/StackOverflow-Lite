# Model class for the questions part
class Question: 
    def __init__(self, qstn_id, question):
        self.qstn_id = qstn_id
        self.question = question

    # method for acessing class attributes as items 
    def __getitem__(self,item):
        return getattr(self, item) 
    
    # method for displaying class objects as dictionaries 
    def __repr__(self):
        return repr(self.__dict__)
        

# Model class for the answers part
class Answer:
    def __init__(self, ans_id, answer, qstn_id):
        self.ans_id = ans_id
        self.answer = answer
        self.qstn_id = qstn_id

    # method for acessing class attributes as items 
    def __getitem__(self,item):
        return getattr(self, item) 
    
    # method for displaying class objects as dictionaries 
    def __repr__(self):
        return repr(self.__dict__)
