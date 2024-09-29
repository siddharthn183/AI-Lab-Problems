import heapq
import re

class PlagiarismNode:
    def __init__(self, position, parent=None, cost_g=0, heuristic_h=0):
        self.position = position
        self.parent = parent
        self.cost_g = cost_g
        self.heuristic_h = heuristic_h
        self.total_cost_f = cost_g + heuristic_h

    def __lt__(self, other):
        return self.total_cost_f < other.total_cost_f

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def calculate_edit_distance(str1, str2):
    length1, length2 = len(str1), len(str2)
    dp_table = [[0] * (length2 + 1) for _ in range(length1 + 1)]
    
    for i in range(length1 + 1):
        for j in range(length2 + 1):
            if i == 0:
                dp_table[i][j] = j
            elif j == 0:
                dp_table[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp_table[i][j] = dp_table[i-1][j-1]
            else:
                dp_table[i][j] = 1 + min(dp_table[i-1][j], dp_table[i][j-1], dp_table[i-1][j-1])
    
    return dp_table[length1][length2]

def generate_successors(node, text1, text2):
    successors = []
    pos1, pos2 = node.position

    if pos1 < len(text1) and pos2 < len(text2):
        new_position = (pos1 + 1, pos2 + 1)
        successor_node = PlagiarismNode(new_position, node)
        successors.append(successor_node)

    if pos1 < len(text1):
        new_position = (pos1 + 1, pos2)
        successor_node = PlagiarismNode(new_position, node)
        successors.append(successor_node)

    if pos2 < len(text2):
        new_position = (pos1, pos2 + 1)
        successor_node = PlagiarismNode(new_position, node)
        successors.append(successor_node)

    return successors

def heuristic_function(position, text1, text2):
    pos1, pos2 = position
    return ((len(text1) - pos1) + (len(text2) - pos2)) / 2

def a_star_plagiarism_detection(text1, text2):
    start_position = (0, 0)
    goal_position = (len(text1), len(text2))
    start_node = PlagiarismNode(start_position)
    open_set = []
    heapq.heappush(open_set, (start_node.total_cost_f, start_node))
    visited_positions = set()

    while open_set:
        _, current_node = heapq.heappop(open_set)
        if current_node.position in visited_positions:
            continue
        visited_positions.add(current_node.position)

        if current_node.position == goal_position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for successor in generate_successors(current_node, text1, text2):
            pos1, pos2 = successor.position
            if pos1 < len(text1) and pos2 < len(text2):
                successor.cost_g = current_node.cost_g + calculate_edit_distance(text1[pos1], text2[pos2])
            else:
                successor.cost_g = current_node.cost_g + 1
            successor.heuristic_h = heuristic_function(successor.position, text1, text2)
            successor.total_cost_f = successor.cost_g + successor.heuristic_h
            heapq.heappush(open_set, (successor.total_cost_f, successor))

    return None

def align_documents(doc1, doc2):
    return a_star_plagiarism_detection(doc1, doc2)

def identify_plagiarism(doc1, doc2, similarity_threshold=0.5):
    doc1_cleaned = [clean_text(sentence) for sentence in doc1]
    doc2_cleaned = [clean_text(sentence) for sentence in doc2]

    alignment_result = align_documents(doc1_cleaned, doc2_cleaned)
    detected_plagiarism = []
    for i, j in alignment_result:
        if i < len(doc1_cleaned) and j < len(doc2_cleaned):
            sentence1, sentence2 = doc1_cleaned[i], doc2_cleaned[j]
            maximum_length = max(len(sentence1), len(sentence2))
            if maximum_length > 0:
                similarity_ratio = 1 - (calculate_edit_distance(sentence1, sentence2) / maximum_length)
                if similarity_ratio >= similarity_threshold:
                    detected_plagiarism.append((doc1_cleaned[i], doc2_cleaned[j], similarity_ratio))
    return detected_plagiarism

document1 = [
    "Good night",
    "Hello World",
    "Jai Hind.",
    "Naveen",
]

document2 = [
    "Good morning",
    "Hello old",
    "Jai Hind",
    "Navin"   
]

plagiarism_results = identify_plagiarism(document1, document2)
if plagiarism_results:
    print("Potential plagiarism detected:")
    for pair in plagiarism_results:
        print(f"Doc1: {pair[0]} \nDoc2: {pair[1]} \nSimilarity: {pair[2]}")
else:
    print("No plagiarism detected.")
