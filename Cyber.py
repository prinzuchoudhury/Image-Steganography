#Hiding Text in an image

from PIL import Image		#PythonImageLibrary
import binascii 		#binary ASCII
import optparse

#Utility functions

def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)		#returning Hex value 

def hex2rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex'))) 	#take away the hash at front and reutrn RGB in a tupple
								#ord -> char to 
								#map() function returns a list of the results after applying the given function to each item of a given iterable (list, tuple etc.) Syntax : map(fun, iter)
def str2bin(message):
	binary = bin(int(binascii.hexlify(message), 16))	#Bin ASCII library - BASE 16	- convert an integer into binary format string prefixed (0b)					
	return binary[2:]					#hexify - Return the hexadecimal representation of the binary data. Every byte of data is converted into the corresponding 2-digit hex representation. The resulting string is therefore twice as long as the length of data.
								#Strip 1st 2 chracters coz it adds 0b at front(don't need) 
def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b'+binary,2)))
	return message

def encode(hexcode, digit):					#Turn our hex code of the colour of the pixel and we'll place a digit in it
	if hexcode[-1] in ('0','1', '2', '3', '4', '5'):	# -1? the very last digit in the hex code
		hexcode = hexcode[:-1] + digit			#replace the very last digit
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None

def hide(filename, message,s):				#filename of image and message to store inside image
	img = Image.open(filename)

	#encrypted text
	msg=message
	message=''
	for characters in msg:
		message=message+chr(ord(characters)+s)	
	print(message)	
	


	binary = str2bin(message) + '1111111111111110'		# plus on the delimeter into our binary, so that we know where the message ends
	if img.mode in ('RGBA'):			#check if image is editable
		img = img.convert('RGBA')		#to make sure it is in correct format
		datas = img.getdata()			#imageData - that's gonna return all the pixles inside the image
		
		newData = []		#list create (all our new pixels data)
		digit = 0		#current digit that we are up to in our binary
		temp = ''
		for item in datas:			#item == each pixel
			if (digit < len(binary)):	#store try and store data (length of binary we waana store)
				newpix = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])		#RGB of current into hex and give the binary that we want to store
				if newpix == None:
					newData.append(item)		#Just store current pixel that we don't want to change 
				else:					#append() method adds a single item to the existing list. It doesn't return a new list; rather it modifies the original list.
					r, g, b = hex2rgb(newpix)	#else create a new pixel and save it into new pixel
					newData.append((r,g,b,255))	#alpha == 255
					digit += 1
			else:
				newData.append(item)		#So No change ...adn Image created
		img.putdata(newData)
		img.save(filename, "PNG")
		return "Completed!"
			
	return "Incorrect Image Mode, Couldn't Hide"

						
				

def retr(filename,s):
	img = Image.open(filename)
	binary = ''

	if img.mode in ('RGBA'): 		#RGB-Alpha
		img = img.convert('RGBA')
		datas = img.getdata()
		
		for item in datas:
			digit = decode(rgb2hex(item[0],item[1],item[2]))	#item[0]=R
			if digit == None:		#we did'nt find any data inside the pixel so,
				pass			#we are going to pass the current
			else:
				binary = binary + digit				#digit we found
				if (binary[-16:] == '1111111111111110'):		#-16 to end of binary
					print "Success"
					msg = bin2str(binary[:-16])

					#decrypted text
					msg1=msg
					msg=''
					for characters in msg1:
						msg=msg+chr(ord(characters)-s)		#edge case - if message is much longer than image size
					return msg

		msg=bin2str(binary)
		#decrypted text
		msg1=msg
		msg=''
		
		for characters in msg1:
			msg=msg+chr(ord(characters)-s)		#edge case - if message is much longer than image size
		return msg

	return "Incorrect Image Mode, Couldn't Retrieve"

def Main():                                     #optparse == arg. handeling after option ( +\ security on next line) #create what it's usage is(when try to use our prog)
        parser = optparse.OptionParser('usage %prog '+\
		'-e/-d <target file>')					        
	parser.add_option('-e', dest='hide', type='string', \
		help='target picture path to hide text')                 
	parser.add_option('-d', dest='retr', type='string', \
		help='target picture path to retrieve text')
	
	(options, args) = parser.parse_args()			#retrive the pass option
	if (options.hide != None):
		text = raw_input("Enter a message to hide: ")	#input in python 3.x
		s = int(input("Enter public key: "))
		print hide(options.hide, text,s)
	elif (options.retr != None):
		s = int(input("Enter your private key: "))	
                print retr(options.retr,s)
	else:						            #Can't enter in a file name or forgot to add option
		print parser.usage
        exit(0)


if __name__ == '__main__':  		#script is being run directly or being imported by something else by testing __name__ variable
	Main()



