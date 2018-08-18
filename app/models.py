# Model class for the question
class Question:
    def __init__(self, qstn_id, question):
        self.qstn_id = qstn_id
        self.question = question

    # method to enable us acess class attributes as items 
    def __getitem__(self,item):
        return getattr(self, item) 
    
    # method to enable us display class objects as dictionaries 
    def __repr__(self):
        return repr(self.__dict__)
        

# Model class for the answer
class Answer:
    def __init__(self, ans_id, answer, qstn_id):
        self.ans_id = ans_id
        self.answer = answer
        self.qstn_id = qstn_id

    # method to enable us acess class attributes as items 
    def __getitem__(self,item):
        return getattr(self, item) 
    
    # method to enable us display class objects as dictionaries 
    def __repr__(self):
        return repr(self.__dict__)