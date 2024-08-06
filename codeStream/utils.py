import json


def load_knowledge(filename):
    """
    Load knowledge points from a JSON file.

    Args:
        filename (str): The path to the JSON file containing knowledge points.

    Returns:
        dict: A dictionary of knowledge points. If an error occurs, returns a default dictionary with sample knowledge points.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            points = json.load(file)
        print(f"Successfully loaded {len(points)} knowledge points")
        return points
    except Exception as e:
        print(f"Error loading file: {e}")
        return {"Python": "A programming language", "Artificial Intelligence": "Technology that simulates human intelligence", "Data Structures": "Ways to organize and store data"}