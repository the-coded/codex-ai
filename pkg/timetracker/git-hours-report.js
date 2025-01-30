const fs = require('fs');

function processGitAnalysis() {
  // Read the analysis data
  const analysisData = JSON.parse(fs.readFileSync('analyze-git-changes.json', 'utf8'));
  
  // Group commits by date (YYYY-MM-DD)
  const commitsByDate = new Map();
  analysisData.forEach(commit => {
    const date = commit.date.split(' ')[0];
    if (!commitsByDate.has(date)) {
      commitsByDate.set(date, []);
    }
    commitsByDate.get(date).push(commit);
  });

  // Calculate statistics
  const stats = {
    projectPeriod: {
      start: analysisData[analysisData.length - 1].date.split(' ')[0],
      end: analysisData[0].date.split(' ')[0],
      totalWorkingDays: commitsByDate.size,
      totalCalendarDays: 0
    },
    developer: {
      name: "Gab",
      statistics: {
        totalHours: 0,
        totalCommits: analysisData.length,
        byType: {
          FEATURE: { commits: 0, hours: 0 },
          FIX: { commits: 0, hours: 0 },
          PUBLISH: { commits: 0, hours: 0 },
          DEFAULT: { commits: 0, hours: 0 }
        },
        byMonth: {}
      }
    }
  };

  // Calculate calendar days
  const startDate = new Date(stats.projectPeriod.start);
  const endDate = new Date(stats.projectPeriod.end);
  stats.projectPeriod.totalCalendarDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));

  // Process commits
  analysisData.forEach(commit => {
    const month = commit.date.substring(0, 7); // YYYY-MM
    
    // Update type statistics
    stats.developer.statistics.byType[commit.type].commits++;
    stats.developer.statistics.byType[commit.type].hours += commit.timeEstimates.total;
    stats.developer.statistics.totalHours += commit.timeEstimates.total;

    // Update monthly statistics
    if (!stats.developer.statistics.byMonth[month]) {
      stats.developer.statistics.byMonth[month] = {
        commits: 0,
        hours: 0,
        byType: {
          FEATURE: { commits: 0, hours: 0 },
          FIX: { commits: 0, hours: 0 },
          PUBLISH: { commits: 0, hours: 0 },
          DEFAULT: { commits: 0, hours: 0 }
        },
        workingDays: new Set()
      };
    }
    
    const monthStats = stats.developer.statistics.byMonth[month];
    monthStats.commits++;
    monthStats.hours += commit.timeEstimates.total;
    monthStats.byType[commit.type].commits++;
    monthStats.byType[commit.type].hours += commit.timeEstimates.total;
    monthStats.workingDays.add(commit.date.split(' ')[0]);
  });

  // Convert Set to size for JSON serialization
  Object.values(stats.developer.statistics.byMonth).forEach(month => {
    month.workingDays = month.workingDays.size;
  });

  return stats;
}

