def main():
	while(True):
		input_op = input("\nDo you want to:\n"
						"1. Read from file? (check '.txt' files in '/sentences')\n"
						"2.Read from console?\n"
						"3. Train model?\n")
		if input_op == '1':
			fp = "/sentences/"\
				+ input("Enter filename (no extension):\n")\
				+ ".txt"

			with open(fp, 'r') as file:
				sentence_buffer = [line.strip() for line in file]

			for s in sentence_buffer:
				predict(s) ### PLACEHOLDER
		elif input_op == '2':
			predict( input("Enter sentence:\n") ) ### PLACEHOLDER
		elif input_op == '3':
			generate_model() ### PLACEHOLDER
		else:
			print("Invalid option entered.\n")

if __name__ == "__main__":
    main()