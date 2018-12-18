# tf-fashionMNIST

Deep Learning with Tensorflow

1. This repo implements each step in building deep learning model from scratch using python & Tensorflow.
2. Most tutorials/blogs/implementations import datasets from APIs like tensorflow/keras etc. We won't, instead we will make our data loader.
3. We will not use any high level APIs like keras or tf.keras etc. We will stick to basic tensorflow

Fashion MNIST Dataset

* Fashion-MNIST is a dataset of Zalando's article images consisting of a training set of 60,000 examples and a test set of 10,000 examples.
* Each example is a 28x28 grayscale image, associated with a label from 10 classes.
* Fashion-MNIST is a direct drop-in replacement for the original MNIST digit dataset for benchmarking machine learning algorithms. It shares the same image size and structure of training and testing splits.

Why Fashion MNIST ?

* MNIST is too easy
* MNIST is overused
* MNIST can not represent modern CV tasks (like Batchnorm)

MNIST is often the first dataset researchers try. "If it doesn't work on MNIST, it won't work at all", they said. "Well, if it does work on MNIST, it may still fail on others."

Deep Learning heros like Ian Goodfellow & Francois Chollet have advised serious researchers to stay away from digit recognition MNIST.
