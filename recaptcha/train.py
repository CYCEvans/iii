import random
import os
import glob
import json

from seq2seq.models import AttentionSeq2Seq, Seq2Seq
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, Callback
import numpy as np
from keras.utils.np_utils import to_categorical
from keras.layers import Convolution2D, MaxPooling2D, GRU, TimeDistributed, Conv2D
from keras.layers.recurrent import SimpleRNN
from keras.layers import Dense, Dropout, Activation, Flatten, RepeatVector, Bidirectional
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import SGD, Adam
from keras import backend as K
K.set_image_dim_ordering("th")


image_shape = (3, 60, 250)
max_caption_len = 8
images_dir = "pic"
labels_dir = "labels"
ch_index_dir = "ch_index"
testimages_dir = "pic_test"
testlabels_dir = "labels_test"
model_output = "checkpoints/"
ch_index = json.load(open(ch_index_dir))
vocab_size = len(ch_index)


class ValidateAcc(Callback):
    def __init__(self, image_model, val_data, val_label, model_output):
        self.image_model = image_model
        self.val = val_data
        self.val_label = val_label
        self.model_output = model_output
	# 每次epoch後都比對一次測試集
    def on_epoch_end(self, epoch, logs={}):
        print('\n------------------')
		#讀取最新的checkpoint
        self.image_model.load_weights(self.model_output+'weights.%02d.hdf5' % epoch)
        r = self.image_model.predict(self.val, verbose=0)
        y_predict = np.asarray([np.argmax(i, axis=1) for i in r])
        val_true = np.asarray([np.argmax(i, axis=1) for i in self.val_label])
        length = len(y_predict) * 1.0
        correct = 0
        for (true, predict) in zip(val_true, y_predict):
            if list(true) == list(predict):
                correct += 1
        print("Validation set acc is: ", correct/length)
        print('\n------------------')
		

def load_data():
    with open(images_dir, "rb") as f:
        images = np.load(f)
    with open(labels_dir, "rb") as f:
        labels = np.load(f)
    vocab_size = len(ch_index)
    labels_categorical = np.asarray([to_categorical(label, vocab_size) for label in labels])
    print("images shape", images.shape)
    print("input labels shape", labels_categorical.shape)
    train_data = images
    train_label = labels_categorical
    return train_data, train_label
	

def load_test_data():
    with open(testimages_dir = "pic_test", "rb") as f:
        images = np.load(f)
    with open(testlabels_dir, "rb") as f:
        labels = np.load(f)
    vocab_size = len(ch_index)
    labels_categorical = np.asarray([to_categorical(label, vocab_size) for label in labels])
    print("test images shape", images.shape)
    print("test labels shape", labels_categorical.shape)
    val_data = images
    val_label = labels_categorical
    return val_data, val_label


def create_simpleCnnRnn(image_shape, max_caption_len, vocab_size):
    image_model = Sequential()
    image_model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=image_shape))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(Convolution2D(32, 3, 3))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(MaxPooling2D(pool_size=(2, 2)))
    image_model.add(Dropout(0.25))
    image_model.add(Convolution2D(64, 3, 3, border_mode='valid'))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(Convolution2D(64, 3, 3))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(MaxPooling2D(pool_size=(2, 2)))
    image_model.add(Dropout(0.25))
    image_model.add(Flatten())
    image_model.add(Dense(128))
    image_model.add(RepeatVector(max_caption_len))
    image_model.add(Bidirectional(GRU(output_dim=128, return_sequences=True)))
    image_model.add(TimeDistributed(Dense(vocab_size)))
    image_model.add(Activation('softmax'))
    sgd = SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
    image_model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return image_model
 
       
def create_imgText(image_shape, max_caption_len,vocab_size):
    image_model = Sequential()
    image_model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=image_shape))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(Convolution2D(32, 3, 3))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(MaxPooling2D(pool_size=(2, 2)))
    image_model.add(Dropout(0.25))
    image_model.add(Convolution2D(64, 3, 3, border_mode='valid'))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(Convolution2D(64, 3, 3))
    image_model.add(BatchNormalization())
    image_model.add(Activation('relu'))
    image_model.add(MaxPooling2D(pool_size=(2, 2)))
    image_model.add(Dropout(0.25))
    image_model.add(Flatten())
    image_model.add(Dense(128))
    image_model.add(RepeatVector(1))
    model = Seq2Seq(input_dim=128, input_length=1, hidden_dim=128, output_length=max_caption_len,
                             output_dim=128, peek=True)
    image_model.add(model)
    image_model.add(TimeDistributed(Dense(vocab_size)))
    image_model.add(Activation('softmax'))
    adam = Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    image_model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    return image_model


def build_cnn(image_shape, max_caption_len, vocab_size):
    model = Sequential()
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(3, 3), input_shape=image_shape,
                     activation='relu', padding='same'))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=32, kernel_size=(3, 3),
                     activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=64, kernel_size=(3, 3),
                     activation='relu', padding='same'))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=64, kernel_size=(3, 3),
                     activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(128))
    model.add(RepeatVector(max_caption_len))
    model.add(Bidirectional(GRU(output_dim=128, return_sequences=True)))
    model.add(TimeDistributed(Dense(vocab_size)))
    model.add(Activation('softmax'))
    adam = Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    return model

def main():
    image_model = build_cnn(image_shape, max_caption_len, vocab_size)
    if not os.path.exists(model_output):
        os.makedirs(model_output)
    else:
        list_of_files = glob.glob(model_output + "/*")
        if len(list_of_files) != 0:
            latest_file = max(list_of_files, key=os.path.getctime)
            print("load model.....{}".format(latest_file))
            # image_model = load_model(latest_file)#SGD
            image_model.load_weights(latest_file)#Adam
    split_ratio = 0.7
    train, train_label = load_data()
	val_test, test_label = load_test_data()
    check_pointer = ModelCheckpoint(filepath=model_output + "weights.{epoch:02d}.hdf5")
    val_acc_check_pointer = ValidateAcc(image_model, val_test, test_label, model_output)
    image_model.fit(train, train_label,
                    shuffle=True, batch_size=16, epochs=10, validation_split=0.2, verbose=1,
                    callbacks=[check_pointer, val_acc_check_pointer])
  
if __name__ == "__main__":
    main()
