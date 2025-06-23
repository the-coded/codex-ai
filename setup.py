"""
Setup configuration for codex-ai package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

# Read requirements from requirements.txt
def read_requirements(filename):
    """Read requirements from file, filtering out comments and empty lines."""
    requirements_file = Path(__file__).parent / filename
    if not requirements_file.exists():
        return []
    
    requirements = []
    with open(requirements_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments, empty lines, and -r includes
            if line and not line.startswith('#') and not line.startswith('-r'):
                requirements.append(line)
    return requirements

# Core requirements
requirements = read_requirements('requirements.txt')


setup(
    name="codex-ai",
    version="1.0.0",
    author="the-coded",
    author_email="gabriel@laplanta.com.br",
    description="AI-powered development toolkit for changelog generation, time tracking, and code analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/the-coded/codex-ai",
    project_urls={
        "Bug Reports": "https://github.com/the-coded/codex-ai/issues",
        "Source": "https://github.com/the-coded/codex-ai",
        "Documentation": "https://github.com/the-coded/codex-ai#readme",
    },
    
    # Package configuration
    py_modules=[
        "cli", "config", "__main__"
    ],
    packages=[
        "commands", "core", "core.git", "core.time", "core.ai", "core.uidocs",
        "constants", "utils", "formatters"
    ],
    
    # Entry points
    entry_points={
        "console_scripts": [
            "codex-ai=cli:main",
        ],
    },
    
    # Dependencies
    install_requires=requirements,
    python_requires=">=3.8",
    
    # Package metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords=[
        "ai", "artificial-intelligence", "git", "changelog", "documentation", 
        "time-tracking", "development-tools", "claude", "automation", 
        "code-analysis", "project-management", "developer-experience"
    ],
    
    # Package data
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yaml", "*.yml", "*.json"],
        "templates": ["**/*.md"],
    },
    
    # Additional metadata
    zip_safe=False,
    platforms=["any"],
)
