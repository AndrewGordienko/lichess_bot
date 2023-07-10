import pickle

with open('listfile.pkl', 'rb') as f:
    loaded_list = pickle.load(f)

for i in range(len(loaded_list)):
    print("--")
    print(len(loaded_list[i]))
    print(loaded_list[i][0].shape)
    print(loaded_list[i][1].shape)
