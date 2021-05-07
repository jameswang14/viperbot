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


# textgen = textgenrnn()
# train(
#     textgen,
#     "data/combined_albums_tracks_generated.txt",
#     "./weights/viper_v2.hdf5",
#     epochs=20,
# )
textgen = load_pretrained_model("./weights/viper_v2.hdf5")
print(textgen.generate(10, temperature=0.9))
