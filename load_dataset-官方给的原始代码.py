from datasets import load_dataset

# For single-turn dataset
#dataset = load_dataset("crag-mm-2025/crag-mm-single-turn-public", revision="v0.1.1")

# For multi-turn dataset
dataset = load_dataset("crag-mm-2025/crag-mm-multi-turn-public", revision="v0.1.1")

# View available splits
print(f"Available splits: {', '.join(dataset.keys())}")

# Access example data
example = dataset["validation"][0]
print(f"Session ID: {example['session_id']}")
print(f"Image: {example['image']}")
print(f"Image URL: {example['image_url']}")
"""
Note:
Either 'image' or 'image_url' will be provided, but not necessarily both.
When the actual image is unavailable, only the image URL will be provided.
The evaluation servers will always include the loaded 'image' field.
"""

# Display image
import matplotlib.pyplot as plt
plt.imshow(example['image'])


def prepare_feature_vocabularies(dataset_split):
    """Extract feature vocabularies for category encoding from dataset.
    
    These vocabularies allow conversion between integer indices and string labels.
    """
    return {
        "domain": dataset_split.features["turns"][0]["domain"],
        "query_category": dataset_split.features["turns"][0]["query_category"],
        "dynamism": dataset_split.features["turns"][0]["dynamism"],
        "image_quality": dataset_split.features["turns"][0]["image_quality"],
    }
from typing import Dict, Any

def print_conversation(example: Dict[str, Any], feature_vocabularies: Dict[str, Any]) -> None:
    """Print a conversation in an indented format.
    
    Args:
        example: A single dataset example containing conversation turns
        feature_vocabularies: Mapping of features to their vocabularies for encoding/decoding from idx to str
    """
    # Print session ID
    print(f"Session ID: {example['session_id']}")
    
    # Print image info
    print(f"Image: {example['image']}")
    print(f"Image URL: {example['image_url']}")
    """
    Note: Either 'image' or 'image_url' will be provided in the dataset, but not necessarily both.
    When the actual image cannot be included, only the image_url will be available.
    The evaluation servers will nevertheless always include the loaded 'image' field.
    """
    image_quality_str = feature_vocabularies["image_quality"].int2str(example['image_quality'])
    print(f"Image Quality: {image_quality_str}")
    
    # Determine if single-turn or multi-turn
    is_single_turn = len(example['turns']) == 1
    print(f"Type: {'Single-turn' if is_single_turn else 'Multi-turn'} ({len(example['turns'])} turns)")
    
    # Create answer lookup dictionary if answers exist
    answer_lookup = {}
    if 'answers' in example and example['answers'] is not None:
        answer_lookup = {a["interaction_id"]: a["ans_full"] for a in example["answers"]}
    
    # Print each turn
    print("\nConversation:")
    for i, turn in enumerate(example['turns']):
        # For multi-turn, show turn number
        if not is_single_turn:
            print(f"\tTurn {i+1}:")
        
        # Convert metadata to string representations
        domain_str = feature_vocabularies["domain"].int2str(turn['domain'])
        category_str = feature_vocabularies["query_category"].int2str(turn['query_category'])
        dynamism_str = feature_vocabularies["dynamism"].int2str(turn['dynamism'])
        
        # Print metadata
        prefix = "\t\t" if not is_single_turn else "\t"
        print(f"{prefix}Domain: {domain_str} | Category: {category_str} | Dynamism: {dynamism_str}")
        
        # Print query and answer with fixed tab indentation
        print(f"{prefix}Q: {turn['query']}")
        
        ans = answer_lookup.get(turn['interaction_id'], "No answer available")
        print(f"{prefix}A: {ans}")
        
        if not is_single_turn and i < len(example['turns']) - 1:
            print()  # Add blank line between turns in multi-turn conversations
    
    print("\n" + "-" * 60 + "\n")  # Add separator between examples


split_to_use = "validation"
feature_vocabularies = prepare_feature_vocabularies(dataset[split_to_use])
print_conversation(example, feature_vocabularies)

