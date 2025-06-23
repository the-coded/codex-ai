import { execSync } from 'child_process';
import { writeFileSync } from 'fs';

// ===== Constants =====

// File patterns
const STRUCTURAL_PATTERNS = [
  '/components/',
  '/layouts/',
  '/pages/',
  '/views/',
  '/styles/',
  '/assets/',
  '/themes/'
];

const ALGORITHMIC_PATTERNS = [
  '/utils/',
  '/helpers/',
  '/services/',
  '/hooks/',
  '/commands/',
  '/lib/',
  '/core/'
];

// File types
const STRUCTURAL_FILE_TYPES = ['css', 'scss', 'less', 'html', 'jsx', 'tsx', 'svg'];
const ALGORITHMIC_FILE_TYPES = ['js', 'ts', 'jsx', 'tsx'];

// Complexity types and levels
const COMPLEXITY_TYPES = {
  STRUCTURAL: 'STRUCTURAL',
  ALGORITHMIC: 'ALGORITHMIC'
};

const COMPLEXITY_LEVELS = {
  STRUCTURAL: {
    TRIVIAL: 0.5,    // Mudanças muito simples
    BASIC: 0.8,      // Mudanças básicas
    MODERATE: 1.2,   // Mudanças moderadas
    COMPLEX: 1.6,    // Mudanças complexas
    VERY_COMPLEX: 2.0 // Mudanças muito complexas
  },
  ALGORITHMIC: {
    TRIVIAL: 0.5,    // Mudanças muito simples
    BASIC: 1.0,      // Mudanças básicas
    MODERATE: 1.5,   // Mudanças moderadas
    COMPLEX: 2.0,    // Mudanças complexas
    VERY_COMPLEX: 2.5 // Mudanças muito complexas
  }
};

// Commit types and their time multipliers
const COMMIT_TYPES = {
  FEATURE: { name: 'FEATURE', multiplier: 1.0 },   // Tempo base
  FIX: { name: 'FIX', multiplier: 0.5 },          // Metade do tempo
  PUBLISH: { name: 'PUBLISH', multiplier: 0.1 },   // 10% do tempo
  MERGE: { name: 'MERGE', multiplier: 0.0 },       // Sem tempo adicional
  DEFAULT: { name: 'DEFAULT', multiplier: 0.8 }    // 80% do tempo base
};

// Base times for different file categories
const FILE_CATEGORIES = {
  // Logic files (high complexity, more planning)
  LOGIC: {
    extensions: ['js', 'ts', 'jsx', 'tsx'],
    baseTime: {
      planning: 1.0,     // 1h
      implementation: 0.04  // ~2.4min por linha
    }
  },
  // Config files (low complexity, quick changes)
  CONFIG: {
    extensions: ['json', 'yml', 'yaml', 'lock', 'gitignore', 'npmrc', 'env'],
    baseTime: {
      planning: 0.25,    // 15min
      implementation: 0.01  // ~0.6min por linha
    }
  },
  // Style files (medium complexity, visual focus)
  STYLE: {
    extensions: ['css', 'scss', 'sass', 'less', 'stylus'],
    baseTime: {
      planning: 0.5,     // 30min
      implementation: 0.02  // ~1.2min por linha
    }
  },
  // Documentation files (low complexity, text focus)
  DOCS: {
    extensions: ['md', 'mdx', 'txt', 'doc', 'docx', 'html'],
    baseTime: {
      planning: 0.3,     // 18min
      implementation: 0.015  // ~0.9min por linha
    }
  }
};

// Time multipliers
const PLANNING_BASE = 0.3;           // 30% base
const PLANNING_NET_WEIGHT = 0.7;     // +70% pelo net ratio
const PLANNING_DELETION_FACTOR = 0.2; // -80% para deleções
const DELETION_TIME_FACTOR = 0.1;    // 10% do tempo para deleções

// Get file extension using regex
function getFileExtension(filename) {
  // Pega a extensão principal (.ts, .tsx, etc)
  const baseMatch = filename.match(/\.([a-zA-Z0-9]+)(?:\})?$/);
  if (!baseMatch) return 'unknown';

  // Checa se tem .stories ou .test antes da extensão
  const specialMatch = filename.match(/\.(stories|test|spec)\.([a-zA-Z0-9]+)(?:\})?$/);
  if (specialMatch) {
    return specialMatch[2]; // Retorna a extensão real (ts/tsx)
  }

  return baseMatch[1];
}

