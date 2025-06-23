#!/usr/bin/env node
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, resolve, basename } from 'path';
import { createRequire } from 'module';

// Get current file's directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Create require function
const require = createRequire(import.meta.url);

// Get the root directory (where .git is located)
const getRootDir = () => {
  try {
    // Try to find .git directory
    const gitDir = execSync('git rev-parse --git-dir').toString().trim();
    return resolve(gitDir, '..');
  } catch (error) {
    console.error('❌ Error: Not a git repository');
    process.exit(1);
  }
};

// Execute a script and handle errors
const executeScript = async (scriptPath) => {
  try {
    // Import script dynamically
    await import(scriptPath);
  } catch (error) {
    console.error(`❌ Error executing ${basename(scriptPath)}:`, error.message);
    process.exit(1);
  }
};

// Main execution
const main = async () => {
  try {
    // Change to root directory
    const rootDir = getRootDir();
    process.chdir(rootDir);
    
    console.log('📊 Running Git Time Tracker...\n');
    
    // Get script paths
    const analyzeScript = resolve(__dirname, 'analyze-git-changes.js');
    const reportScript = resolve(__dirname, 'git-hours-report.js');
    
    // Execute scripts
    console.log('🔍 Analyzing git changes...');
    await executeScript(analyzeScript);
    
    console.log('\n📝 Generating hours report...');
    await executeScript(reportScript);
    
    console.log('\n✨ All done! Check the generated reports:');
    console.log('- analyze-git-changes.json');
    console.log('- analyze-git-changes.md');
    console.log('- git-hours-report.json');
    console.log('- git-hours-report.md');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
};

main();
