class Bar:
    def __init__(self, name:str):
        self.name = name

    def try_something_stupid(self):
        try:
            print(self.name)
        except ValueError as e:
            print(e)
        #except:
        #    pass
    