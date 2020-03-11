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

![Screenshot_2020-03-11_19-08-48](https://user-images.githubusercontent.com/54184905/76455095-7ed90080-63e6-11ea-9161-ed586310a162.png)

(Yanlış resim ve 0 etiketi)

![Screenshot_2020-03-11_19-09-43](https://user-images.githubusercontent.com/54184905/76455103-80a2c400-63e6-11ea-8731-387f9e0e8caf.png)

(Doğru resim ve 1 etiketi)

# Algoritmaların Eğitimi

* Her iki bölümde kod satırları boyunca kendilerini eğitirler.

![Screenshot_2020-03-11_19-12-58](https://user-images.githubusercontent.com/54184905/76455716-03c41a00-63e7-11ea-9c22-6c0e9f7e0f8a.png)

(D eğitimi, G den gelen ve orjinal resimlerle bir orantı kurarak ağırlık verir ve biz bu ağırlıkları loss fonksiyonu ile performans kontrolü yapariz)

![Screenshot_2020-03-11_19-15-42](https://user-images.githubusercontent.com/54184905/76455724-058ddd80-63e7-11ea-87f1-281aac7b11e7.png)

(G eğitimi, D den gelen ağırlıklar ile yeni resim çizer ve sonra tekrardan D ye iletir.)
