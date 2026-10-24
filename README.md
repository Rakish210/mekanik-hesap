# mekanik-hesap

Mekanik tesisat hesap kutuphanesi: TTT/HBK/ML/kesif hesap motoru + test.

## Kapsam

- Isitma, iklimlendirme, havalandirma, sihhi tesisat, gunes, havuz,
  yangin, dogalgaz, asansor, basincli hava, medikal gaz, temiz oda,
  yardimci hesaplar, elektrik (tesisat ara yuz hesaplari).
- Tam liste: `KATALOG.md` (126 hesap, 15 kategori).
- Ilk kanitli modul: `mekanik_hesap/gaz/` (TTT/HBK-hiz/isil-genlesme/konsol).

## Kurulum

```bash
pip install -e .
pip install -e ".[dev]"   # pytest ile calismak icin
```

## Hizli ornek

```python
from mekanik_hesap.gaz import sayac_secimi

print(sayac_secimi(6.1))  # G6
```

## Test

```bash
py -m unittest discover -s tests -v
pytest -q   # dev bagimliliklari kurulduysa
```

## Lisans

MIT. `LICENSE` dosyasina bakin.

## Katki kurali

1. Her modul, dayandigi standardi dosya basinda yazar
   (ornek: `TS EN 12831`, `TS 7363`). Bilinmeyen standart
   uydurulmaz; `[STANDART-TEYIT]` yazilir.
2. Site icerigi ve site kodu dosyaya girmez: harici sitelerden
   metin, tablo, formul blogu kopyalanmaz. Sadece hesap adi
   listelenir; formul, bagimsiz kaynaktan (standart/kaynak kitap)
   yeniden yazilir.
3. Her hesap fonksiyonu: docstring + birim + bir test.
