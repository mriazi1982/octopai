"""
Octopai Simple Quickstart - Core Features
==========================================
A simple, easy-to-use script demonstrating Octopai's core functionality.
You can run this directly or integrate it into your own projects!
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from octopai import (
    Octopai,
    create_from_prompt,
    create_from_text,
    parse,
    hub_create,
    hub_list,
    hub_search,
    hub_stats,
    hub_create_collection,
    hub_semantic_search,
    hub_publish,
    hub_add_rating,
    get_insights
)


def section_header(title):
    """Print a section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_1_basic_initialization():
    """Demo 1: Basic initialization"""
    section_header("1. Basic Initialization")
    print("Initializing Octopai...")
    
    # Initialize Octopai with default settings
    octopai = Octopai()
    print("✓ Octopai initialized successfully!")
    print("  - You're ready to use all Octopai features")
    print("  - Skills will be stored in ./SkillHub directory")
    return octopai


def demo_2_create_from_prompt():
    """Demo 2: Create skill from a simple prompt"""
    section_header("2. Create Skill from Prompt")
    print("Creating a skill from a simple description...")
    
    # Create a skill using the simple convenience function
    skill = create_from_prompt(
        prompt="Create a skill for generating Python unit tests",
        name="Python Unit Test Generator",
        description="Generates comprehensive unit tests for Python functions",
        tags=["python", "testing", "unit-tests"],
        category="development"
    )
    
    print(f"✓ Skill created!")
    print(f"  Name: {skill.metadata.name}")
    print(f"  Version: v{skill.latest_version.version}")
    return skill


def demo_3_create_from_text():
    """Demo 3: Create skill from text content"""
    section_header("3. Create Skill from Text")
    print("Creating a skill from raw text content...")
    
    # Any text can become a skill!
    text_content = """
    # Data Visualization Best Practices
    
    ## Key Principles
    1. Keep it simple and focused
    2. Use appropriate chart types
    3. Label everything clearly
    4. Use color strategically
    
    ## Common Chart Types
    - Bar charts: Compare categories
    - Line charts: Show trends over time
    - Scatter plots: Show correlations
    """
    
    skill = create_from_text(
        text=text_content,
        name="Data Visualization Guide",
        description="Best practices for creating effective data visualizations",
        tags=["visualization", "data", "design"],
        category="data-science"
    )
    
    print(f"✓ Skill created from text!")
    print(f"  Name: {skill.metadata.name}")
    print(f"  Category: {skill.metadata.category}")
    return skill


def demo_4_skill_hub_basics(octopai):
    """Demo 4: SkillHub basics - create, list, search"""
    section_header("4. SkillHub - Manage Your Skills")
    
    # Create a skill in SkillHub
    print("\nCreating a skill in SkillHub...")
    skill = hub_create(
        name="CSV Data Analyzer",
        description="Analyze and visualize CSV data files",
        prompt="Create a comprehensive skill for working with CSV data",
        tags=["csv", "data", "analysis"],
        category="data-processing"
    )
    
    print(f"✓ Skill created in SkillHub!")
    print(f"  Skill ID: {skill.metadata.skill_id}")
    skill_id = skill.metadata.skill_id
    
    # List all skills
    print("\nListing all skills in SkillHub...")
    all_skills = hub_list()
    print(f"✓ Found {len(all_skills)} skills")
    for i, s in enumerate(all_skills[:3], 1):
        print(f"  {i}. {s.name}")
    
    # Search skills
    print("\nSearching for 'data' skills...")
    search_results = hub_search("data", category="data-processing")
    print(f"✓ Found {len(search_results)} matching skills")
    
    # Get statistics
    print("\nGetting SkillHub statistics...")
    stats = hub_stats()
    print(f"✓ Statistics:")
    print(f"  Total skills: {stats.get('total_skills', 0)}")
    print(f"  Total categories: {stats.get('total_categories', 0)}")
    
    return skill_id


def demo_5_collections_and_organization(skill_id):
    """Demo 5: Organize skills into collections"""
    section_header("5. Skill Collections - Organize Your Skills")
    
    # Create a collection
    print("\nCreating a skill collection...")
    collection = hub_create_collection(
        name="Data Science Toolkit",
        description="Essential skills for data science work",
        skill_ids=[skill_id],
        tags=["data-science", "tools", "essential"]
    )
    
    print(f"✓ Collection created!")
    print(f"  Name: {collection.name}")
    print(f"  Skills in collection: {len(collection.skill_ids)}")
    
    # List all collections
    print("\nListing all collections...")
    collections = hub_list_collections()
    print(f"✓ Found {len(collections)} collections")
    return collection.collection_id


