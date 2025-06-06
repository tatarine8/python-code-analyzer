// 📊 Побудова графіків з метрик аналізу коду

window.addEventListener('DOMContentLoaded', () => {
  if (!window.analysisResult || !Array.isArray(window.analysisResult.files)) return;

  const files = window.analysisResult.files;
  const labels = files.map(f => f.filename);
  const summary = window.analysisResult;

  // 🔹 Utility: кольори за шкалами
  const colorByValue = (val, ranges) => {
    for (const [limit, color] of ranges) {
      if (val <= limit) return color;
    }
    return ranges[ranges.length - 1][1];
  };

  const normalize = (val, max = 1, reverse = false, soften = 1) => {
    let score = val / max;
    score = Math.min(score, 1);
    score = Math.pow(score, soften); // згладжування вимкнено (soften = 1)
    return reverse ? 1 - score : score;
};

  // === 1. Maintainability Index Histogram (зменшений розмір) ===
  new Chart(document.getElementById('miHistogram'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Maintainability Index',
        data: files.map(f => f.mi),
        backgroundColor: files.map(f => colorByValue(f.mi, [[60, 'rgba(255,99,132,0.7)'], [80, 'rgba(255,206,86,0.7)'], [100, 'rgba(75,192,192,0.7)']]))
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: { padding: 20 },
      elements: { line: { borderWidth: 2 }, point: { radius: 5 } },
      plugins: { legend: { display: false } },
      scales: { y: { min: 0, max: 100 } }
    }
  });

  // === 2. Donut Chart for Halstead Volume ===
  new Chart(document.getElementById('donutHalsteadVolume'), {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: files.map(f => f.halstead?.volume || 0),
        backgroundColor: labels.map(() => `hsl(${Math.random() * 360}, 60%, 70%)`)
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Halstead Volume (по файлах)' }
      }
    }
  });

  // === 3. Bubble Chart ===
  new Chart(document.getElementById('bubbleChart'), {
    type: 'bubble',
    data: {
      datasets: files.map(f => ({
        label: f.filename,
        data: [{ x: f.rfc || 0, y: f.cbo || 0, r: Math.sqrt(f.wmc || 1) + 2 }],
        backgroundColor: colorByValue(f.mi, [[60, 'rgba(255,99,132,0.6)'], [80, 'rgba(255,206,86,0.6)'], [100, 'rgba(75,192,192,0.6)']])
      }))
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.dataset.label} | RFC: ${ctx.raw.x}, CBO: ${ctx.raw.y}, WMC: ${Math.round((ctx.raw.r - 2) ** 2)}`
          }
        },
        legend: { display: false }
      },
      scales: {
        x: { title: { display: true, text: 'RFC' } },
        y: { title: { display: true, text: 'CBO' } }
      }
    }
  });

  // === 4. Bugs Chart (можна прибрати, якщо зайвий) ===
  // !!! Можливо зайвий, оскільки є line-графік з тими самими даними !!!

  // === 5–7. Бар-чарти: LCOM, Instability, CBO ===
  const charts = [
    { id: 'lcomChart', label: 'LCOM', values: f => f.lcom, range: [[0.4, 'rgba(75,192,192,0.7)'], [0.7, 'rgba(255,206,86,0.7)'], [1.0, 'rgba(255,99,132,0.7)']], max: 1.0 },
    { id: 'instabilityChart', label: 'Instability', values: f => f.instability, range: [[0.4, 'rgba(75,192,192,0.7)'], [0.7, 'rgba(255,206,86,0.7)'], [1.0, 'rgba(255,99,132,0.7)']], max: 1.0 },
    { id: 'cboChart', label: 'CBO', values: f => f.cbo, range: [[5, 'rgba(75,192,192,0.7)'], [10, 'rgba(255,206,86,0.7)'], [Infinity, 'rgba(255,99,132,0.7)']] }
  ];

  charts.forEach(cfg => {
    new Chart(document.getElementById(cfg.id), {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: cfg.label,
          data: files.map(cfg.values),
          backgroundColor: files.map(f => colorByValue(cfg.values(f), cfg.range))
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: cfg.max ? { y: { min: 0, max: cfg.max } } : {}
      }
    });
  });

  // === 8. Line Chart — Bugs Trend ===
  new Chart(document.getElementById('bugsTrendLine'), {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Очікувані баги (Halstead)',
        data: files.map(f => f.halstead?.bugs || 0),
        borderColor: 'rgba(255,99,132,0.8)',
        backgroundColor: 'rgba(255,99,132,0.2)',
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Тренд: Очікувані баги по файлах'
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // === 9. Radar Chart — Зведена оцінка + рекомендації ===
  const metrics = [
    normalize(summary.mi, 100),
    normalize(Math.log1p(summary.wmc / files.length), Math.log1p(50), true),
    normalize(summary.instability, 1, true),
    normalize(Math.log1p(summary.halstead?.bugs || 0), Math.log1p(1), true),
    normalize(Math.log1p(summary.halstead?.volume || 0), Math.log1p(summary.halstead?.volume * 2 || 1), true),
    normalize(Math.log1p(summary.cbo || 0), Math.log1p(30), true)
  ];

  new Chart(document.getElementById('radarChart'), {
    type: 'radar',
    data: {
      labels: ['Підтримуваність (MI)', 'Простота (WMC)', 'Стабільність (Instability)', 'Ризик багів (Bugs)', 'Обсяг (Volume)', 'Зв’язність (CBO)'],
      datasets: [{
        label: 'Проєкт',
        data: metrics,
        backgroundColor: 'rgba(54, 162, 235, 0.3)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          beginAtZero: true,
          min: 0,
          max: 1,
          ticks: {
            stepSize: 0.1
          }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });

  const avgScore = (
    0.15 * metrics[0] +  // MI
    0.2 * metrics[1] +   // WMC
    0.2 * metrics[2] +   // Instability
    0.15 * metrics[3] +  // Bugs
    0.15 * metrics[4] +  // Volume
    0.15 * metrics[5]    // CBO
);
  let scoreLetter = 'D', comment = '';
  if (avgScore >= 0.8) {
    scoreLetter = 'A';
    comment = 'Код легко підтримується, має невелику складність і мінімальний ризик помилок.';
  } else if (avgScore >= 0.6) {
    scoreLetter = 'B';
    comment = 'Проєкт має хорошу якість коду, хоча є кілька аспектів, які можна покращити.';
  } else if (avgScore >= 0.4) {
    scoreLetter = 'C';
    comment = 'Якість коду середня — бажано зменшити складність та кількість зв’язків.';
  } else {
    scoreLetter = 'D';
    comment = 'Код має високий рівень складності та низьку підтримуваність. Рекомендується рефакторинг.';
  }

  const scoreEl = document.getElementById('scoreLetter');
  scoreEl.textContent = scoreLetter;
  scoreEl.classList.remove('text-primary', 'text-success', 'text-warning', 'text-danger');
  if (scoreLetter === 'A') scoreEl.classList.add('text-success');
  else if (scoreLetter === 'B') scoreEl.classList.add('text-primary');
  else if (scoreLetter === 'C') scoreEl.classList.add('text-warning');
  else scoreEl.classList.add('text-danger');
  document.getElementById('scoreComment').textContent = comment;

  const recommendations = [];
  if (summary.mi < 60) recommendations.push("🔧 Низький MI — покращіть читабельність і коментування коду.");
  if (summary.wmc > 50) recommendations.push("🔧 Високий WMC — спростіть логіку методів, розбийте великі функції.");
  if (summary.instability > 0.7) recommendations.push("🔧 Високий Instability — модуль надто залежний від інших, спробуйте зменшити зовнішні імпорти.");
  if (summary.cbo > 20) recommendations.push("🔧 Високий CBO — зменшіть кількість зв’язків між класами.");
  if (summary.halstead?.volume > 1000) recommendations.push("🔧 Високий Halstead Volume — розбийте великі модулі на менші частини.");
  if (summary.halstead?.bugs > 0.5) recommendations.push("🔧 Високий рівень потенційних багів — перевірте найскладніші ділянки коду.");

  const recContainer = document.createElement('div');
  recContainer.className = "mt-3 d-flex flex-column gap-2";
  recommendations.forEach(r => {
    const li = document.createElement('div');
    li.innerHTML = `<span class='text-danger'>🔧</span> <span>${r}</span>`;
    li.className = "alert alert-danger bg-white text-danger py-2 px-3 border border-danger-subtle";
    recContainer.appendChild(li);
  });
  document.getElementById('scoreComment').after(recContainer);
});

function smartFormat(value, forceTwoDecimals = false) {
    const num = parseFloat(value);
    if (isNaN(num)) return value;

    if (forceTwoDecimals) return num.toFixed(2);
    return Math.abs(num) < 1 ? num.toFixed(3) : num.toFixed(2);
}

function roundHalsteadInOverview() {
    const halsteadCard = document.querySelector('#overview .card-title');
    if (!halsteadCard || !halsteadCard.textContent.includes('Halstead')) return;

    const listItems = halsteadCard.closest('.card').querySelectorAll('ul.list-group li');

    listItems.forEach(item => {
        const parts = item.textContent.split(':');
        if (parts.length < 2) return;

        const label = parts[0].trim();
        const valueText = parts[1].replace(/[^\d.-]/g, '').trim();  // Видаляє % і "сек"
        const value = parseFloat(valueText);

        if (!isNaN(value)) {
            const rounded = value.toFixed(2);
            const suffix = item.textContent.includes('%') ? '%' : (item.textContent.includes('сек') ? ' сек' : '');
            item.innerHTML = `${label}: <span>${rounded}${suffix}</span>`;
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    roundHalsteadInOverview();
});


function formatMetricsTable() {
    const table = document.querySelector('#explore table');
    if (!table) return;

    const headerCells = Array.from(table.querySelectorAll('thead th'));

    // Мапа колонок: назва → index
    const columns = {};
    headerCells.forEach((th, i) => {
        const label = th.textContent.trim();
        if (label.includes('% Коментарів')) columns['comment_ratio'] = i;
        else if (label === 'MI') columns['mi'] = i;
        else if (label === 'Volume') columns['volume'] = i;
        else if (label === 'Bugs') columns['bugs'] = i;
        else if (label === 'LCOM') columns['lcom'] = i;
    });

    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        if (columns.comment_ratio !== undefined) {
            const cell = row.children[columns.comment_ratio];
            if (cell) {
                const val = cell.textContent.replace('%', '').trim();
                cell.textContent = smartFormat(val, true) + '%';
            }
        }

        ['mi', 'volume', 'bugs', 'lcom'].forEach(key => {
            const i = columns[key];
            if (i !== undefined) {
                const cell = row.children[i];
                if (cell) {
                    const val = cell.textContent.trim();
                    cell.textContent = smartFormat(val);
                }
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    formatMetricsTable();
});
