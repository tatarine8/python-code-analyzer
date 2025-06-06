let sortAscending = true;  // true = ↑, false = ↓
let originalOrder = [];    // Зберігає початковий порядок елементів для скидання сортування

// Ініціалізація після завантаження DOM
document.addEventListener("DOMContentLoaded", () => {
    const accordion = document.getElementById("functionsAccordion");
    if (!accordion) return;

    // Зберігаємо первинний порядок карток
    originalOrder = Array.from(accordion.children);

    // Якщо відкрили сторінку напряму з #functions, активуємо вкладку
    if (window.location.hash === '#functions') {
        const tab = new bootstrap.Tab(document.querySelector('a[href="#functions"]'));
        tab.show();
    }

    // Початково ховаємо файли без функцій
    const hidden = document.querySelectorAll('.no-functions');
    hidden.forEach(el => el.style.display = 'none');

    // Ініціалізація кнопок
    const toggleBtn = document.getElementById("toggleNoFunctions");
    if (toggleBtn) {
        toggleBtn.textContent = "Показати порожні файли";
    }

    const expandBtn = document.getElementById("toggleAllFunctions");
    if (expandBtn) {
        expandBtn.textContent = "Розгорнути всі";
    }

    // Встановлюємо сортування за замовчуванням
    document.getElementById("sortSelector").value = "default";
    updateSortDirectionIcon();
});

// 🔁 Показати/сховати файли без функцій
function toggleNoFunctions() {
    const cards = document.querySelectorAll('.no-functions');
    const btn = document.getElementById("toggleNoFunctions");

    cards.forEach(card => {
        card.style.display = (card.style.display === "none") ? "block" : "none";
    });

    if (btn) {
        const shown = cards.length > 0 && cards[0].style.display === 'block';
        btn.textContent = shown ? "Сховати порожні файли" : "Показати порожні файли";
    }
}

// 🔁 Перемикач напрямку сортування
function toggleSortDirection() {
    sortAscending = !sortAscending;
    updateSortDirectionIcon();
    sortFiles();  // автоматично сортуємо після зміни напрямку
}

// 🔁 Оновити іконку напрямку сортування (↑ або ↓)
function updateSortDirectionIcon() {
    const btn = document.getElementById("sortDirection");
    if (btn) {
        btn.textContent = sortAscending ? "↑" : "↓";
        btn.title = sortAscending ? "Сортування за зростанням" : "Сортування за спаданням";
    }
}

// 🔃 Основна функція сортування карток
function sortFiles() {
    const sortOption = document.getElementById("sortSelector").value;
    const accordion = document.getElementById("functionsAccordion");
    if (!accordion) return;

    // Повернення до початкового порядку
    if (sortOption === "default") {
        originalOrder.forEach(card => accordion.appendChild(card));
        return;
    }

    const cards = Array.from(accordion.children);

    // Функції для отримання значень для порівняння
    const getFuncCount = (card) => {
        const text = card.querySelector('.card-header h5 small')?.textContent || '';
        const match = text.match(/\d+/);
        return match ? parseInt(match[0], 10) : 0;
    };

    const getMaxComplexity = (card) => {
        const rows = card.querySelectorAll('tbody tr');
        const values = Array.from(rows).map(tr => {
            const cell = tr.children[1];
            return cell ? parseFloat(cell.textContent) || 0 : 0;
        });
        return values.length ? Math.max(...values) : 0;
    };

    // Логіка сортування
    cards.sort((a, b) => {
        let valA = 0, valB = 0;

        if (sortOption === "name") {
            valA = a.querySelector('.card-header h5 strong')?.textContent?.toLowerCase() || '';
            valB = b.querySelector('.card-header h5 strong')?.textContent?.toLowerCase() || '';
        } else if (sortOption === "function_count") {
            valA = getFuncCount(a);
            valB = getFuncCount(b);
        } else if (sortOption === "complexity") {
            valA = getMaxComplexity(a);
            valB = getMaxComplexity(b);
        }

        if (valA < valB) return sortAscending ? -1 : 1;
        if (valA > valB) return sortAscending ? 1 : -1;
        return 0;
    });

    // Додати сортування до DOM
    cards.forEach(card => accordion.appendChild(card));
}

// 🔁 Розгорнути/згорнути всі картки функцій
let allExpanded = false;

function toggleAllFunctions() {
    const accordions = document.querySelectorAll('#functionsAccordion .accordion-collapse');
    accordions.forEach(collapse => {
        const bsCollapse = new bootstrap.Collapse(collapse, { toggle: false });
        allExpanded ? bsCollapse.hide() : bsCollapse.show();
    });

    allExpanded = !allExpanded;

    const btn = document.getElementById("toggleAllFunctions");
    if (btn) {
        btn.textContent = allExpanded ? "Згорнути всі" : "Розгорнути всі";
    }
}
