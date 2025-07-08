/**
 * This script handles the pagination for the tables on the history page.
 * It shows a set number of rows initially and provides a "View More" button
 * to progressively reveal more rows.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Configuration constants
    const INITIAL_ROWS = 10;
    const ROWS_TO_ADD = 15;

    /**
     * Sets up pagination for a given table.
     * @param {string} tableId The ID of the table element.
     * @param {string} buttonId The ID of the "View More" button.
     */
    function setupPagination(tableId, buttonId) {
        const table = document.getElementById(tableId);
        // If the table doesn't exist on the page, do nothing.
        if (!table) return;

        const viewMoreBtn = document.getElementById(buttonId);
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        let visibleRowsCount = INITIAL_ROWS;

        // Hide all rows initially.
        rows.forEach(row => row.style.display = 'none');
        
        // Show the first page of rows.
        rows.slice(0, visibleRowsCount).forEach(row => {
            // Set display to an empty string to restore its default value (e.g., 'table-row').
            row.style.display = ''; 
        });

        // If there are not enough rows to need a "View More" button, hide it.
        if (rows.length <= visibleRowsCount) {
            viewMoreBtn.style.display = 'none';
        }

        // Add click listener to the button.
        viewMoreBtn.addEventListener('click', () => {
            const nextVisibleRowsCount = visibleRowsCount + ROWS_TO_ADD;
            
            // Show the next set of rows.
            rows.slice(visibleRowsCount, nextVisibleRowsCount).forEach(row => {
                row.style.display = '';
            });

            visibleRowsCount = nextVisibleRowsCount;

            // If all rows are now visible, hide the "View More" button.
            if (visibleRowsCount >= rows.length) {
                viewMoreBtn.style.display = 'none';
            }
        });
    }

    // Initialize pagination for both tables on the page.
    setupPagination('interactions-table', 'view-more-interactions');
    setupPagination('quizzes-table', 'view-more-quizzes');
});
