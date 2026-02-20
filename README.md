# 🔐 Image Cryptography in Python

A simple image encryption and decryption project using **XOR-based pixel encryption**, **pixel shuffling**, and **LSB steganographic key hiding** — all built with Python's Pillow library.

---

## 📖 Overview

This project encrypts images by combining three techniques:

1. **XOR Encryption** — Each pixel's RGB values are XORed with a randomly generated 8-bit key.
2. **Pixel Shuffling** — Pixels are permuted using a seeded shuffle for additional obfuscation.
3. **LSB Key Hiding** — The key is embedded into the first 8 pixels' blue channel LSB, so no external key storage is needed.

Decryption fully reverses the process to restore the original image.

---

## ✨ Features

- Random 8-bit key generation (1–255)
- Pixel-wise XOR encryption/decryption
- Seeded pixel shuffle for reproducible permutations
- Key hidden via LSB steganography — no external key file needed
- Supports any RGB image of any size
- Customizable output file names for both encrypted and decrypted images

---

## ⚙️ Algorithm

### Encryption Flow

```
Original Image
      │
      ▼
  XOR each pixel's RGB with key
      │
      ▼
  Shuffle pixels (seed = key)
      │
      ▼
  Hide key in LSB of first 8 blue pixels
      │
      ▼
  Save as Encrypted Image (PNG)
```

### Decryption Flow

```
Encrypted Image (PNG)
      │
      ▼
  Extract key from LSB of first 8 blue pixels
      │
      ▼
  Recreate shuffle permutation (seed = key)
      │
      ▼
  Unshuffle pixels
      │
      ▼
  XOR each pixel's RGB with key
      │
      ▼
  Save as Decrypted Image
```

---

## 🚀 Installation

**1. Clone the repository:**

```bash
git clone https://github.com/Hammail-Riaz/Image-Cryptography-Algorithm.git
```

**2. Install dependencies:**

```bash
pip install pillow
```

---

## 🛠️ Usage

```python
from image_cryptography import Image_Cryptography

img_crypto = Image_Cryptography()

# Encrypt an image
img_crypto.encrypt('input_image.png', save_name='encrypted_image.png')

# Decrypt an image
img_crypto.decrypt('encrypted_image.png', save_name='decrypted_image.png')
```

> **Note:** Always save encrypted images as **PNG** to preserve LSB data. Lossy formats like JPEG will destroy the hidden key.

---

## 🧪 Example

```python
img_crypto = Image_Cryptography()

img_crypto.encrypt('img.jpg', save_name='image_51.png')
img_crypto.decrypt('image_51.png', save_name='hamufile.jpg')
```

This produces `image_51.png` (encrypted) and `hamufile.jpg` (decrypted — visually identical to the original).

---

## 🔍 How It Works

### XOR Encryption
Each pixel's R, G, and B channel values are XORed with the same 8-bit key. XOR is self-inverse, so applying it twice with the same key restores the original values.

### Pixel Shuffling
After XOR, pixels are rearranged using `random.shuffle()` seeded with the key, producing a consistent permutation that can be reversed during decryption.

### LSB Key Hiding (Steganography)
The 8-bit key is stored one bit at a time in the least significant bit of the blue channel of the first 8 pixels. This causes imperceptible color changes while allowing full key recovery.

---

## ⚠️ Notes

- **Encrypted images must be saved as PNG** — JPEG compression corrupts LSB data and makes decryption impossible.
- The key space is only 8 bits (255 possible keys), making this **not suitable for production security use**.
- This project is intended for **educational purposes** to demonstrate basic image cryptography concepts.
- Works with any standard RGB image.

---

## 📦 Dependencies

| Package | Purpose |
|--------|---------|
| [Pillow](https://python-pillow.org/) | Image loading, manipulation, and saving |

---

## 📄 License

MIT License © 2026 Hammail Riaz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
