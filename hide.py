
# can we hide a message in the RGB channel of an image

from PIL import Image

filename = '6823214-large.jpg'
fileout = 'newimage.png'
message = 'there is a hidden message in this image stop can we encode and decode it stop '
message = message * 100
print(len(message))

img = Image.open(filename)
img = img.convert('RGBA')
data = img.getdata()
print(len(data))
print(data[0])

# 3 ** 3 = 27 so we can encode 26 letters and space in one number pixel

# ord('a') = 97
# int('222', 3) = 26

def conv_trin_to_letter(trin):
	# 000 is space
	# 001 is a ...
	if trin == '000':
		return ' '
	else:
		num = int(trin, 3)
		return chr(96 + num)

# lookup for number to trin

trin_dict = {}
n = 0
for i in range(3):
	for j in range(3):
		for k in range(3):
			num = str(i) + str(j) + str(k)
			# trin_dict[1] = 001
			trin_dict[n] = num
			n += 1
print(trin_dict)

def conv_letter_to_trin(letter):
	# a is 001 ...
	if letter == ' ':
		return '000'
	else:
		num = ord(letter) - 96
		return trin_dict[num]

print(conv_trin_to_letter('001'))
print(conv_letter_to_trin('a'))

# create encoded image

newdata = []
n = 0

for item in data:
  if n < len(message):
  	letter = message[n]
  	trin = conv_letter_to_trin(letter)
  	item_list = list(item)
  	for i in range(3):
  	  item_list[i] += int(trin[i])
  	item = tuple(item_list)
  n += 1
  newdata.append(item)

img.putdata(newdata)
img.save(fileout, 'PNG')

# now lets decode it, given original and new image

im1 = Image.open(filename)
im2 = Image.open(fileout)

im1 = im1.convert('RGBA')
im2 = im2.convert('RGBA')

data1 = im1.getdata()
data2 = im2.getdata()

print(len(data1) == len(data2))

def diff_tuples(a, b):
  s = ''
  for i in range(3):
  	s += str(a[i] - b[i])
  return s

message_found = ''
last2 = ''

for i in range(len(data1)):
	item1, item2 = data1[i], data2[i]
	diff = diff_tuples(item2, item1)
	letter = conv_trin_to_letter(diff)
	if last2 == '  ':
		break
	message_found += letter
	last2 = message_found[-2:]

print(message_found)