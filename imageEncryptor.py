import numpy as np
from PIL import Image
import random
import os

class ImageEncryptor:
    def __init__(self, key=12345):
        """
        Initialize the Image Encryptor with a seed key for reproducible encryption/decryption
        """
        self.key = key
        
    def load_image(self, image_path):
        """Load an image and convert it to numpy array"""
        try:
            img = Image.open(image_path)
            # Convert to RGB if not already
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return np.array(img)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def save_image(self, img_array, output_path):
        """Save numpy array as image"""
        try:
            img = Image.fromarray(img_array.astype(np.uint8))
            img.save(output_path)
            print(f"Image saved to: {output_path}")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def xor_encryption(self, img_array, encrypt=True):
        """
        XOR encryption/decryption - same operation for both
        """
        # Create a reproducible random key based on image dimensions and seed
        random.seed(self.key)
        height, width, channels = img_array.shape
        
        # Generate random key array
        key_array = np.random.randint(0, 256, size=(height, width, channels), dtype=np.uint8)
        
        # XOR operation
        result = img_array ^ key_array
        return result
    
    def pixel_swap_encryption(self, img_array, encrypt=True):
        """
        Encrypt by swapping pixel positions based on a pattern
        """
        result = img_array.copy()
        height, width, channels = img_array.shape
        
        # Create reproducible shuffle pattern
        random.seed(self.key)
        
        # Create list of all pixel positions
        positions = [(i, j) for i in range(height) for j in range(width)]
        
        if encrypt:
            # Shuffle positions for encryption
            shuffled_positions = positions.copy()
            random.shuffle(shuffled_positions)
            
            # Create mapping
            for original_pos, new_pos in zip(positions, shuffled_positions):
                result[new_pos[0], new_pos[1]] = img_array[original_pos[0], original_pos[1]]
        else:
            # Reverse the shuffle for decryption
            shuffled_positions = positions.copy()
            random.shuffle(shuffled_positions)
            
            # Reverse mapping
            for original_pos, shuffled_pos in zip(positions, shuffled_positions):
                result[original_pos[0], original_pos[1]] = img_array[shuffled_pos[0], shuffled_pos[1]]
        
        return result
    
    def mathematical_encryption(self, img_array, encrypt=True):
        """
        Apply mathematical operations to pixel values
        """
        result = img_array.copy().astype(np.int32)
        
        if encrypt:
            # Encryption: Add key value and apply modulo
            result = (result + self.key % 256) % 256
            # Additional scrambling based on position
            for i in range(result.shape[0]):
                for j in range(result.shape[1]):
                    result[i, j] = (result[i, j] + (i + j) * 13) % 256
        else:
            # Decryption: Reverse the operations
            for i in range(result.shape[0]):
                for j in range(result.shape[1]):
                    result[i, j] = (result[i, j] - (i + j) * 13) % 256
            result = (result - self.key % 256) % 256
        
        return result.astype(np.uint8)
    
    def channel_shift_encryption(self, img_array, encrypt=True):
        """
        Shift color channels (RGB -> GBR -> BRG, etc.)
        """
        result = img_array.copy()
        
        if encrypt:
            # Shift channels: R->G, G->B, B->R
            result[:, :, 0] = img_array[:, :, 2]  # R = B
            result[:, :, 1] = img_array[:, :, 0]  # G = R  
            result[:, :, 2] = img_array[:, :, 1]  # B = G
        else:
            # Reverse shift: R->B, G->R, B->G
            result[:, :, 0] = img_array[:, :, 1]  # R = G
            result[:, :, 1] = img_array[:, :, 2]  # G = B
            result[:, :, 2] = img_array[:, :, 0]  # B = R
        
        return result
    
    def encrypt_image(self, image_path, output_path, method='xor'):
        """
        Encrypt an image using specified method
        """
        img_array = self.load_image(image_path)
        if img_array is None:
            return False
        
        print(f"Encrypting image using {method} method...")
        
        if method == 'xor':
            encrypted = self.xor_encryption(img_array, encrypt=True)
        elif method == 'swap':
            encrypted = self.pixel_swap_encryption(img_array, encrypt=True)
        elif method == 'math':
            encrypted = self.mathematical_encryption(img_array, encrypt=True)
        elif method == 'channel':
            encrypted = self.channel_shift_encryption(img_array, encrypt=True)
        else:
            print("Unknown encryption method!")
            return False
        
        return self.save_image(encrypted, output_path)
    
    def decrypt_image(self, image_path, output_path, method='xor'):
        """
        Decrypt an image using specified method
        """
        img_array = self.load_image(image_path)
        if img_array is None:
            return False
        
        print(f"Decrypting image using {method} method...")
        
        if method == 'xor':
            decrypted = self.xor_encryption(img_array, encrypt=False)
        elif method == 'swap':
            decrypted = self.pixel_swap_encryption(img_array, encrypt=False)
        elif method == 'math':
            decrypted = self.mathematical_encryption(img_array, encrypt=False)
        elif method == 'channel':
            decrypted = self.channel_shift_encryption(img_array, encrypt=False)
        else:
            print("Unknown decryption method!")
            return False
        
        return self.save_image(decrypted, output_path)

