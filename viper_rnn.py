from textgenrnn import textgenrnn

def train(textgen, filename, weight_path="", epochs=1):
    textgen.train_from_file(filename, num_epochs=epochs)
    if weight_path:
        textgen.save(weight_path)
    else:
        textgen.save()

def load(textgen, filename):
    textgen.load(filename)

textgen = textgenrnn()
# load(textgen, "textgenrnn_weights_saved.hdf5")
train(textgen, "names_generated.txt", "viper_rnn_gen_texdt_weights.hdf5", 5)
print(textgen.generate(temperature=0.5, n=50))