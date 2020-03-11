from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Activation, Reshape
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.python.keras.layers import UpSampling2D, Conv2D
from tensorflow.python.keras.layers import ELU
from tensorflow.python.keras.layers import Flatten, Dropout
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.datasets import mnist

import os #klasör işlemi
from PIL import Image #python resim kütüphanesi
from helper import * #resim birleştirme fonksiyonu ve print işlemi


def generator(input_dim=100, units=1024, activation='relu'): #üretici (resim), ilk paremetre gürültü, ikinci parametre ilk leyer daki nöron sayısı, 3. parametre aktivasyon fonksiyonu
    model = Sequential() #ardışık model
    model.add(Dense(input_dim=input_dim, units=units)) #Dense layer oluşturduk, 1.parametre verdiğimiz gürültü(rastgele sayı),2.parametre nöron sayısı
    model.add(BatchNormalization()) #normalleştirme yöntemi (performansımızı arttırır)
    model.add(Activation(activation)) # aktivasyon fonksiyonu
    model.add(Dense(128*7*7)) # layer içindeki nöron sayısı
    model.add(BatchNormalization())
    model.add(Activation(activation))
    model.add(Reshape((7, 7, 128), input_shape=(128*7*7,))) #convolutional sinir ağı girişi için tekrar düzenledik
    model.add(UpSampling2D((2, 2))) #matrisi 14x14x128 şeklinde düzenledik(derinlik etkilenmez)
    model.add(Conv2D(64, (5, 5), padding='same')) #conVent oluşturup filitre boyutu belirliyoruz (64 filite 5,5 boyutunda) boyutun küçülmesini engelleriz
    model.add(BatchNormalization())
    model.add(Activation(activation))
    model.add(UpSampling2D((2, 2)))
    model.add(Conv2D(1, (5, 5), padding='same')) #derinliği filtre etkiler
    model.add(Activation('tanh')) #aktivasyon fonksiyonu ([-1,1] aralığında değer döndürür bunlarla pixelleri renklendiririz)
    print(model.summary()) #model özeti.
    return model


def discriminator(input_shape=(28, 28, 1), nb_filter=64): #kontrol edici fonksiyon, 1. parametre resmin boyutu (28,28,renkliyse 3 değilse 1), 2.parametre filtre 64 tane
    model = Sequential() #ardışık model oluşturduk, resmi alıp sinir ağının sonunda değer elde ederiz.
    model.add(Conv2D(nb_filter, (5, 5), strides=(2, 2), padding='same', input_shape=input_shape)) 
    #convnet oluşturduk, 1.parametre filitre, 2. parametre  boyutu, 3. parametre filitrelerin resimde nasıl kayacağı (2 pixel kayacak), 4. parametre boyutu korur resmin etrafına 0 lar ekler,5. parametre çıkış boyutu

    model.add(BatchNormalization()) #normalleştirme
    model.add(ELU()) #aktivasyon fonksiyonu (elu)
    model.add(Conv2D(2*nb_filter, (5, 5), strides=(2, 2))) #2 katı filitre ile yeni layer. boyut 5x5x128 e düşer
    model.add(BatchNormalization())
    model.add(ELU())
    model.add(Flatten()) #düzleştirme işlevi Dense layer eklemek için
    model.add(Dense(4*nb_filter)) # nöron sayısı
    model.add(BatchNormalization())
    model.add(ELU())
    model.add(Dropout(0.5)) # ezber yapmasını engeller.
    model.add(Dense(1)) # output sinir hücresi, çıkış
    model.add(Activation('sigmoid')) #aktivasyon fonksiyonu gelen değer [0,1] arasında
    print(model.summary()) #model özeti
    return model


batch_size = 32 # eğitim esnasında tek dögü ile alacağımız resim sayısı
num_epoch = 5 # tüm data setin eğitimden bir kez geçmesine denir
learning_rate = 0.0002 #optimazsyon yaparken loss değerini düşürürüz
image_path = 'images/' #klasöre resim oluşturma.

if not os.path.exists(image_path):
    os.mkdir(image_path) #klasör oluşturma

# gerçek resimlerin pixel değeri 0,1 arası
# sahte resimler 0,255 arasında olacak, böylece ayrımı yapabileceğiz

def train(): # eğitim
    (x_train, y_train), (_, _) = mnist.load_data() # 1. parametre test ve eğitim verisi, 2.parametre etiketler (G de ihtiyaç yok) 
    # pixel ayarları (64,65 açıklama)
    x_train = (x_train.astype(np.float32) - 127.5) / 127.5
    x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)

    g = generator() # çağırma işlemi
    d = discriminator()

    optimize = Adam(lr=learning_rate, beta_1=0.5) #optimizasyon algoritması belirleme.
    d.trainable = True # eğitilebilir olduğunu belirleriz
    d.compile(loss='binary_crossentropy', #loss fonksiyonu (performans ölçmek)
              metrics=['accuracy'], #isabet oranı
              optimizer=optimize) # eğitim gerçekleştirme

    d.trainable = False # eğitilmeyecek
    dcgan = Sequential([g, d]) #GANs oluşumu, D eğitilmeyecek
    dcgan.compile(loss='binary_crossentropy',
                  metrics=['accuracy'],
                  optimizer=optimize)

    num_batches = x_train.shape[0] // batch_size # resim sayısı / 1 dögüde girecek resim sayısı
    gen_img = np.array([np.random.uniform(-1, 1, 100) for _ in range(49)]) # rastgele gürültü oluşturma
    y_d_true = [1] * batch_size #grçekse etiket 1
    y_d_gen = [0] * batch_size # sahteyse etiket 0
    y_g = [1] * batch_size # g için etiket

    for epoch in range(num_epoch):
        
        for i in range(num_batches): #resimleri eğitiyoruz

            x_d_batch = x_train[i*batch_size:(i+1)*batch_size] # besleme için batch (32 resim)
            x_g = np.array([np.random.normal(0, 0.5, 100) for _ in range(batch_size)]) # G için gürültü oluşturma
            x_d_gen = g.predict(x_g) #resim üretme (32 adet) eğitim için

            d_loss = d.train_on_batch(x_d_batch, y_d_true) # D eğitimi (batc üzerinden,(gerçek_resim,sahte_resim))
            d_loss = d.train_on_batch(x_d_gen, y_d_gen) #etiketleri

            g_loss = dcgan.train_on_batch(x_g, y_g) # G eğitimi dcgan üzerinden (input olarak gürültü veririz)
            show_progress(epoch, i, g_loss[0], d_loss[0], g_loss[1], d_loss[1]) # helper fonksiyonundaki bilgiler bölümü
            print("****",num_batches)

        image = combine_images(g.predict(gen_img)) #resimleri birleştirip tek resim yaptık
        image = image * 127.5 + 127.5 # değerleri 0,255 arasına genişlettik
        Image.fromarray(image.astype(np.uint8)).save(image_path + "%03d.png" % (epoch)) #resim kaydetme



if __name__ == '__main__':
    train() #fonk çağırma
