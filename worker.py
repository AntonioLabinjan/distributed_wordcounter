import zmq
import time
from collections import Counter
import random

def count_words(text):
    words = text.lower().split()
    return dict(Counter(words))

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:5557")

    texts = [
        "Ovo je primjer teksta koji će worker obraditi",
        "Distribuirani sustavi su zakon za skalabilnost",
        "Python i ZeroMQ zajedno su moćan tandem",
        "Svaki nod šalje svoje rezultate centralnom serveru",
        "Svaki tekst ima različit broj riječi"
    ]

    while True:
        text = random.choice(texts)
        word_counts = count_words(text)
        message = {"word_counts": word_counts}
        print(f"Worker sending: {message}")
        socket.send_json(message)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
