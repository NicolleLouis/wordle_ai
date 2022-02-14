from larousse.generate_larousse import GenerateLarousse

length = int(input("Choose word length: "))
GenerateLarousse.filter_letter(length)
GenerateLarousse.remove_duplicate()
