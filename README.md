# 🤖 Akıllı Koridor Asistanı Robotu

Merhabalar! Bu proje, Webots simülasyon ortamında geliştirilmiş otonom bir mobil robot projesidir. Temel amacı, akıllı bina koridorlarında güvenli geçişi sağlamak ve aydınlatma kaynaklı enerji israfını önlemektir.

## 🎯 Projenin Amacı ve Çözdüğü Problemler
Geleneksel koridor aydınlatmaları ve yetersiz hareket sensörleri büyük enerji israfına yol açar. Bu robot:
- Koridorlarda aktif devriye gezerek aydınlatmayı sadece gerektiğinde kullanır (**%20+ enerji tasarrufu** sağlar).
- Engelleri otonom olarak algılar ve çarpışmadan güvenli bir trafik akışı oluşturur.

## ⚙️ Robotun Çalışma Mantığı
1. **Düz İlerleme:** Robot engelsiz alanda sabit hızla ilerler.
2. **Engelden Kaçınma:** Üzerindeki mesafe sensörleri (kızılötesi/ultrasonik) ile önüne çıkan nesneleri algılar ve manevra yapar.
3. **Görev Tamamlama:** Koridor sonundaki "Aydınlatma Bölgesi"ne ulaştığında bunu algılar, motorları durdurur ve düşük güç moduna geçer.

## 🛠️ Kullanılan Teknolojiler
- **Simülasyon:** Webots
- **Yazılım Dili:** Python / C++
- **Donanım (Simüle Edilen):** Mesafe sensörleri, zemin algılama sensörü, diferansiyel sürüşlü mobil platform.

## 🚀 Nasıl Çalıştırılır?
1. Bilgisayarınıza [Webots](https://cyberbotics.com/) simülatörünü kurun.
2. Bu projedeki `.wbt` (Dünya) ve `.py` (Kontrolcü) dosyalarını indirin.
3. Webots programında `File > Open World` diyerek dünyayı açın.
4. Simülasyonu başlatın (Play) ve robotun otonom hareketini izleyin!

Yazar: Hasan Köstek
