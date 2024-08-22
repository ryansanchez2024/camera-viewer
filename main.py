import serial
import time
from datetime import datetime
import os


ser = serial.Serial('/dev/tty.usbmodemF412FA9E64082', 115200, timeout=1)


def receive_image():
   print("Waiting for start marker...")
   while True:
       line = ser.readline().decode('utf-8', errors='ignore').strip()
       if line:
           print(f"Debug: {line}")
      
       byte = ser.read(1)
       if byte:
           print(f"Received byte: {byte.hex()}")
           if byte == b'\xFF':
               second_byte = ser.read(1)
               print(f"Second byte: {second_byte.hex()}")
               third_byte = ser.read(1)
               print(f"Third byte: {third_byte.hex()}")
               if second_byte == b'\xAA' and third_byte == b'\x01':
                   break
   print("Start marker received")


   # Read image size
   size_bytes = ser.read(4)
   if len(size_bytes) != 4:
       print(f"Error: Received {len(size_bytes)} bytes for image size instead of 4")
       return None
   image_size = int.from_bytes(size_bytes, byteorder='little')
   print(f"Image size: {image_size} bytes")


   if image_size == 0 or image_size > 1024 * 1024 * 2:  # Check if size is 0 or larger than 2MB
       print(f"Error: Invalid image size: {image_size} bytes")
       return None


   # Read image data
   image_data = b''
   start_time = time.time()
   while len(image_data) < image_size:
       chunk = ser.read(min(1024, image_size - len(image_data)))
       if not chunk:
           print(f"Timeout while reading image data after {len(image_data)} bytes")
           return None
       image_data += chunk
       print(f"Received {len(image_data)} of {image_size} bytes")


       # Read any debug messages
       while ser.in_waiting:
           line = ser.readline().decode('utf-8', errors='ignore').strip()
           if line:
               print(f"Debug: {line}")


       if time.time() - start_time > 30:  # 30 seconds timeout
           print("Timeout: Image transfer took too long")
           return None


   # Wait for end marker
   end_marker = ser.read(2)
   if end_marker != b'\xFF\xBB':
       print(f"Invalid end marker: {end_marker.hex()}")
       return None


   print("Image fully received")
   return image_data


def save_image(image_data):
   desktop = os.path.expanduser("~/Desktop")
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   filename = f"arducam_{timestamp}.jpg"
   filepath = os.path.join(desktop, filename)


   with open(filepath, 'wb') as f:
       f.write(image_data)
  
   print(f"Image saved: {filepath}")


try:
   ser.reset_input_buffer()
   while True:
       print("\nWaiting for image...")
       image_data = receive_image()
       if image_data:
           save_image(image_data)
       else:
           print("Failed to receive image")
except KeyboardInterrupt:
   print("Stopped by user")
finally:
   ser.close()






# ==================================================================================================





# import serial
# import time
# from datetime import datetime
# import os


# ser = serial.Serial('/dev/tty.usbmodemF412FA9E64082', 115200, timeout=1)


# def receive_image():
#    print("Waiting for start marker...")
#    while True:
#        line = ser.readline().decode('utf-8', errors='ignore').strip()
#        if line:
#            print(f"Debug: {line}")
      
#        byte = ser.read(1)
#        if byte:
#            print(f"Received byte: {byte.hex()}")
#            if byte == b'\xFF':
#                second_byte = ser.read(1)
#                print(f"Second byte: {second_byte.hex()}")
#                third_byte = ser.read(1)
#                print(f"Third byte: {third_byte.hex()}")
#                if second_byte == b'\xAA' and third_byte == b'\x01':
#                    break
#    print("Start marker received")


#    # Read image size
#    size_bytes = ser.read(4)
#    image_size = int.from_bytes(size_bytes, byteorder='little')
#    print(f"Image size: {image_size} bytes")