def main():
    """
    Main function to demonstrate the image encryption tool
    """
    # Initialize encryptor with a key
    encryptor = ImageEncryptor(key=54321)
    
    print("=== Image Encryption Tool ===")
    print("Available methods: xor, swap, math, channel")
    print()
    
    while True:
        print("\nOptions:")
        print("1. Encrypt image")
        print("2. Decrypt image")
        print("3. Change encryption key")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            image_path = input("Enter path to image to encrypt: ").strip()
            if not os.path.exists(image_path):
                print("Image file not found!")
                continue
            
            method = input("Enter encryption method (xor/swap/math/channel): ").strip().lower()
            if method not in ['xor', 'swap', 'math', 'channel']:
                print("Invalid method!")
                continue
            
            output_path = input("Enter output path for encrypted image: ").strip()
            if not output_path:
                base_name = os.path.splitext(image_path)[0]
                output_path = f"{base_name}_encrypted_{method}.png"
            
            success = encryptor.encrypt_image(image_path, output_path, method)
            if success:
                print(f"Image encrypted successfully!")
        
        elif choice == '2':
            image_path = input("Enter path to encrypted image: ").strip()
            if not os.path.exists(image_path):
                print("Image file not found!")
                continue
            
            method = input("Enter decryption method (xor/swap/math/channel): ").strip().lower()
            if method not in ['xor', 'swap', 'math', 'channel']:
                print("Invalid method!")
                continue
            
            output_path = input("Enter output path for decrypted image: ").strip()
            if not output_path:
                base_name = os.path.splitext(image_path)[0]
                output_path = f"{base_name}_decrypted.png"
            
            success = encryptor.decrypt_image(image_path, output_path, method)
            if success:
                print(f"Image decrypted successfully!")
        
        elif choice == '3':
            try:
                new_key = int(input("Enter new encryption key (integer): "))
                encryptor.key = new_key
                print(f"Encryption key changed to: {new_key}")
            except ValueError:
                print("Invalid key! Please enter an integer.")
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

# Example usage for testing
def demo_encryption():
    """
    Demo function showing how to use the encryption tool
    """
    # Create a simple test image if none exists
    try:
        # Create a simple gradient image for testing
        test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        for i in range(100):
            for j in range(100):
                test_img[i, j] = [i * 2, j * 2, (i + j)]
        
        Image.fromarray(test_img).save("test_image.png")
        print("Created test image: test_image.png")
        
        # Initialize encryptor
        encryptor = ImageEncryptor(key=12345)
        
        # Test all encryption methods
        methods = ['xor', 'swap', 'math', 'channel']
        
        for method in methods:
            print(f"\nTesting {method} encryption...")
            
            # Encrypt
            encrypted_path = f"test_encrypted_{method}.png"
            encryptor.encrypt_image("test_image.png", encrypted_path, method)
            
            # Decrypt
            decrypted_path = f"test_decrypted_{method}.png"
            encryptor.decrypt_image(encrypted_path, decrypted_path, method)
            
            print(f"Files created: {encrypted_path}, {decrypted_path}")
        
        print("\nDemo completed! Check the generated files.")
        
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Interactive mode")
    print("2. Demo mode")
    
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == '2':
        demo_encryption()
    else:
        main()