// Analyze complexity type and level
function analyzeComplexity(stats) {
  // Structural indicators
  const structuralScore = calculateStructuralScore(stats);
  
  // Algorithmic indicators
  const algorithmicScore = calculateAlgorithmicScore(stats);

  // Determine dominant type
  const type = structuralScore > algorithmicScore 
    ? COMPLEXITY_TYPES.STRUCTURAL 
    : COMPLEXITY_TYPES.ALGORITHMIC;

  // Calculate final score based on type
  const score = type === COMPLEXITY_TYPES.STRUCTURAL 
    ? structuralScore 
    : algorithmicScore;

  // Determine level based on score
  const level = getComplexityLevel(score);

  return { type, level };
}

function calculateStructuralScore(stats) {
  let score = 0;

  // Check file patterns
  stats.files.forEach(file => {
    if (STRUCTURAL_PATTERNS.some(pattern => file.includes(pattern))) {
      score += 10;
    }
  });

  // Check file types
  Object.entries(stats.fileTypes).forEach(([type, count]) => {
    if (STRUCTURAL_FILE_TYPES.includes(type)) {
      score += count * 5;
    }
  });

  // File count impact
  score += stats.filesChanged * 2;

  // Style changes have high structural impact
  const styleFiles = stats.files.filter(f => 
    f.endsWith('.css') || 
    f.endsWith('.scss') || 
    f.endsWith('.less')
  ).length;
  score += styleFiles * 8;

  return score;
}

function calculateAlgorithmicScore(stats) {
  let score = 0;

  // Check file patterns
  stats.files.forEach(file => {
    if (ALGORITHMIC_PATTERNS.some(pattern => file.includes(pattern))) {
      score += 15;
    }
  });

  // Check file types
  Object.entries(stats.fileTypes).forEach(([type, count]) => {
    if (ALGORITHMIC_FILE_TYPES.includes(type)) {
      score += count * 8;
    }
  });

  // Lines per file (more lines = more algorithmic complexity)
  // Agora considera adições com peso maior que deleções
  const avgLinesPerFile = (stats.additions + stats.deletions * 0.10) / stats.filesChanged;
  score += Math.min(avgLinesPerFile / 10, 20);

  // Deletion ratio (reduzido e limitado)
  const deletionRatio = stats.deletions / (stats.additions || 1);
  score += Math.min(deletionRatio, 1.5) * 5; // Máximo de 1.5x e reduzido de 15 para 5

  return score;
}

function getComplexityLevel(score) {
  if (score <= 10) return 'TRIVIAL';
  if (score <= 30) return 'BASIC';
  if (score <= 60) return 'MODERATE';
  if (score <= 100) return 'COMPLEX';
  return 'VERY_COMPLEX';
}


// Get commit type from message
function getCommitType(message) {
  // Commits de merge
  if (message.startsWith('Merge')) return COMMIT_TYPES.MERGE.name;
  
  // Commits de feature
  if (message.startsWith('feat:')) return COMMIT_TYPES.FEATURE.name;
  if (message.match(/^v?\d+\.\d+\.\d+.*\s+-\s+.*feature/i)) return COMMIT_TYPES.FEATURE.name;
  if (message.match(/^.*first commit.*mvp/i)) return COMMIT_TYPES.FEATURE.name;
  
  // Commits de fix
  if (message.startsWith('fix:')) return COMMIT_TYPES.FIX.name;
  if (message.match(/^v?\d+\.\d+\.\d+.*\s+-\s+.*fix/i)) return COMMIT_TYPES.FIX.name;
  
  // Commits de release
  if (message.match(/^release\/v\d+/i)) return COMMIT_TYPES.PUBLISH.name;
  if (message.match(/^v?\d+\.\d+\.\d+\s*$/)) return COMMIT_TYPES.PUBLISH.name;
  if (message.match(/^Publish\s+v?\d+\.\d+\.\d+$/)) return COMMIT_TYPES.PUBLISH.name;
  if (message.match(/^New Release:/i)) return COMMIT_TYPES.PUBLISH.name;
  
  // Verificar se versão tem fix/feature
  if (message.match(/^v?\d+\.\d+\.\d+.*fix/i)) return COMMIT_TYPES.FIX.name;
  if (message.match(/^v?\d+\.\d+\.\d+.*feat/i)) return COMMIT_TYPES.FEATURE.name;
  
  return COMMIT_TYPES.DEFAULT.name;
}

