from boolean_model import BooleanModel

if __name__ == "__main__":
    model = BooleanModel('./corpus/*', 'english')
    # print(model.vocabulary)
    print(model.query("recipe"))