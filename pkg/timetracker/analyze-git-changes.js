const { execSync } = require('child_process');
const fs = require('fs');

// Constants for time estimation
const TIME_FACTORS = {
  PLANNING: {
    BASE: {
      FEATURE: 0.5,    // Base planning time for features
      FIX: 0.15,       // Base planning time for fixes
      PUBLISH: 0.1,    // Base planning time for publishes
      DEFAULT: 0.25    // Base planning time for other changes
    },
    COMPLEXITY_MULTIPLIER: {
      LOW: 1,
      MEDIUM: 2,
      HIGH: 3
    },
    SIZE_MULTIPLIER: (lines) => {
      if (lines <= 5) return 0.5;      // Tiny changes
      if (lines <= 20) return 1;       // Small changes
      if (lines <= 100) return 1.5;    // Medium changes
      if (lines <= 500) return 2;      // Large changes
      return 3;                        // Huge changes
    }
  },
  IMPLEMENTATION: {
    PER_LINE: 0.05,  // Base hours per line
    COMPLEXITY: {
      LOW: 1,
      MEDIUM: 1.5,
      HIGH: 2
    }
  }
};

// Get commit type from message
function getCommitType(message) {
  if (message.startsWith('feat:')) return 'FEATURE';
  if (message.startsWith('fix:')) return 'FIX';
  if (message.includes('Publish') || message.includes('v0.')) return 'PUBLISH';
  return 'DEFAULT';
}

// Calculate complexity based on changes
function calculateComplexity(stats) {
  const score = (
    (stats.filesChanged * 0.3) +
    ((stats.additions + stats.deletions) * 0.5) +
    (Object.keys(stats.fileTypes).length * 0.2)
  );

  if (score > 100) return 'HIGH';
  if (score > 50) return 'MEDIUM';
  return 'LOW';
}

// Get detailed git log with patches
function getDetailedGitLog() {
  // Get detailed git log with stats and patch
  const log = execSync('git log --pretty=format:"%h|%an|%ad|%s" --date=format:"%Y-%m-%d %H:%M:%S" --numstat').toString();
  const commits = [];
  let currentCommit = null;

  log.split('\n').forEach(line => {
    if (line.includes('|')) {
      // This is a commit header
      if (currentCommit) {
        commits.push(currentCommit);
      }
      const [hash, author, date, message] = line.split('|');
      currentCommit = {
        hash,
        author,
        date,
        message,
        stats: {
          filesChanged: 0,
          additions: 0,
          deletions: 0,
          fileTypes: {},
          files: []
        }
      };
    } else if (line.trim() && currentCommit) {
      // This is a file stat line
      const [additions, deletions, file] = line.split('\t');
      if (file) {
        const fileType = file.split('.').pop() || 'unknown';
        currentCommit.stats.fileTypes[fileType] = (currentCommit.stats.fileTypes[fileType] || 0) + 1;
        currentCommit.stats.filesChanged++;
        currentCommit.stats.files.push(file);
        currentCommit.stats.additions += parseInt(additions) || 0;
        currentCommit.stats.deletions += parseInt(deletions) || 0;
      }
    }
  });

  if (currentCommit) {
    commits.push(currentCommit);
  }

  return commits.map(commit => {
    const type = getCommitType(commit.message);
    const complexity = calculateComplexity(commit.stats);
    
    // Calculate time estimates
    const totalLines = commit.stats.additions + commit.stats.deletions;
    const planningHours = TIME_FACTORS.PLANNING.BASE[type] * 
      TIME_FACTORS.PLANNING.COMPLEXITY_MULTIPLIER[complexity] *
      TIME_FACTORS.PLANNING.SIZE_MULTIPLIER(totalLines);
    
    const implementationHours = totalLines * 
      TIME_FACTORS.IMPLEMENTATION.PER_LINE * 
      TIME_FACTORS.IMPLEMENTATION.COMPLEXITY[complexity];

    return {
      hash: commit.hash,
      author: commit.author,
      date: commit.date,
      message: commit.message,
      type,
      complexity,
      stats: commit.stats,
      timeEstimates: {
        planning: planningHours,
        implementation: implementationHours,
        total: planningHours + implementationHours
      }
    };
  });
}

