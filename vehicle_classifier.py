# -*- coding: utf-8 -*-
"""Vehicle Classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m4AIxczrAdQBm-o86851zdgWxSvmCyic
"""

import numpy as np
import pandas as pd
import os
from re import search
import shutil
import natsort
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2



!pip install natsort

from google.colab import drive
drive.mount('/content/drive')

dir_path = '/content/drive/MyDrive/vehicle_dataset/images/'

# Opening single Image 
image_open = Image.open('/content/drive/MyDrive/vehicle_dataset/images/Rickshaw/images/rickshaw (54).jpg')
plt.imshow(image_open)
plt.title('Image : Rickshaw 53')
plt.show()

Train_dir = '/content/drive/MyDrive/vehicle_dataset/images/'
Categories = ['Bicycle/images','Bus/images','Car/images','Cng/images','Rickshaw/images','Truck/images',]
for i in Categories:
    path = os.path.join(Train_dir,i)
    for img in os.listdir(path):
        old_image = cv2.imread(os.path.join(path,img),cv2.COLOR_BGR2RGB)
        new_image=cv2.resize(old_image,(256,256))
        plt.imshow(old_image)
        plt.show()
        break
    break

len(Categories)



new_image=cv2.resize(old_image,(256,256))
plt.imshow(new_image)
plt.show()

from tensorflow.keras.preprocessing.image import ImageDataGenerator

!pip install --upgrade tensorflow

datagen = ImageDataGenerator(rescale = 1/255,
                            shear_range = 0.2,
                            zoom_range = 0.2,
                            horizontal_flip = True,
                            vertical_flip = True,
                            validation_split = 0.2)

train_datagen = datagen.flow_from_directory(Train_dir,
                                target_size = (256,256),
                                batch_size =16,
                                class_mode = 'categorical',
                                subset = 'training')
val_datagen = datagen.flow_from_directory(Train_dir,
                                         target_size = (256,256),
                                    batch_size =16,
                                    class_mode = 'categorical',
                                    subset = 'validation')

train_datagen.class_indices

from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.layers import Dense,Activation,Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D,Dropout,BatchNormalization

model1 = Sequential()
model1.add(Conv2D(64,(3,3),activation='relu',padding='same',input_shape=(256,256,3)))
model1.add(MaxPooling2D(3,3))
model1.add(Conv2D(32,(3,3),activation='relu',padding='same'))
model1.add(MaxPooling2D(2,2))
model1.add(Conv2D(16,(3,3),activation='relu',padding='same'))
model1.add(MaxPooling2D(2,2))
model1.add(BatchNormalization())

model1.add(Dropout(0.1))
model1.add(Flatten())
model1.add(Dense(64,activation='relu'))
model1.add(Dense(32,activation='relu'))
model1.add(Dense(6,activation='softmax'))
model1.summary()

model=Sequential()
model.add(Conv2D(64,(3,3),activation='relu',padding='same',input_shape=(256,256,3)))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.1))
model.add(Conv2D(64,(3,3),activation='relu',padding='same'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.1))
model.add(Conv2D(64,(3,3),activation='relu',padding='same'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.1))
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.1))
model.add(Conv2D(128,(3,3),activation='relu',padding='same'))
model.add(MaxPooling2D(2,2))
model.add(BatchNormalization())
model.add(Dropout(0.1))
model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(6,activation='softmax'))
model.summary()

model.compile(optimizer = 'adam', loss='categorical_crossentropy', 
              metrics=['accuracy'])
checkpoint=ModelCheckpoint(r'vehicale_classifier.h5',
                          monitor='val_loss',
                          mode='min',
                          save_best_only=True,
                          verbose=1)
earlystop=EarlyStopping(monitor='val_loss',
                       min_delta=0.001,
                       patience=10,
                       verbose=1,
                       restore_best_weights=True)

callbacks=[checkpoint,earlystop]

model_history = model.fit(train_datagen, validation_data=val_datagen,
                          epochs = 30,
                          callbacks =callbacks)

while True:
  pass

train_acc = model_history.history['accuracy']
val_acc = model_history.history['val_accuracy']
epoachs = range(1,20)
plt.plot(epoachs,train_acc,'g',label='Training Accuracy')
plt.plot(epoachs,val_acc,'b',label='Validation Accuracy')
plt.title("Training and Validation Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

loss_train=model_history.history['loss']
loss_val=model_history.history['val_loss']
epochs=range(1,20)
plt.plot(epochs,loss_train,'g',label='Training Loss')
plt.plot(epochs,loss_val,'b',label='Validation Loss')
plt.title("Training and Validation Loss")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

model.save('vehicale_classifier.h5')

test_image=r'/content/drive/MyDrive/vehicle_dataset/Test/test_2.jpg'
image_result=Image.open(test_image)

from tensorflow.keras.preprocessing import image
test_image=image.load_img(test_image,target_size=(256,256))
test_image=image.img_to_array(test_image)
test_image=test_image/255
test_image=np.expand_dims(test_image,axis=0)
result=model.predict(test_image)
print(np.argmax(result))
Categories=['Bicycle','Bus','Car','Cng','Rickshaw','Truck']
image_result=plt.imshow(image_result)
plt.title(Categories[np.argmax(result)])
plt.show()

import tensorflow as tf
from tensorflow.keras.applications import DenseNet121, DenseNet169, DenseNet201, EfficientNetB7

from IPython.display import SVG
!pip install efficientnet

import efficientnet.tfkeras as efn

from keras.layers import Conv2D, MaxPooling2D

model_efficientnet_b7 = tf.keras.Sequential([
        efn.EfficientNetB7(
            input_shape=(256, 256, 3),
            weights='imagenet',
            include_top=False
        ),
        MaxPooling2D(pool_size=(2,2)),
        Flatten(),
        BatchNormalization(),
        Dropout(0.3),
        Dense(9, activation='softmax')
    ])

model_efficientnet_b7.compile(optimizer = 'adam', loss='categorical_crossentropy', 
              metrics=['accuracy'])

checkpoint=ModelCheckpoint(r'vehicale_classifier.h5',
                          monitor='val_loss',
                          mode='min',
                          save_best_only=True,
                          verbose=1)
earlystop=EarlyStopping(monitor='val_loss',
                       min_delta=0.001,
                       patience=10,
                       verbose=1,
                       restore_best_weights=True)

callbacks=[checkpoint,earlystop]

model_history = model.fit(train_datagen, validation_data=val_datagen,
                          epochs = 20,
                          callbacks =callbacks)

while True:
  pass