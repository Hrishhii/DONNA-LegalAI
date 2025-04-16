import os

class TextChunker:
    def __init__(self, max_chunk_size=1000):
        self.max_chunk_size = max_chunk_size
    
    def chunk_text(self, text):
        overlap_size = 200
        chunks = [text[i:i + self.max_chunk_size] for i in range(0, len(text), self.max_chunk_size - overlap_size)]
        return chunks
    
    def read_extracted_text(self, text_file_name):
        file_path = os.path.join("extracted_texts", text_file_name)
        with open(file_path, 'r', encoding="utf-8") as file:
            text = file.read()
        return text
    
    def chunk_extracted_text(self, text_file_name):
        text = self.read_extracted_text(text_file_name)
        return self.chunk_text(text)
    
if __name__ == "__main__":
    text_file_name = "sample.txt"
    chunker = TextChunker()
    chunks = chunker.chunk_extracted_text(text_file_name)
    for idx, chunk in enumerate(chunks):
        print(f"Chunk {idx + 1}: {chunk[:200]}...")