import random
import pandas as pd
import json
from helpers.fetch_data import fetch_data


def export_data(filtered_data):
    json_output_file_name = 'lc-questions.json'
    excel_output_file_name = 'lc-questions.xlsx'
    
    filtered_data["Title"] = filtered_data["Title"].apply(lambda x: x.split('>')[1].split('<')[0])

    json.dumps(filtered_data, indent=4, sort_keys=True, default=str)
    filtered_data.to_excel(excel_output_file_name, index=False)

    return json_output_file_name, excel_output_file_name


def get_rand_int(max_skip, limit):
    return random.randint(0, max_skip // limit) * limit


all_topics = ["Array",
              "String",
              "Hash Table",
              "Dynamic Programming",
              "Math",
              "Sorting",
              "Greedy",
              "Depth-First Search",
              "Database",
              "Binary Search",
              "Tree",
              "Breadth-First Search",
              "Matrix",
              "Bit Manipulation",
              "Two Pointers",
              "Binary Tree",
              "Heap (Priority Queue)",
              "Prefix Sum",
              "Stack",
              "Simulation",
              "Graph",
              "Counting",
              "Design",
              "Sliding Window",
              "Backtracking",
              "Enumeration",
              "Union Find",
              "Linked List",
              "Ordered Set",
              "Monotonic Stack",
              "Number Theory",
              "Trie",
              "Divide and Conquer",
              "Bitmask",
              "Recursion",
              "Segment Tree",
              "Queue",
              "Binary Search Tree",
              "Memoization",
              "Geometry",
              "Binary Indexed Tree",
              "Hash Function",
              "Combinatorics",
              "Topological Sort",
              "String Matching",
              "Shortest Path",
              "Rolling Hash",
              "Game Theory",
              "Interactive",
              "Data Stream",
              "Brainteaser",
              "Monotonic Queue",
              "Randomized",
              "Merge Sort",
              "Iterator",
              "Concurrency",
              "Doubly-Linked List",
              "Probability and Statistics",
              "Quickselect",
              "Bucket Sort",
              "Suffix Array",
              "Minimum Spanning Tree",
              "Counting Sort",
              "Shell",
              "Line Sweep",
              "Reservoir Sampling",
              "Strongly Connected Component",
              "Eulerian Circuit",
              "Radix Sort",
              "Rejection Sampling",
              "Biconnected Component"]


def filter_data(num_questions, easy_proportion, medium_proportion, hard_proportion, topics):
    easy_questions = []
    medium_questions = []
    hard_questions = []

    num_easy = int(num_questions * easy_proportion // 100)
    num_medium = int(num_questions * medium_proportion // 100)
    num_hard = int(num_questions * hard_proportion // 100)

    limit = 100
    max_skip = 3189
    previous_skips = set()

    while len(easy_questions) < num_easy or len(medium_questions) < num_medium or len(hard_questions) < num_hard:
        skip = get_rand_int(max_skip, limit)

        while skip in previous_skips:
            skip = get_rand_int(max_skip, limit)

        data = fetch_data(limit, skip)
        previous_skips.add(skip)
        print(f"Fetched data for skip: {skip}")
        questions = data['data']['problemsetQuestionList']['questions']

        if topics:
            filtered_questions = [
                q for q in questions if q['topicTags'] and any(topic['name'] in topics for topic in q['topicTags'])
            ]
        else:
            filtered_questions = questions

        easy_questions.extend([q for q in filtered_questions if q['difficulty'] == 'Easy'])
        medium_questions.extend([q for q in filtered_questions if q['difficulty'] == 'Medium'])
        hard_questions.extend([q for q in filtered_questions if q['difficulty'] == 'Hard'])

        if len(easy_questions) >= num_easy and len(medium_questions) >= num_medium and len(hard_questions) >= num_hard:
            break

    sampled_easy = random.sample(easy_questions, min(num_easy, len(easy_questions)))
    sampled_medium = random.sample(medium_questions, min(num_medium, len(medium_questions)))
    sampled_hard = random.sample(hard_questions, min(num_hard, len(hard_questions)))

    final_questions = sampled_easy + sampled_medium + sampled_hard
    random.shuffle(final_questions)

    formatted_response = []
    for question in final_questions:
        title_text, slug = question["title"],  question["titleSlug"]
        url = f"https://leetcode.com/problems/{slug}/description"

        title = f'<a target="_blank" href="{url}">{title_text}</a>'
        topic_names = ", ".join([topic["name"] for topic in question["topicTags"]])
        difficulty = question["difficulty"]
        acceptance_rate = round(float(question["acRate"]), 2)
        formatted_response.append(
            {"Title": title, "Topics": topic_names, "Difficulty": difficulty, "Acceptance Rate": acceptance_rate})

    filtered_data = pd.DataFrame(formatted_response)
    json_file, excel_file = export_data(filtered_data)

    return filtered_data, json_file, excel_file
