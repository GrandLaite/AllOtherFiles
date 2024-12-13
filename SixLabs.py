import heapq
import json
from collections import Counter
from graphviz import Digraph

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def create_huffman_codes(node, prefix="", codebook={}):
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        create_huffman_codes(node.left, prefix + "0", codebook)
        create_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def visualize_huffman_tree(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph(format='png', filename='huffman_tree')

    current = str(id(node))

    if node.char is None:
        label = f"Freq: {node.freq}"
    else:
        label = f"'{node.char}'\\nFreq: {node.freq}"

    graph.node(current, label)

    if parent:
        graph.edge(parent, current)

    if node.left:
        visualize_huffman_tree(node.left, graph, current)
    if node.right:
        visualize_huffman_tree(node.right, graph, current)

    return graph

if __name__ == "__main__":
    input_file = input("Введите имя входного файла: ")

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_string = file.read().strip()
    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
        exit()

    frequency = Counter(input_string)

    huffman_tree = build_huffman_tree(frequency)

    huffman_codes = create_huffman_codes(huffman_tree)

    print("Коды Хаффмана для символов:")
    for char, code in huffman_codes.items():
        print(f"{repr(char)}: {code}")

    graph = visualize_huffman_tree(huffman_tree)
    graph.render()
    print("Дерево Хаффмана сохранено в файле 'huffman_tree.png'.")

    output_file = input("Введите имя файла для сохранения кодов Хаффмана: ")
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(huffman_codes, file, ensure_ascii=False, indent=4)
    print(f"Коды Хаффмана сохранены в файл {output_file}.")
