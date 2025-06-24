"""
Time tracking module for Codex-AI.

Contains time analysis functionality (ported from JavaScript):
- calculator: Core time calculation algorithms
- report_generator: Time tracking report generation
- complexity_analyzer: Code complexity analysis (TODO)
- algorithms: Pure time calculation functions (TODO)
"""

# Import main classes and functions
try:
    from .calculator import (
        TimeCalculator, CommitStats, TimeEstimate, CommitAnalysis,
        ComplexityType, ComplexityLevel, CommitType,
        analyze_repository_time, calculate_commit_time
    )
    CALCULATOR_AVAILABLE = True
except ImportError:
    CALCULATOR_AVAILABLE = False

try:
    from .report_generator import (
        ReportGenerator, TimeTrackingReport, ProjectStats, DeveloperStats,
        MonthlyStats, DeveloperTypeStats, generate_time_report,
        generate_report_from_analysis_file, create_full_time_report
    )
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False

# Module availability
TIMETRACKER_AVAILABLE = CALCULATOR_AVAILABLE and REPORT_GENERATOR_AVAILABLE

__all__ = [
    # Main classes
    "TimeCalculator",
    "ReportGenerator",
    
    # Data classes
    "CommitStats",
    "TimeEstimate", 
    "CommitAnalysis",
    "TimeTrackingReport",
    "ProjectStats",
    "DeveloperStats",
    "MonthlyStats",
    "DeveloperTypeStats",
    
    # Constants
    "ComplexityType",
    "ComplexityLevel", 
    "CommitType",
    
    # Convenience functions
    "analyze_repository_time",
    "calculate_commit_time",
    "generate_time_report",
    "generate_report_from_analysis_file",
    "create_full_time_report",
    
    # Availability flags
    "CALCULATOR_AVAILABLE",
    "REPORT_GENERATOR_AVAILABLE",
    "TIMETRACKER_AVAILABLE"
]
