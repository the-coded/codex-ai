#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

// Get the root directory (where .git is located)
const getRootDir = () => {
  try {
    // Try to find .git directory
    const gitDir = execSync('git rev-parse --git-dir').toString().trim();
    return path.resolve(gitDir, '..');
  } catch (error) {
    console.error('❌ Error: Not a git repository');
    process.exit(1);
  }
};

// Execute a script and handle errors
const executeScript = (scriptPath) => {
  try {
    require(scriptPath);
  } catch (error) {
    console.error(`❌ Error executing ${path.basename(scriptPath)}:`, error.message);
    process.exit(1);
  }
};

// Main execution
try {
  // Change to root directory
  const rootDir = getRootDir();
  process.chdir(rootDir);
  
  console.log('📊 Running Git Time Tracker...\n');
  
  // Get script paths
  const analyzeScript = path.join(__dirname, 'analyze-git-changes.js');
  const reportScript = path.join(__dirname, 'git-hours-report.js');
  
  // Execute scripts
  console.log('🔍 Analyzing git changes...');
  executeScript(analyzeScript);
  
  console.log('\n📝 Generating hours report...');
  executeScript(reportScript);
  
  console.log('\n✨ All done! Check the generated reports:');
  console.log('- analyze-git-changes.json');
  console.log('- analyze-git-changes.md');
  console.log('- git-hours-report.json');
  console.log('- git-hours-report.md');
} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}
