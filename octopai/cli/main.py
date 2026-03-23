import click
import os
from octopai.core.converter import URLConverter
from octopai.core.skill_factory import SkillFactory
from octopai.core.skill_hub import SkillHub
from octopai.core.evolution_engine import EvolutionEngine
from octopai.core.pipeline import OctopaiPipeline
from octopai.utils.helpers import ensure_directory


@click.group()
def cli():
    """Octopai - Explore, Extend, Evolve AI Agent Cognition."""
    pass


@cli.command()
@click.option('--url', required=True, help='URL to convert')
@click.option('--name', required=True, help='skill name')
@click.option('--description', required=True, help='skill description')
@click.option('--output', default='./skills', help='output directory')
@click.option('--category', default=None, help='skill category')
@click.option('--author', default=None, help='skill author')
@click.option('--tags', default=None, help='comma-separated tags')
def create(url, name, description, output, category, author, tags):
    """Create a skill from URL with full lifecycle (create -> optimize -> package)"""
    ensure_directory(output)

    tag_list = [t.strip() for t in tags.split(',')] if tags else None

    pipeline = OctopaiPipeline()
    result = pipeline.create_from_url(
        url=url,
        name=name,
        description=description,
        tags=tag_list,
        category=category,
        author=author
    )

    if result.success:
        click.echo(f"Skill created successfully!")
        click.echo(f"Skill ID: {result.skill_id}")
        click.echo(f"Skill directory: {result.skill_dir}")
    else:
        click.echo(f"Skill creation failed: {', '.join(result.errors)}")


@cli.command()
@click.option('--skill', required=True, help='skill directory')
@click.option('--iterations', default=10, help='number of evolution iterations')
def evolve(skill, iterations):
    """Evolve skill content using Octopai's evolution engine"""
    from octopai.core.evolution_engine import EvolutionConfig

    config = EvolutionConfig(max_iterations=iterations)
    engine = EvolutionEngine(config=config)

    try:
        evolved_dir = engine.evolve_skill(skill, config=config)
        click.echo(f"Evolution complete! Skill updated: {evolved_dir}")
    except Exception as e:
        click.echo(f"Evolution failed: {str(e)}")


@cli.command()
@click.option('--name', required=True, help='skill name')
@click.option('--description', required=True, help='skill description')
@click.option('--prompt', required=True, help='skill prompt/description')
@click.option('--output', default='./skills', help='output directory')
@click.option('--category', default=None, help='skill category')
@click.option('--author', default=None, help='skill author')
def prompt(name, description, prompt_text, output, category, author):
    """Create a skill from a prompt/description"""
    ensure_directory(output)

    factory = SkillFactory()
    skill_def = factory.create_from_prompt(
        prompt=prompt_text,
        name=name,
        description=description,
        category=category,
        author=author
    )

    click.echo(f"Skill created from prompt!")
    click.echo(f"Skill ID: {skill_def.metadata.skill_id}")


@cli.command()
@click.option('--skill', required=True, help='skill ID')
def info(skill):
    """Show skill information"""
    hub = SkillHub()
    skill_obj = hub.get_skill(skill)

    if skill_obj:
        click.echo(f"Name: {skill_obj.metadata.name}")
        click.echo(f"Description: {skill_obj.metadata.description}")
        click.echo(f"Category: {skill_obj.metadata.category}")
        click.echo(f"Tags: {', '.join(skill_obj.metadata.tags)}")
        click.echo(f"Version: {skill_obj.metadata.version}")
        click.echo(f"Status: {skill_obj.metadata.status.value}")
        click.echo(f"Usage count: {skill_obj.metadata.usage_count}")
    else:
        click.echo(f"Skill not found: {skill}")


@cli.command()
@click.option('--skill', required=True, help='skill directory')
def validate(skill):
    """Validate a skill package"""
    from octopai.core.skill_packager import SkillPackager

    packager = SkillPackager()
    is_valid, issues = packager.validate_package(skill)

    if is_valid:
        click.echo(f"Skill package is valid: {skill}")
    else:
        click.echo(f"Validation issues found:")
        for issue in issues:
            click.echo(f"  - {issue}")


@cli.command()
@click.option('--query', default='', help='search query')
@click.option('--category', default=None, help='filter by category')
@click.option('--limit', default=10, help='maximum results')
def search(query, category, limit):
    """Search for skills in SkillHub"""
    hub = SkillHub()

    if query:
        results = hub.search_skills(query, category=category, limit=limit)
    else:
        results = hub.list_skills(category=category, limit=limit)

    if results:
        click.echo(f"Found {len(results)} skills:")
        for s in results:
            click.echo(f"  - {s.metadata.name} ({s.metadata.skill_id})")
    else:
        click.echo("No skills found.")


@cli.command()
@click.option('--urls', required=True, help='File containing URL list')
@click.option('--output', default='./skills', help='output directory')
def batch(urls, output):
    """Batch process URL list"""
    ensure_directory(output)

    with open(urls, 'r') as f:
        url_list = [line.strip() for line in f if line.strip()]

    pipeline = OctopaiPipeline()

    for i, url in enumerate(url_list):
        try:
            click.echo(f"Processing ({i+1}/{len(url_list)}): {url}")
            result = pipeline.create_from_url(
                url=url,
                name=f"Skill from URL {i+1}",
                description=f"Skill created from URL"
            )
            if result.success:
                click.echo(f"  Success: {result.skill_id}")
            else:
                click.echo(f"  Failed: {', '.join(result.errors)}")
        except Exception as e:
            click.echo(f"  Error: {str(e)}")

    click.echo("Batch processing complete!")


@cli.command()
def version():
    """Show version information"""
    click.echo("Octopai v0.1.0")


@cli.command()
def stats():
    """Show SkillHub statistics"""
    hub = SkillHub()
    stats = hub.get_statistics()

    click.echo("=== Octopai Statistics ===")
    click.echo(f"Total Skills: {stats['total_skills']}")
    click.echo(f"Total Versions: {stats['total_versions']}")
    click.echo(f"Total Usage: {stats['total_usage']}")
    click.echo(f"Average Success Rate: {stats['average_success_rate']:.2%}")
    click.echo(f"Categories: {', '.join(stats['categories'].keys())}")


if __name__ == '__main__':
    cli()