// Get file category and base time
function getFileCategory(fileType) {
  for (const [category, info] of Object.entries(FILE_CATEGORIES)) {
    if (info.extensions.includes(fileType)) {
      return {
        category,
        baseTime: info.baseTime
      };
    }
  }
  
  // Default to LOGIC if unknown
  return {
    category: 'LOGIC',
    baseTime: FILE_CATEGORIES.LOGIC.baseTime
  };
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
      if (author !== 'github-ci') { // Ignore CI commits
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
      } else {
        currentCommit = null;
      }
    } else if (line.trim() && currentCommit) {
      // This is a file stat line
      const [additions, deletions, file] = line.split('\t');
      if (file) {
        const fileType = getFileExtension(file);
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
    const { type: complexityType, level: complexityLevel } = analyzeComplexity(commit.stats);
    
    // Calculate weighted time based on file categories
    let totalPlanningHours = 0;
    let totalImplementationHours = 0;
    
    Object.entries(commit.stats.fileTypes).forEach(([fileType, count]) => {
      const { baseTime } = getFileCategory(fileType);
      const typeRatio = count / commit.stats.filesChanged;
      
      // Separar adições e deleções
      const addedLines = commit.stats.additions * typeRatio;
      const deletedLines = commit.stats.deletions * typeRatio;
      const totalLines = addedLines + deletedLines;
      
      // Get complexity multiplier based on type and level
      const complexityMultiplier = COMPLEXITY_LEVELS[complexityType][complexityLevel];
      
      // Calculate net ratio para planning
      const netRatio = totalLines > 0 
        ? Math.max(0, (commit.stats.additions - commit.stats.deletions)) / totalLines
        : 0;
      
      // Planning multiplier base + net ratio weight
      let planningMultiplier = PLANNING_BASE + (netRatio * PLANNING_NET_WEIGHT);
      
      // Reduz ainda mais se for mais deleção que adição
      if (commit.stats.deletions > commit.stats.additions) {
        planningMultiplier *= PLANNING_DELETION_FACTOR;
      }
      
      // Get commit type multiplier
      const typeMultiplier = COMMIT_TYPES[type].multiplier;
      
      // Calculate hours for this file type
      totalPlanningHours += baseTime.planning * 
        complexityMultiplier *
        typeRatio *
        planningMultiplier *
        typeMultiplier;
      
      // Adições têm peso total, deleções têm peso reduzido
      totalImplementationHours += 
        (addedLines * baseTime.implementation * complexityMultiplier * typeMultiplier) +
        (deletedLines * baseTime.implementation * complexityMultiplier * DELETION_TIME_FACTOR * typeMultiplier);
    });

    return {
      hash: commit.hash,
      author: commit.author,
      date: commit.date,
      message: commit.message,
      type,
      complexityType,
      complexityLevel,
      stats: commit.stats,
      timeEstimates: {
        planning: totalPlanningHours,
        implementation: totalImplementationHours,
        total: totalPlanningHours + totalImplementationHours
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
    const key = `${commit.complexityType}/${commit.complexityLevel}`;
    acc[key] = (acc[key] || 0) + 1;
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
    markdown += `- **Author**: ${commit.author}\n`;
    markdown += `- **Type**: ${commit.type}\n`;
    markdown += `- **Complexity**: ${commit.complexityType}/${commit.complexityLevel}\n`;
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
    markdown += `- ${complexity}: ${percentage}% (${count} commits)\n`;
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
  writeFileSync('analyze-git-changes.json', JSON.stringify(commits, null, 2));
  
  // Write Markdown report
  writeFileSync('analyze-git-changes.md', generateMarkdown(commits));
  
  console.log('Analysis completed successfully!');
  console.log('- analyze-git-changes.json');
  console.log('- analyze-git-changes.md');
} catch (error) {
  console.error('Error analyzing git changes:', error.message);
  process.exit(1);
}
