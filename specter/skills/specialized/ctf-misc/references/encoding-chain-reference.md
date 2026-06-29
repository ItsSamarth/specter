# Encoding Chain Identification and Decoding

## Encoding Identification Features

| Encoding | Feature | Example |
|------|------|------|
| Base64 | `A-Za-z0-9+/=`, length % 4 | `TnNTY1RmLnBocA==` |
| Base32 | `A-Z2-7=`, length % 8 | `OBZHK5DFN2A====` |
| Base16 | `0-9A-F`, even length | `4E535354662E706870` |
| URL encoding | `%XX` | `%2F%61%64%6D%69%6E` |
| HTML entity | `&#xNNN;` or `&#NNN;` | `&#x3C;script&#x3E;` |
| Unicode | `\uXXXX` or `\UXXXXXXXX` | `\u003c\u0073\u0063` |
| Hex (Python) | `\xNN` | `\x4e\x53\x53\x54` |
| ROT13 | letter substitution, Caesar | `axzc` → `nmp` |
| Morse | `.` `-` `/` combination | `.-/-.../-.-.` |
| Binary | `01` array | `01001101` |

## Common Encoding Chains

### 1. Simple Chain
```
Hex → Base64 → URL encoding
```

### 2. Binary Family
```
Binary → ASCII
Octal → ASCII
Hex → ASCII
```

### 3. Browser Family
```
HTML entity → URL encoding → Base64
```

### 4. Special Encodings
```
Brainfuck (`><+-.,[]`)
Ook! (`Ook. Ook?`)
Hex → Ook! → Brainfuck
```

## Automatic Decoding Script

```python
import base64, binascii, urllib.parse, html

def auto_decode(data, max_iter=10):
    """Automatically attempt multi-layer decoding"""
    result = data
    for _ in range(max_iter):
        changed = False
        original = result

        # URL decode
        try:
            result = urllib.parse.unquote(result)
            if result != original:
                changed = True
        except:
            pass

        # HTML entity decode
        try:
            result = html.unescape(result)
            if result != original:
                changed = True
        except:
            pass

        # Base64 decode
        try:
            result = base64.b64decode(result).decode('utf-8')
            if result != original:
                changed = True
        except:
            try:
                result = base64.b64decode(result + '==').decode('utf-8')
                if result != original:
                    changed = True
            except:
                pass

        # Hex decode
        try:
            if all(c in '0123456789abcdefABCDEF' for c in result.replace('%', '')):
                result = bytes.fromhex(result.replace('%', '')).decode('utf-8')
                if result != original:
                    changed = True
        except:
            pass

        # ROT13
        try:
            result = original.encode().translate(bytes.maketrans(
                b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                b'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
            )).decode()
            if result != original:
                changed = True
        except:
            pass

        if not changed:
            break

    return result
```

## QR Code Decoding

```python
from PIL import Image
import zbarlight

def decode_qr(image_path):
    """Decode QR code"""
    image = Image.open(image_path)
    codes = zbarlight.scan_codes(['qrcode'], image)
    return codes
```

## Audio Steganography (Least Significant Bit)

```python
def extract_lsb_wav(wav_path):
    """Extract LSB steganography data from WAV"""
    import wave, struct
    with wave.open(wav_path, 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        binary = ''
        for byte in frames:
            binary += str(byte & 1)
    # One character per 8 bits
    result = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            result += chr(int(byte, 2))
    return result
```

## Image Steganography

```python
from PIL import Image

def extract_lsb_png(image_path):
    """Extract LSB steganography from PNG"""
    img = Image.open(image_path)
    pixels = list(img.getdata())
    binary = ''
    for pixel in pixels:
        if isinstance(pixel, tuple):
            for channel in pixel[:3]:
                binary += str(channel & 1)
        else:
            binary += str(pixel & 1)
    # One character per 8 bits
    result = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            result += chr(int(byte, 2))
    return result
```
