#!/usr/bin/env python

import numpy as np
import tensorflow as tf
from dataset import fashion_MNIST
from util import config
from progressbar import ProgressBar

def model(batch_x):

    """
    We will define the learned variables, the weights and biases,
    within the method ``model()`` which also constructs the neural network.
    The variables named ``hn``, where ``n`` is an integer, hold the learned weight variables.
    The variables named ``bn``, where ``n`` is an integer, hold the learned bias variables.
    In particular, the first variable ``h1`` holds the learned weight matrix that
    converts an input vector of dimension ``n_input + 2*n_input*n_context``
    to a vector of dimension ``n_hidden_1``.
    Similarly, the second variable ``h2`` holds the weight matrix converting
    an input vector of dimension ``n_hidden_1`` to one of dimension ``n_hidden_2``.
    The variables ``h3``, ``h5``, and ``h6`` are similar.
    Likewise, the biases, ``b1``, ``b2``..., hold the biases for the various layers.

    The model consists of fully connected 2 hidden layers along with input and output layers.
    """

    b1 = tf.get_variable("b1", [config.n_hidden1], initializer = tf.zeros_initializer())
    h1 = tf.get_variable("h1", [config.n_input, config.n_hidden1],
                         initializer = tf.contrib.layers.xavier_initializer())
    layer1 = tf.nn.relu(tf.add(tf.matmul(batch_x,h1),b1))

    b2 = tf.get_variable("b2", [config.n_hidden2], initializer = tf.zeros_initializer())
    h2 = tf.get_variable("h2", [config.n_hidden1, config.n_hidden2],
                         initializer = tf.contrib.layers.xavier_initializer())
    layer2 = tf.nn.relu(tf.add(tf.matmul(layer1,h2),b2))

    b3 = tf.get_variable("b3", [config.n_class], initializer = tf.zeros_initializer())
    h3 = tf.get_variable("h3", [config.n_hidden2, config.n_class],
                         initializer = tf.contrib.layers.xavier_initializer())

    layer3 = tf.add(tf.matmul(layer2,h3),b3)

    return layer3


def compute_loss(predicted, actual):
    """
    This routine computes the cross entropy log loss for each of output node/classes.
    returns mean loss is computed over n_class nodes.
    """

    total_loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits = predicted,labels = actual)
    avg_loss = tf.reduce_mean(total_loss)
    return avg_loss


def create_optimizer():
    """
    we will use the Adam method for optimization (http://arxiv.org/abs/1412.6980),
    because, generally, it requires less fine-tuning.
    """

    optimizer = tf.train.AdamOptimizer(learning_rate=config.learning_rate)
    return optimizer


def one_hot(n_class, Y):
    """
    return one hot encoded labels to train output layers of NN model
    """
    return np.eye(n_class)[Y]


def train(X_train, X_val, X_test, y_train, y_val, y_test, verbose = False):
    """
    Trains the network, also evaluates on test data finally.
    """
    # Creating place holders for image data and its labels
    X = tf.placeholder(tf.float32, [None, 784], name="X")
    Y = tf.placeholder(tf.float32, [None, 10], name="Y")

    # Forward pass on the model
    logits = model(X)

    # computing sofmax cross entropy loss with logits
    avg_loss = compute_loss(logits, Y)

    # create adams' optimizer, compute the gradients and apply gradients (minimize())
    optimizer = create_optimizer().minimize(avg_loss)

    # compute validation loss
    validation_loss = compute_loss(logits, Y)

    # evaluating accuracy on various data (train, val, test) set
    correct_prediction = tf.equal(tf.argmax(logits,1), tf.argmax(Y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    # initialize all the global variables
    init = tf.global_variables_initializer()

    # starting session to actually execute the computation graph
    with tf.Session() as sess:

        # all the global varibles holds actual values now
        sess.run(init)

        # looping over number of epochs
        for epoch in range(config.n_epoch):

            epoch_loss = 0.

            # calculate number of batches in dataset
            num_batches = np.round(X_train.shape[0]/config.batch_size).astype(int)

            # For displaying progresbar
            pbar = ProgressBar(term_width=80)

            # looping over batches of dataset
            for i in pbar(range(num_batches)):

                # selecting batch data
                batch_X = X_train[(i*config.batch_size):((i+1)*config.batch_size),:]
                batch_y = y_train[(i*config.batch_size):((i+1)*config.batch_size),:]

                # execution of dataflow computational graph of nodes optimizer, avg_loss
                _, batch_loss = sess.run([optimizer, avg_loss],
                                                       feed_dict = {X: batch_X, Y:batch_y})

                # summed up batch loss for whole epoch
                epoch_loss += batch_loss

            # average epoch loss
            epoch_loss = epoch_loss/num_batches
            # compute train accuracy
            train_accuracy = float(accuracy.eval({X: X_train, Y: y_train}))
            # compute validation loss
            val_loss = sess.run(validation_loss, feed_dict = {X: X_val ,Y: y_val})
            # compute validation accuracy
            val_accuracy = float(accuracy.eval({X: X_val, Y: y_val}))

            # display within an epoch (train_loss, train_accuracy, valid_loss, valid accuracy)
            if verbose:
                print("epoch:{epoch_num}, train_loss: {train_loss}, train_accuracy: {train_acc},"
                 "val_loss: {valid_loss}, val_accuracy: {val_acc}".format(
                 epoch_num = epoch,
                 train_loss = round(epoch_loss,3),
                 train_acc = round(train_accuracy,2),
                 valid_loss = round(float(val_loss),3),
                 val_acc = round(val_accuracy,2)
                 ))

        # calculate final accuracy on never seen test data
        print ("Test Accuracy:", accuracy.eval({X: X_test, Y: y_test}))
        sess.close()


def main(_):

    # Instantiating the dataset class
    fashion_mnist = fashion_MNIST.Dataset(data_download_path='../data/fashion', validation_flag=True, verbose=True)

    # Loading the fashion MNIST data
    X_train, X_val, X_test, Y_train, Y_val, Y_test = fashion_mnist.load_data()

    # Showing few exapmle images from dataset in 2D grid
    fashion_mnist.show_samples_in_grid(w=10,h=10)

    # One hot encoding of labels for output layer training
    y_train =  one_hot(config.n_class, Y_train)
    y_val = one_hot(config.n_class, Y_val)
    y_test = one_hot(config.n_class, Y_test)

    # Let's train and evaluate the fully connected NN model
    train(X_train, X_val, X_test, y_train, y_val, y_test, True)



if __name__ == '__main__' :
    tf.app.run(main)
