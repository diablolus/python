from tensorflow.keras.layers import Input,LSTM,Dense
from tensorflow.keras.models import Model

import pandas as pd
import numpy as np

class Seq2Seq:
    def __init__(self):
        self.N_UNITS = 256
        self.BATCH_SIZE = 32
        self.EPOCH = 600
        self.NUM_SAMPLES = 1000  #屬性
        
        self.INUPT_LENGTH = 0
        self.OUTPUT_LENGTH = 0
        self.INPUT_FEATURE_LENGTH = 0
        self.OUTPUT_FEATURE_LENGTH = 0

    def Create_Model(self, n_input,n_output,n_units):
        #训练阶段
        encoder_input = Input(shape = (None, n_input))
        encoder = LSTM(n_units, return_state=True)
        _,encoder_h,encoder_c = encoder(encoder_input)
        encoder_state = [encoder_h,encoder_c]
    
        decoder_input = Input(shape = (None, n_output))
        decoder = LSTM(n_units,return_sequences=True, return_state=True)
        decoder_output, _, _ = decoder(decoder_input,initial_state=encoder_state)
    
        decoder_dense = Dense(n_output,activation='softmax')
        decoder_output = decoder_dense(decoder_output)
    
        model = Model([encoder_input,decoder_input],decoder_output)
    
        encoder_infer = Model(encoder_input,encoder_state)
        
        decoder_state_input_h = Input(shape=(n_units,))
        decoder_state_input_c = Input(shape=(n_units,))    
        decoder_state_input = [decoder_state_input_h, decoder_state_input_c]#上个时刻的状态h,c   
        
        decoder_infer_output, decoder_infer_state_h, decoder_infer_state_c = decoder(decoder_input,initial_state=decoder_state_input)
        decoder_infer_state = [decoder_infer_state_h, decoder_infer_state_c]#当前时刻得到的状态
        decoder_infer_output = decoder_dense(decoder_infer_output)#当前时刻的输出
        decoder_infer = Model([decoder_input]+decoder_state_input,[decoder_infer_output]+decoder_infer_state)
        
        return model, encoder_infer, decoder_infer

    def Predict_Chinese(self, source, encoder_inference, decoder_inference, n_steps, features, target_dict, target_dict_reverse):
        state = encoder_inference.predict(source)
    
        predict_seq = np.zeros((1,1,features))
        predict_seq[0,0,target_dict['\t']] = 1
    
        output = ''
    
        for i in range(n_steps):#n_steps为句子最大长度
            yhat,h,c = decoder_inference.predict([predict_seq]+state)
            char_index = np.argmax(yhat[0,-1,:])
            char = target_dict_reverse[char_index]
            output += char
            state = [h,c]
            predict_seq = np.zeros((1,1,features))
            predict_seq[0,0,char_index] = 1
            if char == '\n':
                break
            
        return output

    def Load_Data(self):
        data_path = 'translation2019zh_train.json'
        
        df = pd.read_json(data_path, lines=True).iloc[:self.NUM_SAMPLES,:,]
        df.columns=['inputs','targets']
        
        df['targets'] = df['targets'].apply(lambda x: '\t'+x+'\n')
        
        input_texts = df.inputs.values.tolist()
        target_texts = df.targets.values.tolist()
    
        input_characters = sorted(list(set(df.inputs.unique().sum())))
        target_characters = sorted(list(set(df.targets.unique().sum())))
        
        return (input_texts, target_texts, input_characters, target_characters)

    def Training_Models(self, input_texts, target_texts, input_characters, target_characters):
        
        self.INUPT_LENGTH = max([len(i) for i in input_texts])
        self.OUTPUT_LENGTH = max([len(i) for i in target_texts])
        self.INPUT_FEATURE_LENGTH = len(input_characters)
        self.OUTPUT_FEATURE_LENGTH = len(target_characters)

        
        encoder_input = np.zeros((self.NUM_SAMPLES, self.INUPT_LENGTH, self.INPUT_FEATURE_LENGTH))
        decoder_input = np.zeros((self.NUM_SAMPLES, self.OUTPUT_LENGTH, self.OUTPUT_FEATURE_LENGTH))
        decoder_output = np.zeros((self.NUM_SAMPLES, self.OUTPUT_LENGTH, self.OUTPUT_FEATURE_LENGTH))
        
        input_dict = {char:index for index,char in enumerate(input_characters)}
        input_dict_reverse = {index:char for index,char in enumerate(input_characters)}
        target_dict = {char:index for index,char in enumerate(target_characters)}
        target_dict_reverse = {index:char for index,char in enumerate(target_characters)}
        
        for seq_index,seq in enumerate(input_texts):
            for char_index, char in enumerate(seq):
                encoder_input[seq_index,char_index,input_dict[char]] = 1
                
        for seq_index,seq in enumerate(target_texts):
            for char_index,char in enumerate(seq):
                decoder_input[seq_index,char_index,target_dict[char]] = 1.0
                if char_index > 0:
                    decoder_output[seq_index,char_index-1,target_dict[char]] = 1.0
             

        model_train, encoder_infer, decoder_infer = self.Create_Model(self.INPUT_FEATURE_LENGTH, self.OUTPUT_FEATURE_LENGTH, self.N_UNITS)
        model_train.compile(optimizer='rmsprop', loss='categorical_crossentropy')    
        model_train.fit([encoder_input,decoder_input],decoder_output,batch_size=self.BATCH_SIZE,epochs=self.EPOCH,validation_split=0.2)
        
        return (input_dict_reverse, target_dict_reverse, encoder_infer, decoder_infer , target_dict, encoder_input)


if __name__== "__main__":
    seq2seq = Seq2Seq()

    tuple1 = seq2seq.Load_Data()
    tuple2 = seq2seq.Training_Models(tuple1[0],tuple1[1],tuple1[2],tuple1[3])

    input_texts = tuple1[0]
    target_texts = tuple1[1]
    
    target_dict_reverse = tuple2[1] 
    encoder_infer = tuple2[2]
    decoder_infer = tuple2[3]
    target_dict = tuple2[4]
    encoder_input = tuple2[5]
    
    for i in range(20,120):
        test = encoder_input[i:i+1,:,]#i:i+1保持数组是三维
        #test = ["i love bird"]
        out = seq2seq.Predict_Chinese(test,encoder_infer,decoder_infer,seq2seq.OUTPUT_LENGTH,seq2seq.OUTPUT_FEATURE_LENGTH, target_dict, target_dict_reverse)
        #print(input_texts[i],'\n---\n',target_texts[i],'\n---\n',out)
        print(input_texts[i])
        print(out)
