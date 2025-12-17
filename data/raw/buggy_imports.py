
import os, sys, pickle

def save_data(data):
    with open("data.pkl", "wb") as f:
        pickle.dump(data, f)  # insecure serialization
