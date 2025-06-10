
# 🖼️ Image Encryption Tool

This is a simple Python-based **Image Encryption and Decryption Tool** that supports multiple encryption techniques like:

- XOR Encryption
- Pixel Swap Encryption
- Mathematical Encryption
- Channel Shift Encryption

It's great for educational purposes and beginner-level cryptography with images.

---

## 📦 Requirements

Before you run this tool, make sure you have Python installed. Then install the required libraries:

```bash
pip install pillow numpy
```

---

## 🚀 How to Run

### 1. Clone or Download the Script

Save the script as `imageEncryptor.py` or clone your project folder.

### 2. Run the Script

You can run the tool in two modes:

#### 🔹 Interactive Mode (For Manual Use)

```bash
python imageEncryptor.py
```

Then follow the on-screen menu:

- Choose to encrypt or decrypt
- Select method (`xor`, `swap`, `math`, or `channel`)
- Provide image paths and output paths
- You can also change the encryption key

#### 🔹 Demo Mode (For Automatic Testing)

Demo mode automatically:
- Creates a test image
- Encrypts and decrypts it using all 4 methods
- Saves output files for you to review

To run demo mode:

```bash
python imageEncryptor.py
```

Then choose `2` when prompted:

```
Choose mode:
1. Interactive mode
2. Demo mode
Enter choice (1 or 2): 2
```

---

## 🔐 Encryption Methods Explained

| Method    | Description |
|-----------|-------------|
| `xor`     | Applies XOR operation using a random key |
| `swap`    | Shuffles pixel positions using a reproducible pattern |
| `math`    | Modifies pixel values mathematically |
| `channel` | Rotates color channels (RGB → GBR → BRG) |

All methods are reversible using the **same key**.

---

## 📝 Notes

- Images must be in a format that supports color (RGB), such as `.png` or `.jpg`.
- Encryption and decryption must be done using the **same method and key**.
- The tool uses `random.seed(key)` to ensure repeatable encryption/decryption.

---

## 📁 Output Files

Encrypted and decrypted images will be saved with names like:

- `test_encrypted_xor.png`
- `test_decrypted_xor.png`

---

## 👨‍💻 Author

Made with 💡 by **You!**