function generateMarkdown(stats) {
  let markdown = '# Relatório de Horas do Git\n\n';

  // Resumo do Projeto
  markdown += '## Resumo do Projeto\n';
  markdown += `- **Período**: ${stats.projectPeriod.start} - ${stats.projectPeriod.end}\n`;
  markdown += `- **Dias Totais**: ${stats.projectPeriod.totalCalendarDays}\n`;
  markdown += `- **Dias Trabalhados**: ${stats.projectPeriod.totalWorkingDays}\n`;
  markdown += `- **Total de Horas**: ${stats.developer.statistics.totalHours.toFixed(2)}\n`;
  markdown += `- **Média de Horas por Dia Trabalhado**: ${(stats.developer.statistics.totalHours / stats.projectPeriod.totalWorkingDays).toFixed(2)}\n\n`;

  // Horas por Desenvolvedor
  markdown += '## Horas por Desenvolvedor\n\n';
  markdown += `### ${stats.developer.name}\n\n`;

  // Tabela Mensal
  markdown += '| Mês | Dias Trabalhados | Features | Correções | Publicações | Outros | Total Horas | Horas/Dia |\n';
  markdown += '|-----|------------------|-----------|------------|-------------|---------|-------------|------------|\n';

  Object.entries(stats.developer.statistics.byMonth)
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
        `${data.byType.DEFAULT.commits} (${data.byType.DEFAULT.hours.toFixed(1)}h) | ` +
        `${data.hours.toFixed(1)} | ${hoursPerDay} |\n`;
    });

  // Linha de totais
  const totals = stats.developer.statistics;
  const avgHoursPerDay = (totals.totalHours / stats.projectPeriod.totalWorkingDays).toFixed(1);
  markdown += `| **Total** | ${stats.projectPeriod.totalWorkingDays} | ` +
    `${totals.byType.FEATURE.commits} (${totals.byType.FEATURE.hours.toFixed(1)}h) | ` +
    `${totals.byType.FIX.commits} (${totals.byType.FIX.hours.toFixed(1)}h) | ` +
    `${totals.byType.PUBLISH.commits} (${totals.byType.PUBLISH.hours.toFixed(1)}h) | ` +
    `${totals.byType.DEFAULT.commits} (${totals.byType.DEFAULT.hours.toFixed(1)}h) | ` +
    `${totals.totalHours.toFixed(1)} | ${avgHoursPerDay} |\n\n`;

  // Distribuição do Trabalho
  markdown += '## Distribuição do Trabalho\n\n';
  const typeNames = {
    FEATURE: 'Features',
    FIX: 'Correções',
    PUBLISH: 'Publicações',
    DEFAULT: 'Outros'
  };
  Object.entries(totals.byType).forEach(([type, data]) => {
    const percentage = ((data.hours / totals.totalHours) * 100).toFixed(1);
    markdown += `- ${typeNames[type]}: ${data.commits} commits, ${data.hours.toFixed(1)} horas (${percentage}% do tempo total)\n`;
  });
  markdown += '\n';

  // Padrão de Trabalho
  markdown += '## Padrão de Trabalho\n';
  markdown += `- Período Total: ${stats.projectPeriod.totalCalendarDays} dias\n`;
  markdown += `- Dias Ativos: ${stats.projectPeriod.totalWorkingDays} dias\n`;
  markdown += `- Frequência de Trabalho: ${((stats.projectPeriod.totalWorkingDays / stats.projectPeriod.totalCalendarDays) * 100).toFixed(1)}% dos dias tiveram atividade\n`;
  markdown += `- Média de Horas por Dia Trabalhado: ${(totals.totalHours / stats.projectPeriod.totalWorkingDays).toFixed(2)}\n`;
  markdown += `- Média de Commits por Dia Trabalhado: ${(totals.totalCommits / stats.projectPeriod.totalWorkingDays).toFixed(2)}\n\n`;

  // Análise Resumida
  markdown += '## Análise Resumida\n\n';
  markdown += `O novo relatório mostra um total de ${stats.developer.statistics.totalHours.toFixed(2)} horas de trabalho, distribuídas em:\n\n`;
  
  const typeNamesLower = {
    FEATURE: 'features',
    FIX: 'correções',
    PUBLISH: 'publicações',
    DEFAULT: 'outras atividades'
  };
  Object.entries(totals.byType).forEach(([type, data]) => {
    const percentage = ((data.hours / totals.totalHours) * 100).toFixed(1);
    markdown += `- ${data.hours.toFixed(1)} horas em ${typeNamesLower[type]} (${percentage}%)\n`;
  });

  markdown += '\nPeríodos mais intensos:\n\n';
  
  // Get monthly hours sorted by hours
  const monthlyHours = Object.entries(stats.developer.statistics.byMonth)
    .map(([month, data]) => ({
      month,
      hours: data.hours,
      features: data.byType.FEATURE.commits,
      fixes: data.byType.FIX.commits
    }))
    .sort((a, b) => b.hours - a.hours);

  // Get top 2 months
  const [topMonth, secondMonth] = monthlyHours;
  const formatMonth = (monthStr) => {
    const [year, month] = monthStr.split('-');
    const date = new Date(parseInt(year), parseInt(month) - 1);
    return date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
  };

  // Determine month description based on commit types
  const getMonthDescription = (monthData) => {
    if (monthData.features > 0) return "desenvolvimento de features";
    if (monthData.fixes > 0) return "correções";
    return "melhorias e publicações";
  };

  markdown += `- ${formatMonth(topMonth.month)}: ${topMonth.hours.toFixed(1)} horas (${getMonthDescription(topMonth)})\n`;
  markdown += `- ${formatMonth(secondMonth.month)}: ${secondMonth.hours.toFixed(1)} horas (${getMonthDescription(secondMonth)})\n`;
  
  const otherMonthsHours = monthlyHours
    .slice(2)
    .reduce((acc, curr) => acc + curr.hours, 0);
  
  markdown += `- Demais meses: ~${otherMonthsHours.toFixed(1)} horas (melhorias e correções)\n\n`;

  markdown += `O trabalho foi realizado em ${stats.projectPeriod.totalWorkingDays} dias ativos dos ${stats.projectPeriod.totalCalendarDays} dias do período, `;
  markdown += `com média de ${(totals.totalHours / stats.projectPeriod.totalWorkingDays).toFixed(2)} horas por dia de trabalho, `;
  markdown += `indicando dias de desenvolvimento intenso quando houve atividade.\n`;

  return markdown;
}

// Main execution
try {
  const stats = processGitAnalysis();
  
  // Write JSON report
  fs.writeFileSync('git-hours-report.json', JSON.stringify(stats, null, 2));
  
  // Write Markdown report
  fs.writeFileSync('git-hours-report.md', generateMarkdown(stats));
  
  console.log('Reports generated successfully!');
  console.log('- git-hours-report.json');
  console.log('- git-hours-report.md');
} catch (error) {
  console.error('Error generating reports:', error.message);
  process.exit(1);
}