// Generate markdown report
function generateMarkdown(commits) {
  let markdown = '# Git Changes Analysis\n\n';

  // Overall Statistics
  const totalStats = commits.reduce((acc, commit) => {
    acc.filesChanged += commit.stats.filesChanged;
    acc.additions += commit.stats.additions;
    acc.deletions += commit.stats.deletions;
    acc.totalHours += commit.timeEstimates.total;
    return acc;
  }, { filesChanged: 0, additions: 0, deletions: 0, totalHours: 0 });

  const complexityCount = commits.reduce((acc, commit) => {
    acc[commit.complexity] = (acc[commit.complexity] || 0) + 1;
    return acc;
  }, {});

  markdown += '## Overall Statistics\n';
  markdown += `- Total Commits: ${commits.length}\n`;
  markdown += `- Total Files Changed: ${totalStats.filesChanged}\n`;
  markdown += `- Total Lines Added: ${totalStats.additions}\n`;
  markdown += `- Total Lines Deleted: ${totalStats.deletions}\n`;
  markdown += `- Total Hours Estimated: ${totalStats.totalHours.toFixed(2)}\n\n`;

  // Commits Detail
  markdown += '## Commits Detail\n\n';
  commits.forEach(commit => {
    markdown += `### ${commit.hash} - ${commit.date} - ${commit.message}\n`;
    markdown += `- **Type**: ${commit.type}\n`;
    markdown += `- **Complexity**: ${commit.complexity}\n`;
    markdown += '- **Changes**:\n';
    markdown += `  * Files: ${commit.stats.filesChanged}\n`;
    markdown += `  * Added: ${commit.stats.additions} lines\n`;
    markdown += `  * Deleted: ${commit.stats.deletions} lines\n`;
    markdown += `  * Net: ${commit.stats.additions - commit.stats.deletions} lines\n`;
    markdown += '- **File Types**:\n';
    Object.entries(commit.stats.fileTypes).forEach(([type, count]) => {
      markdown += `  * ${type}: ${count} files\n`;
    });
    markdown += '- **Time Estimates**:\n';
    markdown += `  * Planning: ${commit.timeEstimates.planning.toFixed(2)} hours\n`;
    markdown += `  * Implementation: ${commit.timeEstimates.implementation.toFixed(2)} hours\n`;
    markdown += `  * Total: ${commit.timeEstimates.total.toFixed(2)} hours\n\n`;
  });

  // Complexity Analysis
  markdown += '## Complexity Analysis\n';
  Object.entries(complexityCount).forEach(([complexity, count]) => {
    const percentage = ((count / commits.length) * 100).toFixed(1);
    markdown += `- ${complexity} Complexity Changes: ${percentage}% (${count} commits)\n`;
  });
  markdown += '\n';

  // File Type Impact
  const fileTypeStats = commits.reduce((acc, commit) => {
    Object.entries(commit.stats.fileTypes).forEach(([type, count]) => {
      if (!acc[type]) {
        acc[type] = { files: 0, additions: 0, deletions: 0, hours: 0 };
      }
      acc[type].files += count;
      // Estimate proportional lines and hours for each file type
      const typeRatio = count / commit.stats.filesChanged;
      acc[type].additions += commit.stats.additions * typeRatio;
      acc[type].deletions += commit.stats.deletions * typeRatio;
      acc[type].hours += commit.timeEstimates.total * typeRatio;
    });
    return acc;
  }, {});

  markdown += '## File Type Impact\n';
  markdown += '| Type | Files Changed | Lines Added | Lines Deleted | Hours Spent |\n';
  markdown += '|------|--------------|-------------|---------------|-------------|\n';
  Object.entries(fileTypeStats).forEach(([type, stats]) => {
    markdown += `| ${type} | ${stats.files} | ${Math.round(stats.additions)} | ${Math.round(stats.deletions)} | ${stats.hours.toFixed(2)} |\n`;
  });

  return markdown;
}

// Main execution
try {
  const commits = getDetailedGitLog();
  
  // Write JSON report
  fs.writeFileSync('analyze-git-changes.json', JSON.stringify(commits, null, 2));
  
  // Write Markdown report
  fs.writeFileSync('analyze-git-changes.md', generateMarkdown(commits));
  
  console.log('Analysis completed successfully!');
  console.log('- analyze-git-changes.json');
  console.log('- analyze-git-changes.md');
} catch (error) {
  console.error('Error analyzing git changes:', error.message);
  process.exit(1);
}
