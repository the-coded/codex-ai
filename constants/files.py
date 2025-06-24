"""
File-related constants for categorization and processing.

This module contains only the essential file type constants actually used
by the Codex-AI system, based on the existing timetracker and uidocs functionality.
"""

from typing import Dict, List, Set

# ===== ESSENTIAL FILE CATEGORIES =====
#
# 📊 EXPLANATION:
# Only the 4 categories actually used by the timetracker system.
# Based on: old/pkg/timetracker/analyze-git-changes.js

FILE_CATEGORIES = {
    "LOGIC": {
        "extensions": ["js", "ts", "jsx", "tsx"],
        "description": "Programming logic files"
    },
    "STYLE": {
        "extensions": ["css", "scss", "sass", "less", "stylus"],
        "description": "Stylesheet files"
    },
    "CONFIG": {
        "extensions": ["json", "yml", "yaml", "lock", "gitignore", "npmrc", "env"],
        "description": "Configuration files"
    },
    "DOCS": {
        "extensions": ["md", "mdx", "txt", "doc", "docx", "html"],
        "description": "Documentation files"
    }
}

# ===== COMPLEXITY PATTERNS =====
#
# 📊 EXPLANATION:
# Directory patterns used by timetracker for complexity analysis.
# Directly from: old/pkg/timetracker/analyze-git-changes.js

STRUCTURAL_PATTERNS = [
    "/components/",
    "/layouts/", 
    "/pages/",
    "/views/",
    "/styles/",
    "/assets/",
    "/themes/"
]

ALGORITHMIC_PATTERNS = [
    "/utils/",
    "/helpers/",
    "/services/",
    "/hooks/",
    "/commands/",
    "/lib/",
    "/core/"
]

# File types for complexity scoring
STRUCTURAL_FILE_TYPES = ["css", "scss", "less", "html", "jsx", "tsx", "svg"]
ALGORITHMIC_FILE_TYPES = ["js", "ts", "jsx", "tsx"]

# ===== uidocs PATTERNS =====
#
# 📊 EXPLANATION:
# Patterns used by uidocs system for file type detection.
# Based on existing uidocs functionality.

uidocs_PATTERNS = {
    "REACT": [
        r"components?/.*\.(jsx|tsx)$",
        r".*\.component\.(jsx|tsx)$",
        r"pages?/.*\.(jsx|tsx)$"
    ],
    "SASS": [
        r".*\.(scss|sass)$",
        r"styles?/.*\.css$"
    ],
    "STORYBOOK": [
        r".*\.stories\.(js|ts|jsx|tsx)$",
        r"stories/.*\.(js|ts|jsx|tsx)$"
    ]
}

# ===== SPECIAL FILE PATTERNS =====
#
# 📊 EXPLANATION:
# Only the essential special patterns actually used.

SPECIAL_PATTERNS = {
    "TEST": [
        r"\.test\.(js|ts|jsx|tsx)$",
        r"\.spec\.(js|ts|jsx|tsx)$"
    ],
    "STORIES": [
        r"\.stories\.(js|ts|jsx|tsx)$"
    ]
}

# ===== HELPER FUNCTIONS =====

def get_file_extension(filename: str) -> str:
    """
    Extract file extension, handling special cases like .stories.tsx
    
    Based on: old/pkg/timetracker/analyze-git-changes.js getFileExtension()
    """
    import re
    
    # Check for special patterns like .stories.tsx or .test.ts
    special_match = re.search(r'\.(stories|test|spec)\.([a-zA-Z0-9]+)(?:\})?$', filename)
    if special_match:
        return special_match.group(2)  # Return actual extension (ts/tsx)
    
    # Get base extension
    base_match = re.search(r'\.([a-zA-Z0-9]+)(?:\})?$', filename)
    if base_match:
        return base_match.group(1)
    
    return 'unknown'


def get_file_category(file_type: str) -> str:
    """
    Get file category based on extension.
    
    Returns:
        str: Category name or 'UNKNOWN'
    """
    file_type = file_type.lower()
    
    for category, info in FILE_CATEGORIES.items():
        if file_type in info["extensions"]:
            return category
    
    return "UNKNOWN"


def is_structural_file(file_type: str) -> bool:
    """Check if file type is structural (for complexity analysis)."""
    return file_type.lower() in STRUCTURAL_FILE_TYPES


def is_algorithmic_file(file_type: str) -> bool:
    """Check if file type is algorithmic (for complexity analysis)."""
    return file_type.lower() in ALGORITHMIC_FILE_TYPES


def matches_pattern(filepath: str, patterns: List[str]) -> bool:
    """Check if filepath matches any of the given patterns."""
    import re
    
    for pattern in patterns:
        if re.search(pattern, filepath):
            return True
    return False


def is_react_file(filepath: str) -> bool:
    """Check if file is a React component."""
    return matches_pattern(filepath, uidocs_PATTERNS["REACT"])


def is_sass_file(filepath: str) -> bool:
    """Check if file is a Sass/SCSS file."""
    return matches_pattern(filepath, uidocs_PATTERNS["SASS"])


def is_storybook_file(filepath: str) -> bool:
    """Check if file is a Storybook story."""
    return matches_pattern(filepath, uidocs_PATTERNS["STORYBOOK"])


def get_all_extensions() -> Set[str]:
    """Get all known file extensions."""
    extensions = set()
    for category in FILE_CATEGORIES.values():
        extensions.update(category["extensions"])
    return extensions


# ===== EXPORT CONSTANTS =====

__all__ = [
    # Main constants
    "FILE_CATEGORIES",
    "STRUCTURAL_PATTERNS",
    "ALGORITHMIC_PATTERNS", 
    "STRUCTURAL_FILE_TYPES",
    "ALGORITHMIC_FILE_TYPES",
    "uidocs_PATTERNS",
    "SPECIAL_PATTERNS",
    
    # Helper functions
    "get_file_extension",
    "get_file_category",
    "is_structural_file",
    "is_algorithmic_file",
    "matches_pattern",
    "is_react_file",
    "is_sass_file", 
    "is_storybook_file",
    "get_all_extensions"
]
