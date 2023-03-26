import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras import Input
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.layers import Dense, Flatten, Dropout, ZeroPadding3D, ConvLSTM2D, Reshape, BatchNormalization, Activation, Conv2D, LayerNormalization
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import TimeDistributed, RepeatVector,Permute, Multiply, Add
from tensorflow.keras.applications import MobileNetV2, VGG16
from tensorflow.keras.layers import ELU, ReLU, LeakyReLU, Lambda, Dense, Bidirectional, Conv3D, GlobalAveragePooling2D, Multiply, MaxPooling3D, MaxPooling2D, Concatenate, Add, AveragePooling2D 
from tensorflow.keras.initializers import glorot_uniform, he_normal
from tensorflow.keras.models import Model
from tensorflow.keras.backend import expand_dims
from tensorflow.keras.regularizers import l2
from tensorflow.python.keras import backend as K

if __name__ == "__main__":
    from sep_conv_rnn import SepConvLSTM2D, AttenSepConvLSTM2D
    from InputMode import InputMode
else:
    from .sep_conv_rnn import SepConvLSTM2D, AttenSepConvLSTM2D
    from .InputMode import InputMode



class NNModel(object):
    """
    Neural Network Model
    This class is a Singleton wrapper for the trained
    Neural Network model.
    Static variables:
        input_mode: InputMode
    Args:
        input_mode (InputMode): The type of the input data (frames, differences or both).
    Methods:
        __init__(reized: int): Instantiates the class variables.
    """
    
    _instance = None

    def __init__(self, input_mode: InputMode, chunk_size: int = 32, frame_size: int = 224, cnn_trainable: bool = True, cnn_dropout: float = 0.25, seed: int = 42, lstm_type: str = 'sepconv', lstm_dropout: float = 0.25, weight_decay: float = 2e-5, frame_diff_interval: int = 1, dense_dropout: float = 0.3):
        if NNModel._instance is not None:
            raise RuntimeError('NNModel has already been initialized.')
        
        self.input_mode = input_mode
        self.chunk_size = chunk_size
        self.frame_size = frame_size
        self.cnn_trainable = cnn_trainable
        self.cnn_dropout = cnn_dropout
        self.seed = seed
        self.lstm_type = lstm_type
        self.lstm_dropout = lstm_dropout
        self.weight_decay = weight_decay
        self.frame_diff_interval = frame_diff_interval     
        self.dense_dropout = dense_dropout   
        self.model = self.generate_model()

    def generate_model(self):
        
        """
        Depending on the Input Mode, we are deciding
        how the model's architecture is going to look like.
        """
        if self.input_mode == InputMode.BOTH:
            frames = True
            differences = True
        elif self.input_mode == InputMode.ONLY_FRAMES:
            frames = True
            differences = False
        elif self.input_mode == InputMode.ONLY_DIFFERENCES:
            frames = False
            differences = True

        if frames:
            frames_input = Input(shape = (self.chunk_size, self.frame_size, self.frame_size, 3), name = 'frames_input')
            frames_cnn = MobileNetV2(input_shape = (self.frame_size, self.frame_size, 3), alpha = 0.35, weights = 'imagenet', include_top = False)
            frames_cnn = Model(inputs = [frames_cnn.layers[0].input], outputs = [frames_cnn.layers[-30].output] )

            for layer in frames_cnn.layers:
                layer.trainable = self.cnn_trainable
                
            frames_cnn = TimeDistributed(frames_cnn, name = 'frames_CNN')(frames_input)
            frames_cnn = TimeDistributed(LeakyReLU(alpha = 0.1), name = 'leaky_relu_1_')(frames_cnn)
            frames_cnn = TimeDistributed(Dropout(self.cnn_dropout, seed = self.seed), name = 'dropout_1_')(frames_cnn)

            if self.lstm_type == 'sepconv':
                frames_lstm = SepConvLSTM2D(filters = 64, kernel_size = (3, 3), padding = 'same', return_sequences = False, dropout = self.lstm_dropout, recurrent_dropout = self.lstm_dropout, name = 'SepConvLSTM2D_1', kernel_regularizer = l2(self.weight_decay), recurrent_regularizer = l2(self.weight_decay))(frames_cnn)
            elif self.lstm_type == 'conv':    
                frames_lstm = ConvLSTM2D(filters = 64, kernel_size = (3, 3), padding = 'same', return_sequences = False, dropout = self.lstm_dropout, recurrent_dropout = self.lstm_dropout, name = 'ConvLSTM2D_1', kernel_regularizer = l2(self.weight_decay), recurrent_regularizer = l2(self.weight_decay))(frames_cnn)
            elif self.lstm_type == 'asepconv':    
                frames_lstm = AttenSepConvLSTM2D(filters = 64, kernel_size = (3, 3), padding = 'same', return_sequences = False, dropout = self.lstm_dropout, recurrent_dropout = self.lstm_dropout, name = 'AttenSepConvLSTM2D_1', kernel_regularizer = l2(self.weight_decay), recurrent_regularizer = l2(self.weight_decay))(frames_cnn)
            elif self.lstm_type == '3dconv':
                frames_lstm = conv3d_block(frames_cnn, 'frames_3d_conv_block')(frames_cnn)
            else:
                raise Exception("lstm type not recognized!")

            frames_lstm = BatchNormalization(axis = -1)(frames_lstm)
        
        if differences:

            frames_diff_input = Input(shape = (self.chunk_size - self.frame_diff_interval, self.frame_size, self.frame_size, 3), name='frames_diff_input')
            frames_diff_cnn = MobileNetV2(input_shape = (self.frame_size, self.frame_size, 3), alpha = 0.35, weights = 'imagenet', include_top = False)
            frames_diff_cnn = Model(inputs = [frames_diff_cnn.layers[0].input], outputs = [frames_diff_cnn.layers[-30].output])
    
            for layer in frames_diff_cnn.layers:
                layer.trainable = self.cnn_trainable
        
            frames_diff_cnn = TimeDistributed(frames_diff_cnn,name = 'frames_diff_CNN')(frames_diff_input)
            frames_diff_cnn = TimeDistributed(LeakyReLU(alpha = 0.1), name='leaky_relu_2_')(frames_diff_cnn)
            frames_diff_cnn = TimeDistributed(Dropout(self.cnn_dropout, seed = self.seed), name='dropout_2_')(frames_diff_cnn)

            if self.lstm_type == 'sepconv':
                frames_diff_lstm = SepConvLSTM2D(filters = 64, kernel_size = (3, 3), padding='same', return_sequences = False, dropout = self.lstm_dropout, recurrent_dropout = self.lstm_dropout, name = 'SepConvLSTM2D_2', kernel_regularizer = l2(self.weight_decay), recurrent_regularizer = l2(self.weight_decay))(frames_diff_cnn)
            elif self.lstm_type == 'conv':    
                frames_diff_lstm = ConvLSTM2D(filters = 64, kernel_size = (3, 3), padding = 'same', return_sequences = False, dropout = self.lstm_dropout, recurrent_dropout = self.lstm_dropout, name='ConvLSTM2D_2', kernel_regularizer = l2(self.weight_decay), recurrent_regularizer = l2(self.weight_decay))(frames_diff_cnn)
            elif self.lstm_type == 'asepconv':    
                frames_diff_lstm = AttenSepConvLSTM2D(filters = 64, kernel_size = (3, 3), padding = 'same', return_sequences = False, dropout = self.lstm_dropout, recurrent_dropout = self.lstm_dropout, name = 'AttenSepConvLSTM2D_2', kernel_regularizer = l2(self.weight_decay), recurrent_regularizer = l2(self.weight_decay))(frames_diff_cnn)
            elif self.lstm_type == '3dconv':
                frames_diff_lstm = conv3d_block(frames_diff_cnn, 'frames_diff_3d_conv_block')(frames_diff_cnn)
            else:
                raise Exception("lstm type not recognized!")

            frames_diff_lstm = BatchNormalization(axis = -1)(frames_diff_lstm)
        
        if frames:
            frames_lstm = MaxPooling2D((2,2))(frames_lstm)
            x1 = LeakyReLU(alpha=0.1)(frames_lstm)
        
        if differences:
            frames_diff_lstm = MaxPooling2D((2,2))(frames_diff_lstm)
            x2 = Activation("sigmoid")(frames_diff_lstm)
    
        if self.input_mode == InputMode.BOTH:
            x = Multiply()([x1, x2])
        elif self.input_mode == InputMode.ONLY_FRAMES:
            x = x1
        elif self.input_mode == InputMode.ONLY_DIFFERENCES:
            x = x2
        
        x = Flatten()(x)
        x = Dense(64)(x)
        x = LeakyReLU(alpha = 0.1)(x)
        x = Dense(16)(x)
        x = LeakyReLU(alpha = 0.1)(x)
        x = Dropout(self.dense_dropout, seed = self.seed)(x)
        predictions = Dense(1, activation='sigmoid')(x)
    
        if self.input_mode == InputMode.BOTH:
            model = Model(inputs = [frames_input, frames_diff_input], outputs = predictions)
        elif self.input_mode == InputMode.ONLY_FRAMES:
            model = Model(inputs = frames_input, outputs = predictions)
        elif self.input_mode == InputMode.ONLY_DIFFERENCES:
            model = Model(inputs = frames_diff_input, outputs = predictions)

        model.load_weights("./controllers/neural_network/trained_model/rwf2000_model")
        return model

    def predict(self, data: object):
        return self.model.predict([data])
