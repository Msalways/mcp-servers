from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
result = model.encode('test')
print('Type:', type(result))
print('tolist method exists:', hasattr(result, 'tolist'))
print('Is list:', isinstance(result, list))
print('Length:', len(result))
print('First 5 elements:', result[:5])