#    # Read image data
#    image_data = b''
#    while len(image_data) < image_size:
#        chunk = ser.read(min(1024, image_size - len(image_data)))
#        if not chunk:
#            print("Timeout while reading image data")
#            return None
#        image_data += chunk
#        print(f"Received {len(image_data)} of {image_size} bytes")


#        # Read any debug messages
#        while ser.in_waiting:
#            line = ser.readline().decode('utf-8', errors='ignore').strip()
#            if line:
#                print(f"Debug: {line}")


#    # Wait for end marker
#    end_marker = ser.read(2)
#    if end_marker != b'\xFF\xBB':
#        print(f"Invalid end marker: {end_marker}")
#        return None


#    print("Image fully received")
#    return image_data


# def save_image(image_data):
#    desktop = os.path.expanduser("~/Desktop")
#    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#    filename = f"arducam_{timestamp}.jpg"
#    filepath = os.path.join(desktop, filename)


#    with open(filepath, 'wb') as f:
#        f.write(image_data)
  
#    print(f"Image saved: {filepath}")


# try:
#    ser.reset_input_buffer()
#    while True:
#        print("\nWaiting for image...")
#        image_data = receive_image()
#        if image_data:
#            save_image(image_data)
#        else:
#            print("Failed to receive image")
# except KeyboardInterrupt:
#    print("Stopped by user")
# finally:
#    ser.close()






# ============================================================





# import serial
# import time
# from datetime import datetime
# import os

# ser = serial.Serial('/dev/cu.usbmodemF412FA9E64082', 115200, timeout=1)

# def receive_image():
#     print("Waiting for start marker...")
#     # Wait for start marker
#     while True:
#         if ser.in_waiting >= 3:
#             marker = ser.read(3)
#             if marker == b'\xFF\xAA\x01':
#                 print("Start marker received")
#                 break
#             else:
#                 print(f"Unexpected marker: {marker}")

#     # Read image size
#     size_bytes = ser.read(4)
#     image_size = int.from_bytes(size_bytes, byteorder='little')
#     print(f"Image size: {image_size}")

#     # Read image data
#     image_data = bytearray()
#     while len(image_data) < image_size:
#         if ser.in_waiting > 0:
#             image_data.extend(ser.read(ser.in_waiting))
#     print("Image data received")

#     # Wait for end marker
#     while ser.read(2) != b'\xFF\xBB':
#         pass
#     print("End marker received")

#     return image_data

# def save_image(image_data):
#     desktop = os.path.expanduser("~/Desktop")
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"arducam_{timestamp}.jpg"
#     filepath = os.path.join(desktop, filename)

#     with open(filepath, 'wb') as f:
#         f.write(image_data)
  
#     print(f"Image saved: {filepath}")

# try:
#     while True:
#         image_data = receive_image()
#         save_image(image_data)
#         time.sleep(10)  # Wait for 10 seconds before next capture
# except KeyboardInterrupt:
#     print("Stopped by user")
# finally:
#     ser.close()




# ============================================================






# import serial
# import time
# from datetime import datetime
# import os

# ser = serial.Serial('/dev/tty.usbmodemF412FA9E64082', 115200)  # Update this if necessary

# def receive_image():
#     print("Waiting for start marker...")
#     # Wait for start marker
#     while ser.read(3) != b'\xFF\xAA\x01':
#         pass
#     print("Start marker received")

#     # Read image size
#     size_bytes = ser.read(4)
#     image_size = int.from_bytes(size_bytes, byteorder='little')
#     print(f"Image size: {image_size}")

#     # Read image data
#     image_data = bytearray()
#     while len(image_data) < image_size:
#         if ser.in_waiting > 0:
#             image_data.extend(ser.read(ser.in_waiting))
#     print("Image data received")

#     # Wait for end marker
#     while ser.read(2) != b'\xFF\xBB':
#         pass
#     print("End marker received")

#     return image_data

# def save_image(image_data):
#     desktop = os.path.expanduser("~/Desktop")
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"arducam_{timestamp}.jpg"
#     filepath = os.path.join(desktop, filename)

