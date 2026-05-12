from PIL import Image

# 1.1 ДЕКОДИРОВАНИЕ ТЕКСТА

# Загружаем изображение
image = Image.open("new33.png")
pixels = image.load()

# Координаты из keys33.txt
keys = []
with open("keys33.txt", "r") as file:
    for line in file:
        line = line.strip()
        line = line.replace("(", "")
        line = line.replace(")", "")
        x, y = line.split(",")
        keys.append((int(x), int(y)))

# Извлекаем синий канал и собираем байты
text_bytes = []
for x, y in keys:
    r, g, b, a = pixels[x, y]
    text_bytes.append(b)

# Преобразуем байты в текст
text = bytes(text_bytes).decode("utf-8", errors="ignore")

print("Декодированное сообщение:")
print(text)

# 1.2 КОДИРОВАНИЕ И ДЕКОДИРОВАНИЕ ТЕКСТА

# Текст для кодирования
message = "Hi"

# Переводим текст в байты
message_bytes = message.encode("utf-8")

# Преобразуем байты в биты
message_bits = []
for byte in message_bytes:
    bits = format(byte, "08b")
    for bit in bits:
        message_bits.append(bit)

# Вывод битов первого символа
first_symbol_bits = format(message_bytes[0], "08b")
print("\nБиты первого символа:")
print(first_symbol_bits)

# Кодирование
bit_index = 0
for y in range(image.height):
    for x in range(image.width):

        if bit_index >= len(message_bits):
            break

        r, g, b, a = pixels[x, y]

        # Исходное значение пикселя
        old_b = b

        # Берём 4 бита сообщения
        bits4 = ""

        for i in range(4):
            if bit_index < len(message_bits):
                bits4 += message_bits[bit_index]
                bit_index += 1
            else:
                bits4 += "0"

        # Заменяем младшие 4 бита синего канала
        b = (b & 240) | int(bits4, 2)

        # Записываем новый пиксель
        pixels[x, y] = (r, g, b, a)

        # Вывод информации
        print("\nПиксель:", (x, y))
        print("Исходный B:", old_b, "->", format(old_b, "08b"))
        print("Измененный B:", b, "->", format(b, "08b"))

    if bit_index >= len(message_bits):
        break

# Сохраняем изображение
image.save("encoded.png")

print("\nТекст успешно закодирован.")

# ДЕКОДИРОВАНИЕ ОБРАТНО

image2 = Image.open("encoded.png")
pixels2 = image2.load()

decoded_bits = ""

needed_bits = len(message_bytes) * 8
current_bits = 0

for y in range(image2.height):
    for x in range(image2.width):

        if current_bits >= needed_bits:
            break

        r, g, b, a = pixels2[x, y]

        # Получаем младшие 4 бита
        bits4 = format(b & 15, "04b")

        decoded_bits += bits4
        current_bits += 4

    if current_bits >= needed_bits:
        break

# Собираем байты обратно
decoded_bytes = []
for i in range(0, len(decoded_bits), 8):
    byte = decoded_bits[i:i+8]
    decoded_bytes.append(int(byte, 2))

decoded_text = bytes(decoded_bytes).decode("utf-8", errors="ignore")
print("\nДекодированный текст:")
print(decoded_text)