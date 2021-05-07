import sys
from textgenrnn import textgenrnn


def train(textgen, filename, weight_path, epochs=1, batch_size=128):
    textgen.train_from_file(filename, num_epochs=epochs)
    textgen.save(weight_path)


def load(textgen, filename):
    textgen.load(filename)


def load_pretrained_model(weight_path):
    textgen = textgenrnn()
    load(textgen, weight_path)
    return textgen


def generate(weight_path):
    n = 500
    textgen = load_pretrained_model(weight_path)
    gen = []
    for t in [0.8, 0.9, 1.0]:
        gen += textgen.generate(n, temperature=t, return_as_list=True)

    f = open("viper_generated.txt", "w")
    for line in gen:
        f.write(line + "\n")
    f.close()


# textgen = textgenrnn()
# train(
#     textgen,
#     "data/combined_albums_tracks_generated.txt",
#     "./weights/viper_v2.hdf5",
#     epochs=20,
# )
generate("./weights/viper_v2.hdf5")
