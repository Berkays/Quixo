from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, Dropout, Flatten, MaxPooling2D
import numpy as np

dataset = "datasets/dataset_move_ai.npz"
test_size = 0.33

if __name__ == "__main__":
    model = Sequential()
    # model.add(Flatten(input_shape=(5,5)))
    model.add(
        Conv2D(
            4,
            kernel_size=5,
            strides=(1, 1),
            padding='same',
            input_shape=(5, 5, 1)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu', name='Dense_1'))
    model.add(Dropout(0.4))
    model.add(Dense(32, activation='relu', name='Dense_2'))
    model.add(Dense(1, activation='sigmoid', name='Dense_Output'))

    model.compile(
        optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    data = np.load(dataset)
    X = data['arr_0'] / 2
    X = np.expand_dims(X, axis=-1)
    Y = data['arr_1']
    print(f"Dataset size : {len(X)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=test_size)
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    del X
    del Y

    model.fit(X_train, y_train, epochs=8, batch_size=192)

    model.save('value.h5')

    test_loss, test_acc = model.evaluate(X_test, y_test)

    print('Test accuracy:', test_acc)

    for i in range(0, 5):
        testCase = X_test[i]
        print(testCase.reshape(5,5))
        # testCase = np.expand_dims(testCase, axis=-1)
        print(testCase.shape)
        t = [testCase]
        pred = model.predict(np.array(t))[0][0]
        print(pred)
        if (pred < 0.5):
            print("Winner is O")
        else:
            print("Winner is X")
        print()