from boolean_model import BooleanModel

if __name__ == "__main__":
    model = BooleanModel('./corpus/soccer/*', 'english')
    print(list(model.vocabulary)[-1])
    # while(True):
        # txt = input(">>> ")
    # txt = "Karim & Benzema"
    # print(model.query(txt))