#     with open(filepath, 'wb') as f:
#         f.write(image_data)
  
#     print(f"Image saved: {filepath}")

# try:
#     while True:
#         image_data = receive_image()
#         save_image(image_data)
#         time.sleep(10)  # Wait for 10 seconds before next capture
# except KeyboardInterrupt:
#     print("Stopped by user")
# finally:
#     ser.close()








# ============================================================





# import serial
# import time

# ser = serial.Serial('/dev/cu.usbmodemF412FA9E64082', 115200)  # Update this if necessary

# def receive_data():
#     print("Waiting for start marker...")
#     start_time = time.time()
#     # Wait for start marker
#     while True:
#         if ser.in_waiting >= 3:
#             if ser.read(3) == b'\xFF\xAA\x01':
#                 print("Start marker received")
#                 break
#         if time.time() - start_time > 5:  # Timeout after 5 seconds
#             print("Timeout waiting for start marker")
#             return

#     # Read payload
#     payload = bytearray()
#     start_time = time.time()
#     while len(payload) < 5:
#         if ser.in_waiting > 0:
#             payload.extend(ser.read(ser.in_waiting))
#         if time.time() - start_time > 5:  # Timeout after 5 seconds
#             print("Timeout waiting for payload")
#             return
#     print(f"Payload received: {list(payload[:5])}")

#     # Wait for end marker
#     start_time = time.time()
#     while True:
#         if ser.in_waiting >= 2:
#             if ser.read(2) == b'\xFF\xBB':
#                 print("End marker received")
#                 break
#         if time.time() - start_time > 5:  # Timeout after 5 seconds
#             print("Timeout waiting for end marker")
#             return

# try:
#     while True:
#         receive_data()
#         time.sleep(1)  # Wait for 1 second before next read
# except KeyboardInterrupt:
#     print("Stopped by user")
# finally:
#     ser.close()





# ==================================================================






# import serial
# import time

# ser = serial.Serial('/dev/cu.usbmodemF412FA9E64082', 115200)  # Update this if necessary

# def receive_data():
#     # Wait for start marker
#     while ser.read(3) != b'\xFF\xAA\x01':
#         pass
#     print("Start marker received")

#     # Read data
#     data = ser.read(14)  # Read 14 bytes (length of "Hello, Python!")
#     print(f"Data received: {data.decode('utf-8')}")

#     # Wait for end marker
#     while ser.read(2) != b'\xFF\xBB':
#         pass
#     print("End marker received")

# try:
#     while True:
#         receive_data()
#         time.sleep(1)  # Wait for 1 second before next read
# except KeyboardInterrupt:
#     print("Stopped by user")
# finally:
#     ser.close()







# import serial
# import time
# from datetime import datetime
# import os


# ser = serial.Serial('/dev/cu.usbmodemF412FA9E64082', 115200)


# def receive_image():
#    # Wait for start marker
#    while ser.read(3) != b'\xFF\xAA\x01':
#        pass


#    # Read image size
#    size_bytes = ser.read(4)
#    image_size = int.from_bytes(size_bytes, byteorder='little')


#    # Read image data
#    image_data = ser.read(image_size)


#    # Wait for end marker
#    while ser.read(2) != b'\xFF\xBB':
#        pass


#    return image_data


# def save_image(image_data):
#    desktop = os.path.expanduser("~/Desktop")
#    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#    filename = f"arducam_{timestamp}.jpg"
#    filepath = os.path.join(desktop, filename)


#    with open(filepath, 'wb') as f:
#        f.write(image_data)
  
#    print(f"Image saved: {filepath}")


# try:
#    while True:
#        image_data = receive_image()
#        save_image(image_data)
#        time.sleep(10)  # Wait for 10 seconds before next capture
# except KeyboardInterrupt:
#    print("Stopped by user")
# finally:
#    ser.close()