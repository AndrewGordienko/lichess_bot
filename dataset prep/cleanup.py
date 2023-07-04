import re

with open('master_games.txt', 'r') as file:
    content = file.read()

# Use regular expressions to extract paragraphs between white spaces
paragraphs = re.findall(r'\n\n(.*?)\n\n', content, re.DOTALL)

# Write the extracted paragraphs to clean_moves.txt
with open('clean_moves.txt', 'w') as file:
    for i, paragraph in enumerate(paragraphs):
        file.write(paragraph + '\n')

        if i < len(paragraphs) - 1:
            file.write('\n')
