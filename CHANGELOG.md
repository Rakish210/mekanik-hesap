# Changelog

## 1.0.0

- gas/gaz modulleri birlestirildi: tek kaynak `mekanik_hesap/gaz/`.
  `mekanik_hesap.gas` geriye uyumluluk shim olarak korundu.
- KATALOG.md: Dogalgaz satiri tek modul olarak guncellendi.
- README.md: Ilk kanitli modul referansi `gaz/` olarak duzeltildi.
- CI/CD: GitHub Actions test workflow eklendi (.github/workflows/tests.yml).
- Versiyon 0.1.0 -> 1.0.0.

## 0.1.0

- 126 hesap, 15 kategori (`KATALOG.md`).
- 196 test (`tests/`, `unittest discover` ile yesil).
- Paket dagitimi: `pyproject.toml` (setuptools), `pip install -e .`.
