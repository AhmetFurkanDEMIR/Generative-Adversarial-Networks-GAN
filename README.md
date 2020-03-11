# Generative Adversarial Networks-GAN 

* Ressimler ile öğrenip yeni resimler oluşturan sinir ağları
* G (Generator) = üretici
* D (Discriminator) = ayırt edici

# Generative

* input olarak rastgele bir gürültü alır çıktı olarak bir ressim verir.

![Screenshot_2020-03-11_19-08-00](https://user-images.githubusercontent.com/54184905/76454566-f35f6f80-63e5-11ea-9108-605b8028a0c3.png)

# Adversarial

* G ye rakip olarak görülür. D gerçek resimlere ulaşabilir ama G ulaşamaz, D gerçek ve G nin ürettiği resimleri alıp yorumlar ve bir çıktı verir.
* Eğer tahmin doğru ise 1 e yaklaşır tahmin yanlış ise 0 a yaklaşır.
* G den üretilen resimleri alır ve nerede hata yaptığını G ye söyler.
