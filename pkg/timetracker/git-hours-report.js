import { readFileSync, writeFileSync } from 'fs';

function processGitAnalysis() {
  // Read the analysis data
  const analysisData = JSON.parse(readFileSync('analyze-git-changes.json', 'utf8'));

  // Group commits by date (YYYY-MM-DD)
  const commitsByDate = new Map();
  analysisData.forEach(commit => {
    const date = commit.date.split(' ')[0];
    if (!commitsByDate.has(date)) {
      commitsByDate.set(date, []);
    }
    commitsByDate.get(date).push(commit);
  });

  // Get unique developers (normalized to lowercase)
  const developers = [...new Set(analysisData.map(commit => commit.author.toLowerCase()))].sort();

  // Calculate statistics for each developer
  const devStats = {};
  developers.forEach(dev => {
    const devCommits = analysisData.filter(commit => commit.author.toLowerCase() === dev);
    devStats[dev] = {
      totalHours: 0,
      totalCommits: devCommits.length,
      byType: {
        FEATURE: { commits: 0, hours: 0 },
        FIX: { commits: 0, hours: 0 },
        PUBLISH: { commits: 0, hours: 0 },
        MERGE: { commits: 0, hours: 0 },
        DEFAULT: { commits: 0, hours: 0 }
      },
      byMonth: {}
    };

    // Process commits for this developer
    devCommits.forEach(commit => {
      const month = commit.date.substring(0, 7); // YYYY-MM

      // Update type statistics
      devStats[dev].byType[commit.type].commits++;
      devStats[dev].byType[commit.type].hours += commit.timeEstimates.total;
      devStats[dev].totalHours += commit.timeEstimates.total;

      // Update monthly statistics
      if (!devStats[dev].byMonth[month]) {
        devStats[dev].byMonth[month] = {
          commits: 0,
          hours: 0,
          byType: {
            FEATURE: { commits: 0, hours: 0 },
            FIX: { commits: 0, hours: 0 },
            PUBLISH: { commits: 0, hours: 0 },
            MERGE: { commits: 0, hours: 0 },
            DEFAULT: { commits: 0, hours: 0 }
          },
          workingDays: new Set()
        };
      }

      const monthStats = devStats[dev].byMonth[month];
      monthStats.commits++;
      monthStats.hours += commit.timeEstimates.total;
      monthStats.byType[commit.type].commits++;
      monthStats.byType[commit.type].hours += commit.timeEstimates.total;
      monthStats.workingDays.add(commit.date.split(' ')[0]);
    });

    // Convert Set to size for JSON serialization
    Object.values(devStats[dev].byMonth).forEach(month => {
      month.workingDays = month.workingDays.size;
    });
  });

  // Calculate project-wide statistics
  const projectStats = {
    start: analysisData[analysisData.length - 1].date.split(' ')[0],
    end: analysisData[0].date.split(' ')[0],
    totalWorkingDays: commitsByDate.size,
    totalCalendarDays: 0,
    totalHours: Object.values(devStats).reduce((acc, dev) => acc + dev.totalHours, 0)
  };

  // Calculate calendar days
  const startDate = new Date(projectStats.start);
  const endDate = new Date(projectStats.end);
  projectStats.totalCalendarDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

  return { projectStats, devStats };
}

function generateMarkdown(stats) {
  const { projectStats, devStats } = stats;
  let markdown = '# Relatório de Horas do Git\n\n';

  // Project Summary
  markdown += '## Resumo do Projeto\n';
  markdown += `- **Período**: ${projectStats.start} - ${projectStats.end}\n`;
  markdown += `- **Dias Totais**: ${projectStats.totalCalendarDays}\n`;
  markdown += `- **Dias com Commits**: ${projectStats.totalWorkingDays}\n`;
  markdown += `- **Total de Horas**: ${projectStats.totalHours.toFixed(2)}\n\n`;

  // Developer Statistics
  markdown += '## Estatísticas por Desenvolvedor\n\n';
  Object.entries(devStats)
    .sort(([a], [b]) => a.localeCompare(b))
    .forEach(([dev, stats]) => {
      markdown += `### ${dev}\n\n`;

      // Summary for this developer
      markdown += `- **Total de Horas**: ${stats.totalHours.toFixed(2)}\n`;
      markdown += `- **Total de Commits**: ${stats.totalCommits}\n`;
      markdown += `- **Média de Horas por Commit**: ${(stats.totalHours / stats.totalCommits).toFixed(2)}\n\n`;

      // Monthly table for this developer
      markdown += '| Mês | Dias Ativos | Features | Correções | Publicações | Merges | Outros | Total Horas | Horas/Dia |\n';
      markdown += '|-----|-------------|-----------|------------|-------------|---------|---------|-------------|------------|\n';

      Object.entries(stats.byMonth)
        .sort((a, b) => a[0].localeCompare(b[0]))
        .forEach(([month, data]) => {
          const hoursPerDay = (data.hours / data.workingDays).toFixed(1);
          const formatMonth = (monthStr) => {
            const [year, month] = monthStr.split('-');
            const date = new Date(parseInt(year), parseInt(month) - 1);
            return date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
          };
          markdown += `| ${formatMonth(month)} | ${data.workingDays} | ` +
            `${data.byType.FEATURE.commits} (${data.byType.FEATURE.hours.toFixed(1)}h) | ` +
            `${data.byType.FIX.commits} (${data.byType.FIX.hours.toFixed(1)}h) | ` +
            `${data.byType.PUBLISH.commits} (${data.byType.PUBLISH.hours.toFixed(1)}h) | ` +
            `${data.byType.MERGE.commits} (${data.byType.MERGE.hours.toFixed(1)}h) | ` +
            `${data.byType.DEFAULT.commits} (${data.byType.DEFAULT.hours.toFixed(1)}h) | ` +
            `${data.hours.toFixed(1)} | ${hoursPerDay} |\n`;
        });

      markdown += '\n';

      // Work distribution for this developer
      markdown += '#### Distribuição do Trabalho\n\n';
      Object.entries(stats.byType).forEach(([type, data]) => {
        const percentage = ((data.hours / stats.totalHours) * 100).toFixed(1);
        const typeNames = {
          FEATURE: 'Features',
          FIX: 'Correções',
          PUBLISH: 'Publicações',
          MERGE: 'Merges',
          DEFAULT: 'Outros'
        };
        markdown += `- ${typeNames[type]}: ${data.commits} commits, ${data.hours.toFixed(1)} horas (${percentage}% do tempo)\n`;
      });
      markdown += '\n';
    });

  // Project-wide work pattern
  markdown += '## Padrão de Trabalho do Projeto\n';
  markdown += `- Período Total: ${projectStats.totalCalendarDays} dias\n`;
  markdown += `- Dias com Commits: ${projectStats.totalWorkingDays} dias\n`;
  markdown += `- Frequência de Commits: ${((projectStats.totalWorkingDays / projectStats.totalCalendarDays) * 100).toFixed(1)}% dos dias\n`;
  markdown += `- Média de Horas por Dia com Commits: ${(projectStats.totalHours / projectStats.totalWorkingDays).toFixed(2)}\n\n`;

  return markdown;
}

// Main execution
try {
  const stats = processGitAnalysis();

  // Write JSON report
  writeFileSync('git-hours-report.json', JSON.stringify(stats, null, 2));

  // Write Markdown report
  writeFileSync('git-hours-report.md', generateMarkdown(stats));

  console.log('Reports generated successfully!');
  console.log('- git-hours-report.json');
  console.log('- git-hours-report.md');
} catch (error) {
  console.error('Error generating reports:', error.message);
  process.exit(1);
}
