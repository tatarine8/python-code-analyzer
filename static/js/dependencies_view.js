console.log("✅ dependencies_view.js loaded");

let depsExpanded = false;     // Стан розгортання всіх карток залежностей
let graphExpanded = false;    // Стан розгортання візуального графа

// 🔁 Перемикання видимості модулів без імпортів
function toggleNoDeps() {
    const cards = document.querySelectorAll('.no-deps');
    cards.forEach(card => {
        card.style.display = (card.style.display === 'none') ? 'block' : 'none';
    });

    const btn = document.getElementById("toggleNoDeps");
    if (btn) {
        const shown = cards.length > 0 && cards[0].style.display === 'block';
        btn.textContent = shown ? "Сховати модулі без імпортів" : "Показати модулі без імпортів";
    }
}

// 🔁 Згорнути або розгорнути всі картки з залежностями
function toggleAllDeps() {
    const accordions = document.querySelectorAll('#depsAccordion .accordion-collapse');
    accordions.forEach(collapse => {
        const bsCollapse = new bootstrap.Collapse(collapse, { toggle: false });
        depsExpanded ? bsCollapse.hide() : bsCollapse.show();
    });

    depsExpanded = !depsExpanded;

    const btn = document.getElementById("toggleAllDeps");
    if (btn) {
        btn.textContent = depsExpanded ? "Згорнути всі" : "Розгорнути всі";
    }
}

// Ініціалізація після завантаження DOM
document.addEventListener("DOMContentLoaded", () => {

    // Сховати блоки без імпортів за замовчуванням
    const hidden = document.querySelectorAll('.no-deps');
    hidden.forEach(el => el.style.display = 'none');

    // Ініціалізація текстів кнопок
    const btnExpand = document.getElementById("toggleAllDeps");
    if (btnExpand) btnExpand.textContent = "Розгорнути всі";

    const btnNoDeps = document.getElementById("toggleNoDeps");
    if (btnNoDeps) btnNoDeps.textContent = "Показати модулі без імпортів";

    // Обробка кнопки зміни розміру графа
    const toggleGraphBtn = document.getElementById("toggleGraphSize");
    const graphContainer = document.getElementById("dependencyGraphContainer");

    if (toggleGraphBtn && graphContainer) {
        toggleGraphBtn.addEventListener("click", () => {
            graphExpanded = !graphExpanded;

            if (graphExpanded) {
                graphContainer.style.maxHeight = "90vh";
                graphContainer.style.overflowY = "auto";
                toggleGraphBtn.textContent = "🔽 Згорнути";
            } else {
                graphContainer.style.maxHeight = "280px";
                graphContainer.style.overflow = "hidden";
                toggleGraphBtn.textContent = "🔍 Розгорнути";
            }
        });
    }

    // 🧠 Побудова графа залежностей між модулями
    const container = document.getElementById("dependencyGraph");
    const edges = window.analysisResult?.edges || [];

    if (container && edges.length) {
        // Побудова унікального списку модулів (вузлів графа)
        const nodesMap = new Map();
        edges.forEach(edge => {
            nodesMap.set(edge.from, true);
            nodesMap.set(edge.to, true);
        });

        const nodes = Array.from(nodesMap.keys()).map((label, id) => ({
            id,
            label,
            shape: "box",
            font: { align: "center" },
            color: {
                background: "#eaf4ff",
                border: "#0d6efd",
                highlight: {
                    background: "#d0eaff",
                    border: "#0d6efd"
                }
            }
        }));

        // Відповідність label → id
        const nodeIndex = Object.fromEntries(nodes.map(n => [n.label, n.id]));

        // Форматування зв’язків для візуалізації
        const formattedEdges = edges.map(edge => ({
            from: nodeIndex[edge.from],
            to: nodeIndex[edge.to],
            arrows: "to"
        }));

        // Динамічне масштабування висоти графа в залежності від кількості вузлів
        const totalNodes = nodes.length;
        let graphHeight = 400 + totalNodes * 20;
        graphHeight = Math.min(graphHeight, 1000);
        let nodeSpacing = 100 + Math.min(totalNodes * 5, 300);
        let levelSeparation = 120 + Math.min(totalNodes * 3, 200);
        container.style.height = `${graphHeight}px`;

        // Ініціалізація графа за допомогою бібліотеки vis-network
        const network = new vis.Network(container, {
            nodes: new vis.DataSet(nodes),
            edges: new vis.DataSet(formattedEdges)
        }, {
            layout: {
                hierarchical: {
                    enabled: true,
                    direction: "UD",             // Зверху вниз
                    sortMethod: "directed",
                    levelSeparation,
                    nodeSpacing,
                    treeSpacing: 200
                }
            },
            nodes: {
                shape: "box",
                margin: 10,
                font: {
                    size: 14,
                    face: "Arial",
                    align: "center"
                },
                borderWidth: 1
            },
            edges: {
                arrows: { to: { enabled: true, scaleFactor: 0.9 } },
                color: {
                    color: "#0d6efd",
                    highlight: "#0b5ed7"
                },
                smooth: {
                    type: "cubicBezier",
                    forceDirection: "vertical",
                    roundness: 0.4
                }
            },
            physics: false,  // Фіксована структура
            interaction: {
                hover: true,
                tooltipDelay: 150
            }
        });

        // Автофокусування графа в контейнері
        network.fit({
            animation: {
                duration: 600,
                easingFunction: "easeInOutQuad"
            }
        });
    }
});
