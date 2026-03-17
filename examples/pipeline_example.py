"""
Octopai Pipeline Example

This example demonstrates how to use Octopai's proprietary pipeline
for complete skill development from creation to optimization.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from octopai import Octopai, PipelineStage


def example_create_from_url():
    """Example: Create a skill from a URL"""
    print("=" * 60)
    print("Octopai Pipeline Example - Create from URL")
    print("=" * 60)
    
    octopai = Octopai()
    
    # Register callback for pipeline stages
    def on_stage_complete(result):
        print(f"\n✓ Stage completed: {result.stage.value}")
        if result.skill_id:
            print(f"  Skill ID: {result.skill_id}")
    
    octopai.pipeline.register_callback(PipelineStage.CREATION, on_stage_complete)
    octopai.pipeline.register_callback(PipelineStage.OPTIMIZATION, on_stage_complete)
    octopai.pipeline.register_callback(PipelineStage.PACKAGING, on_stage_complete)
    octopai.pipeline.register_callback(PipelineStage.VALIDATION, on_stage_complete)
    
    # Note: This is just an example - uncomment to run with actual URL
    # result = octopai.create_from_url(
    #     url="https://example.com/documentation",
    #     name="Example Skill",
    #     description="A skill created from web documentation",
    #     tags=["example", "web", "documentation"]
    # )
    
    print("\nExample setup complete!")
    print("To use this example, uncomment the create_from_url call with a real URL.")


def example_create_from_prompt():
    """Example: Create a skill from a prompt"""
    print("\n" + "=" * 60)
    print("Octopai Pipeline Example - Create from Prompt")
    print("=" * 60)
    
    octopai = Octopai(auto_optimize=False, auto_package=False)
    
    # Note: This is just an example - uncomment to run
    # result = octopai.create_from_prompt(
    #     prompt="Create a skill that helps analyze CSV data files and generate visualizations",
    #     name="CSV Analysis Skill",
    #     description="Analyzes CSV data and creates meaningful visualizations",
    #     tags=["data", "analysis", "visualization", "csv"],
    #     category="Data Science"
    # )
    
    print("\nExample setup complete!")
    print("To use this example, uncomment the create_from_prompt call.")


def example_skill_management():
    """Example: Manage skills with SkillHub"""
    print("\n" + "=" * 60)
    print("Octopai Skill Management Example")
    print("=" * 60)
    
    octopai = Octopai()
    
    # List skills in SkillHub
    print("\nListing skills in SkillHub:")
    skills = octopai.list_skills_in_hub(limit=10)
    for skill in skills:
        print(f"  - {skill.name}")
    
    # Search for skills
    print("\nSearching for skills:")
    results = octopai.search_skills_in_hub("data", limit=5)
    for skill in results:
        print(f"  - {skill.name}")
    
    # Get SkillHub stats
    print("\nSkillHub Statistics:")
    stats = octopai.get_skill_hub_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_experience_tracking():
    """Example: Experience tracking and insights"""
    print("\n" + "=" * 60)
    print("Octopai Experience Tracking Example")
    print("=" * 60)
    
    octopai = Octopai()
    
    # Get overall insights
    print("\nOverall Experience Insights:")
    insights = octopai.get_experience_insights()
    print(f"  Generated at: {insights.get('generated_at')}")
    print(f"  Scope: {insights.get('scope')}")
    
    if 'ecosystem_insights' in insights:
        eco_insights = insights['ecosystem_insights']
        print(f"\nEcosystem Insights:")
        for key, value in eco_insights.items():
            print(f"  {key}: {value}")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Octopai - Proprietary Skill Development Platform")
    print("=" * 60)
    
    example_create_from_url()
    example_create_from_prompt()
    example_skill_management()
    example_experience_tracking()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
