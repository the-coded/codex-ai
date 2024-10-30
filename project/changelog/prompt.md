You will act as a changelog generator.
Please think step by step and provide the necessary information.

Follow the template in .nexus/project/changelog/template.md for our output changelog.

Please create our changelog according to the log file attached: 
- Analyze the commit messages
- Analyze the commit file changes
- Analyze the whole file that had changes

Include the following sections in your changelog:

1. Summary: Provide a brief overview of the main changes and improvements in this version.

2. Description: Include an overall analysis of the release changes, focusing on the main objectives and impact on the project.

3. Breaking Changes: List any changes that break compatibility with previous versions.

4. Added: List new features or functionalities added.

5. Changed: Describe changes to existing functionalities.

6. Deprecated: Mention features that will be removed in future versions.

7. Removed: List features that were removed in this version.

8. Fixed: Describe bug fixes.

9. Security: Mention vulnerability fixes or security improvements.

10. Dependencies: List updates or changes to project dependencies.

11. Documentation: Describe significant updates to documentation.

12. Tests: Mention changes to tests or test coverage.

13. Performance: Describe performance improvements or issues.

14. Known Issues: List known issues or limitations in this version.

For each section, differentiate between backend and frontend changes where applicable. Provide specific examples for each type of change, similar to the examples in the template.

Include a section for each "Commit Details" with the following information:
- Commit message
- Commit date
- Commit author
- Commit short_hash

Include a section for the "File Changes" for each commit, with the following information:
- File name
- File short_hash
- File changes
- Description of the changes

Include links to relevant issues or pull requests using [#Number] format.

Add a "Contributor Acknowledgements" section to recognize the contributions of both backend and frontend developers.

You will create a file changelog.md with our output changelog.
