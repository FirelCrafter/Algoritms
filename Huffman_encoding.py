import heapq
from collections import Counter
from collections import namedtuple


class Node(namedtuple('Node', ['left', 'right'])):
    def walk(self, code, acc):
        self.left.walk(code, acc + '0')
        self.right.walk(code, acc + '1')


class Leaf(namedtuple('Leaf', ['char'])):
    def walk(self, code, acc):
        code[self.char] = acc or '0'


def huffman_encode(s):
    h = []
    for char, freq in Counter(s).items():
        h.append((freq, len(h), Leaf(char)))
    heapq.heapify(h)
    count = len(h)
    while len(h) > 1:
        freq1, _count1, left = heapq.heappop(h)
        freq2, _count2, right = heapq.heappop(h)

        heapq.heappush(h, (freq1 + freq2, count, Node(left, right)))

        count += 1
    code = {}
    if h:
        [(freq, _count, root)] = h
        root.walk(code, '')
    return code


def huffman_decode(encoded, code):
    sx = []
    enc_char = ''
    for char in encoded:
        enc_char += char
        for dec_char in code:
            if code.get(dec_char) == enc_char:
                sx.append(dec_char)
                enc_char = ''
                break
    return ''.join(sx)


def main():
    s = input()
    code = huffman_encode(s)
    encoded = ''.join(code[char] for char in s)

    print(len(code), len(encoded))
    for char in sorted(code):
        print('{}: {}'.format(char, code[char]))
    print(encoded)
    print(huffman_decode(encoded, code))

main()
