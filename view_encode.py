import pickle

with open("encodings/encodings.pickle", "rb") as f:
    data = pickle.load(f)
    print("Number of encodings:", len(data["encodings"]))
    print("Number of names:", len(data["names"]))
