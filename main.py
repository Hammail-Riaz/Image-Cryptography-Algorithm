from PIL import Image
from random import seed, randint, shuffle

class Image_Cryptography:
    """
    Image_Cryptography implements a simple image encryption and decryption scheme using:
    
    Algorithm Flow:
    1. Generate a random 8-bit key (1-255).
    2. XOR each RGB pixel with the key to encrypt the image.
    3. Shuffle the pixels using a permutation generated from the key as a seed.
    4. Hide the key in the first 8 pixels (blue channel LSB) of the final shuffled image.
    5. Save the encrypted image.

    Decryption Flow:
    1. Extract the hidden key from the first 8 pixels' blue channel LSB.
    2. Recreate the same permutation using the key.
    3. Unshuffle the pixels to original order.
    4. XOR each pixel with the key to decrypt.
    5. Save the decrypted image.
    """

    def __init__(self):
        """Initialize the Image_Cryptography object with key and image placeholders."""
        self.key = None
        self.img = None

    def _generate_key(self):
        """Generate a random 8-bit key (1-255) for encryption."""
        self.key = randint(1, 255)

    def _hide_key(self, img):
        """
        Hide the 8-bit key in the first 8 pixels of the image's blue channel LSB.
        Only the least significant bit of each pixel's blue channel is modified.
        """
        pixels = img.load()
        width, height = img.size
        key_binary = format(self.key, '08b')  # convert key to 8-bit binary
        bit_index = 0

        for y in range(height):
            for x in range(width):
                if bit_index == 8:  # stop after 8 bits
                    return

                r, g, b = pixels[x, y]
                # Clear LSB and insert key bit
                new_blue = (b & 254) | int(key_binary[bit_index])
                pixels[x, y] = (r, g, new_blue)

                bit_index += 1

    def _extract_key(self, img):
        """
        Extract the hidden 8-bit key from the first 8 pixels of the image's blue channel LSB.
        Returns the decimal value of the extracted key.
        """
        pixels = img.load()
        width, height = img.size
        bits = []
        count = 0

        for y in range(height):
            for x in range(width):
                if count == 8:
                    break
                r, g, b = pixels[x, y]
                bits.append(str(b & 1))  # extract LSB
                count += 1
            if count == 8:
                break

        binary_key = ''.join(bits)
        return int(binary_key, 2)

    def _set_seed(self, key):
        """Set the random module seed using the key for reproducible shuffling."""
        seed(key)

    def encrypt(self, image_path, save_name=f"image_{randint(1, 100)}.png"):
        """
        Encrypt the image:
        1. Generate a key.
        2. XOR each pixel with the key.
        3. Shuffle pixels using permutation derived from key.
        4. Hide key in first 8 pixels' blue channel LSB.
        5. Save encrypted image.
        """
        self._generate_key()
        self._set_seed(self.key)

        self.img = Image.open(image_path)
        pixels = self.img.load()
        width, height = self.img.size

        # XOR each pixel with key
        rgb_pixels = [(r ^ self.key, g ^ self.key, b ^ self.key)
                      for y in range(height) for x in range(width)
                      for r, g, b in [pixels[x, y]]]

        # Shuffle pixels
        permutation = list(range(len(rgb_pixels)))
        shuffle(permutation)
        shuffled = [rgb_pixels[i] for i in permutation]

        # Create new image and hide key
        new_img = Image.new("RGB", self.img.size)
        new_img.putdata(shuffled)
        self._hide_key(new_img)

        # Save encrypted image with random name
        new_img.save(save_name)

    def decrypt(self, image_path, save_name = "image_decrypted.png"):
        """
        Decrypt the image:
        1. Extract key from first 8 blue pixels LSB.
        2. Set seed for reproducible shuffling.
        3. Unshuffle pixels.
        4. XOR each pixel with key.
        5. Save decrypted image as 'image_decrypted.png'.
        """
        self.img = Image.open(image_path)
        self.key = self._extract_key(self.img)
        self._set_seed(self.key)

        original_pixels = self.img.load()
        width, height = self.img.size

        # Flatten pixels
        rgb_pixels = [original_pixels[x, y] for y in range(height) for x in range(width)]

        # Unshuffle
        permutation = list(range(len(rgb_pixels)))
        shuffle(permutation)
        unshuffled = [0] * len(rgb_pixels)
        for i, idx in enumerate(permutation):
            unshuffled[idx] = rgb_pixels[i]

        # XOR to decrypt
        decrypted = [(r ^ self.key, g ^ self.key, b ^ self.key) for r, g, b in unshuffled]

        # Save decrypted image
        new_img = Image.new("RGB", self.img.size)
        new_img.putdata(decrypted)
        new_img.save(save_name)
