from collections import defaultdict

def filter_versions(versions):
    """
    Filter versions to keep the latest 2 minor version groups (excluding 1.0.0x).
    Returns a tuple of (versions_to_keep, versions_to_delete).
    """
    # Filter out 1.0.0x versions and group by first 5 characters
    filtered_versions = [v for v in versions if v[:5] != "1.0.0"]
    
    # Group by first 5 characters (e.g., "1.0.1", "1.0.2", "1.1.0")
    groups = defaultdict(list)
    for version in filtered_versions:
        group_key = version[:5]
        groups[group_key].append(version)
    
    # Sort groups by key in descending order and take first 2
    sorted_groups = sorted(groups.items(), key=lambda x: x[0], reverse=True)
    top_2_groups = sorted_groups[:2]
    
    # Flatten the top 2 groups to get versions to keep
    to_keep = []
    for _, group_versions in top_2_groups:
        to_keep.extend(group_versions)
    
    # Get versions to delete (everything not in to_keep)
    to_delete = [v for v in versions if v not in to_keep]
    
    return to_keep, to_delete


def display_results(to_keep, to_delete):
    """Display the results in a formatted way."""
    print("=== Images to KEEP ===")
    for version in to_keep:
        print(f"  ✓ {version}")
    
    print("\n=== Images to DELETE ===")
    for version in to_delete:
        print(f"  ✗ {version}")


def main():
    versions = ["1.0.01", "1.0.02", "1.0.10", "1.0.20", "1.0.23", 
                "1.0.32", "1.0.34", "1.0.42", "1.1.00"]
    
    to_keep, to_delete = filter_versions(versions)
    display_results(to_keep, to_delete)
    
    return to_keep, to_delete


if __name__ == "__main__":
    kept, deleted = main()
