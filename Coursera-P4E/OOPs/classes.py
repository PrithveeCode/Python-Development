class Animal:
    def __init__(self, species:str, age:int): 
        '''
        @brief: I Am Trying To learn about specifying Datatypes in Python Functions..
        '''
        self.species = species
        self.age = age

    def hiAnimal(self):
        if self.species == "doggo":
            print("Hi! Cute Doggo!")
        else:
            print(f"Hi {self.species}.")



def main():
    a1 = Animal("doggo", 12) 
    a1.hiAnimal()
    return



'''
@brief: From Here The Main () Execution Starts:
'''
if __name__ == "__main__":
    main()