def demo_6_semantic_search_and_publishing(skill_id):
    """Demo 6: Semantic search and publishing workflow"""
    section_header("6. Semantic Search & Publishing")
    
    # Semantic search (more intelligent than keyword search)
    print("\nPerforming semantic search...")
    semantic_results = hub_semantic_search(
        "analyze spreadsheet files",
        category="data-processing"
    )
    print(f"✓ Semantic search found {len(semantic_results)} results")
    for i, (skill, score) in enumerate(semantic_results[:3], 1):
        print(f"  {i}. {skill.name} (relevance: {score:.2f})")
    
    # Publish the skill
    print("\nPublishing the skill...")
    published = hub_publish(skill_id)
    if published:
        print(f"✓ Skill published!")
        print(f"  Status: {published.metadata.status}")
        print(f"  Visibility: {published.metadata.visibility}")
    
    # Add a rating
    print("\nAdding a rating to the skill...")
    rating = hub_add_rating(
        skill_id=skill_id,
        rating=5.0,
        feedback="This skill is very useful for CSV analysis!",
        reviewer="User"
    )
    if rating:
        print(f"✓ Rating added!")
        print(f"  Rating: {rating.rating}/5.0")


def demo_7_everything_is_a_skill(octopai):
    """Demo 7: Demonstrate the 'Everything Can Be a Skill' philosophy"""
    section_header("7. Everything Can Be a Skill!")
    
    print("Octopai can transform ANYTHING into a skill:")
    print("  - Text content ✓")
    print("  - Web URLs ✓")
    print("  - Files (PDF, DOC, Excel, etc.) ✓")
    print("  - Code snippets ✓")
    print("  - Prompts and ideas ✓")
    print("  - Even Python dictionaries and objects! ✓")
    
    # Example: Create from a Python dictionary
    print("\nCreating a skill from a Python dictionary...")
    data_dict = {
        "topic": "Machine Learning Algorithms",
        "types": ["Supervised", "Unsupervised", "Reinforcement"],
        "examples": ["Regression", "Classification", "Clustering"],
        "tools": ["scikit-learn", "TensorFlow", "PyTorch"]
    }
    
    skill = octopai.create_anything(
        source=data_dict,
        name="ML Algorithms Overview",
        description="Quick reference for machine learning algorithm types",
        tags=["ml", "algorithms", "reference"],
        category="ai"
    )
    
    print(f"✓ Skill created from dictionary!")
    print(f"  Name: {skill.metadata.name}")


def demo_8_integration_pattern():
    """Demo 8: How to integrate Octopai into your own projects"""
    section_header("8. Integrate Octopai Into Your Projects")
    
    print("Octopai is designed to be easily integrated into any Python project!")
    print("\nExample patterns:")
    
    print("\nPattern 1: Use convenience functions (simplest)")
    print("""
    from octopai import create_from_prompt, hub_create, hub_search
    
    # Create a skill
    skill = create_from_prompt(
        prompt="Create a skill for my task",
        name="My Skill",
        description="Does something amazing"
    )
    
    # Search for existing skills
    results = hub_search("task automation")
    """)
    
    print("\nPattern 2: Use Octopai class (more control)")
    print("""
    from octopai import Octopai
    
    # Initialize with custom settings
    octopai = Octopai(
        skill_hub_dir="./my_skills",
        experience_dir="./my_experiences"
    )
    
    # Use all features through the instance
    skill = octopai.create_skill_in_hub(
        name="Custom Skill",
        description="My custom skill",
        prompt="Create something special"
    )
    """)
    
    print("\nPattern 3: Import only what you need")
    print("""
    from octopai import hub_list, hub_stats, hub_semantic_search
    
    # Just use SkillHub features
    skills = hub_list(category="data-science")
    stats = hub_stats()
    results = hub_semantic_search("machine learning")
    """)


def demo_9_get_insights():
    """Demo 9: Get experience insights"""
    section_header("9. Experience & Insights")
    
    print("Octopai tracks skill usage and provides insights!")
    print("\nGetting insights...")
    
    insights = get_insights()
    print(f"✓ Insights available:")
    print(f"  Total interactions: {insights.get('total_interactions', 0)}")
    print(f"  Success rate: {insights.get('success_rate', 0):.1%}")


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("  🐙 Octopai - Simple Quickstart")
    print("="*70)
    print("\nWelcome to Octopai!")
    print("This script will demonstrate all core features in simple steps.")
    print("You can copy these patterns directly into your own projects!")
    
    try:
        # Run all demos
        octopai = demo_1_basic_initialization()
        demo_2_create_from_prompt()
        demo_3_create_from_text()
        skill_id = demo_4_skill_hub_basics(octopai)
        demo_5_collections_and_organization(skill_id)
        demo_6_semantic_search_and_publishing(skill_id)
        demo_7_everything_is_a_skill(octopai)
        demo_8_integration_pattern()
        demo_9_get_insights()
        
        # Summary
        print("\n" + "="*70)
        print("  ✓ All demos completed successfully!")
        print("="*70)
        print("\nNext Steps:")
        print("  1. Explore the examples directory for more advanced usage")
        print("  2. Check out the README for complete documentation")
        print("  3. Try creating your own skills with real content")
        print("  4. Integrate Octopai into your projects!")
        print("\nRemember: Everything Can Be a Skill! 🐙")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nNote: Some features may require API keys for full functionality.")
        print("Check the .env.example file for configuration.")


if __name__ == "__main__":
    main()
