
import hashlib
import datetime
import json
import random
import pickle
import csv

class Block:
    def __init__(self, text):
        self.text = text
            
        

    def to_json(self):
        return {
            "messages": self.text
        }
    def calculate_hash(self):
        block_text = str(self.timestamp) + str(self.text) + str(self.previous_hash)
        hash_object = hashlib.sha256(block_text.encode('utf-8'))
        return hash_object.hexdigest()

    def to_csv(self):

        return f"{self.text}"

    def from_csv(csv_string):
        text = csv_string.strip()
        return Block(text)

class Blockchain:
    def __init__(self, password):
        self.chain = []
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.create_genesis_block()

    def verify_password(self, input_password):
        return hashlib.sha256(input_password.encode('utf-8')).hexdigest() == self.password

    def create_genesis_block(self):
        #genesis_block = Block("Genesis Block")________________________________________________________________________________________________________
        genesis_block = Block('1')
        self.chain.append(genesis_block)

#chunk_size=512
        
    def add_block(self, text, input_password, chunk_size=1024):
        if not self.verify_password(input_password):
            return "Invalid password"

        i = 0
        while i < len(text):
        # Extract up to the chunk size
            chunk_text = text[i:i + chunk_size]

        # Check if we are not at the end and the next character is not a period
            if i + chunk_size < len(text) and text[i + chunk_size] != '.':
            # Find the last period in this chunk
                last_period_index = chunk_text.rfind('.')
                if last_period_index != -1:
                # Adjust the chunk to end at the last period
                    chunk_text = chunk_text[:last_period_index + 1]

            chunk_text = chunk_text.strip()

            if chunk_text:
                new_block = Block(chunk_text)
                self.chain.append(new_block)

        # Move the index. If we adjusted the chunk, move accordingly
            i += len(chunk_text)
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_block(self, index, input_password):
        if not self.verify_password(input_password):
            return "Invalid password"

        if index < 0 or index >= len(self.chain):
            return "Invalid block index"
        return self.chain[index]

    def display_block(self, index, input_password):

        if not self.verify_password(input_password):
            print("Invalid password")
            return

        block = self.get_block(index, input_password)
        if isinstance(block, Block):
            print(f"Block {index}:")
            print(f"text: {block.text}")
            print(f"Password: {input_password}")
        else:
            print(block)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.chain, file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            loaded_chain = pickle.load(file)
            if self.is_valid_chain(loaded_chain):
                self.chain = loaded_chain
            else:
                raise Exception("Invalid Chain")

    def is_valid_chain(self, chain):
        if not chain:
            return False

        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            # Check hash consistency
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check previous hash reference
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def display_chain_length(self):
        print("Blocks in the blockchain:", len(self.chain))

    def display_full_content(self, delimiter="--END--"):
        full_content = ""
        for block in self.chain:
            full_content += block.text

        # Split the content into individual files based on the delimiter
        individual_files = full_content.split(delimiter)

        for i, file_content in enumerate(individual_files):
            if file_content.strip():  # Check if the content is not just whitespace
                print(f"File {i + 1} Content:")
                print(file_content)
                print("\n" + "-" * 50 + "\n")  # Separator between files

    def get_random_block_text(blockchain):
        if len(blockchain.chain) > 1:
            random_block = random.choice(blockchain.chain[1:])
            return random_block.text
        else:
            return "No blocks to display."

    def save_to_jsonl(self, filename):
        with open(filename, 'w') as file:
            for block in self.chain:
                json.dump(block.to_json(), file)
                file.write('\n')


    def load_from_jsonl(self, filename):
        with open(filename, 'r') as file:
            self.chain = []
            for line in file:
                try:
                    block_data = json.loads(line)
                    block = Block(block_data["text"])  # Adjust based on your Block class structure
                    self.chain.append(block)
                except json.JSONDecodeError as e:
                    print("Error processing line:", line)
                    print("JSONDecodeError:", e)

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            for block in self.chain:
                csv_writer.writerow([block.to_csv()])

    def load_from_csv(self, filename):
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            self.chain = []
            for row in csv_reader:
                if row:  # Check if the row is not empty
                    block = Block.from_csv(row[0])
                    self.chain.append(block)
    
def get_block_texts(blockchain):
    texts = [block.text for block in blockchain.chain[1:]]  # Skip the genesis block
    return texts
