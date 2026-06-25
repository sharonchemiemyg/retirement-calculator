document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('calculatorForm');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSpinner = document.querySelector('.loading');
    const errorMessage = document.querySelector('.error-message');

    // Set default values
    document.getElementById('age').value = 35;
    document.getElementById('retirement_age').value = 65;
    document.getElementById('current_salary').value = 120000;
    document.getElementById('current_fund_balance').value = 50000;
    document.getElementById('monthly_contribution').value = 1500;
    document.getElementById('annual_investment_return').value = 0.08;
    document.getElementById('annual_salary_escalation').value = 0.05;
    document.getElementById('inflation_rate').value = 0.04;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading
        loadingSpinner.style.display = 'block';
        errorMessage.style.display = 'none';
        document.querySelectorAll('#resultsSection').forEach(el => el.style.display = 'none');

        // Prepare data
        const formData = new FormData(form);
        const data = {
            age: parseInt(formData.get('age')),
            retirement_age: parseInt(formData.get('retirement_age')),
            current_salary: parseFloat(formData.get('current_salary')),
            current_fund_balance: parseFloat(formData.get('current_fund_balance')),
            monthly_contribution: parseFloat(formData.get('monthly_contribution')),
            annual_investment_return: parseFloat(formData.get('annual_investment_return')),
            annual_salary_escalation: parseFloat(formData.get('annual_salary_escalation')),
            inflation_rate: parseFloat(formData.get('inflation_rate')),
            spouse_age_difference: parseInt(formData.get('spouse_age_difference')),
            life_expectancy: parseInt(formData.get('life_expectancy'))
        };

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.details ? error.details.join(', ') : error.error);
            }

            const result = await response.json();
            displayResults(result.data);
            document.querySelectorAll('#resultsSection').forEach(el => el.style.display = 'block');
            window.scrollTo({ top: document.querySelector('.results-grid').offsetTop, behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Error: ' + error.message;
            errorMessage.style.display = 'block';
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    function displayResults(data) {
        // Update result cards
        document.getElementById('irrValue').textContent = data.income_replacement_ratio.toFixed(2) + '%';
        document.getElementById('fundValue').textContent = 'R' + formatNumber(data.projected_fund_at_retirement);
        document.getElementById('incomeValue').textContent = 'R' + formatNumber(data.projected_retirement_income);
        document.getElementById('spouseValue').textContent = 'R' + formatNumber(data.spouse_pension);

        // Update status
        const statusEl = document.getElementById('status');
        statusEl.className = 'status ' + data.status;
        
        if (data.income_replacement_ratio >= 75) {
            statusEl.textContent = '✓ On Track for Retirement';
        } else if (data.income_replacement_ratio >= 60) {
            statusEl.textContent = '⚠ Below Target - Consider Increasing Contributions';
        } else {
            statusEl.textContent = '✗ Significantly Below Target - Urgent Action Needed';
        }

        // Display projections table
        displayProjections(data.projections);
    }

    function displayProjections(projections) {
        const tbody = document.querySelector('.projections-table tbody');
        tbody.innerHTML = '';

        // Show first 5 years and last 5 years
        const toDisplay = [...projections.slice(0, 6), '...', ...projections.slice(-5)];

        toDisplay.forEach((proj, index) => {
            if (proj === '...') {
                const tr = document.createElement('tr');
                tr.innerHTML = '<td colspan="5" style="text-align: center; color: #999;">...</td>';
                tbody.appendChild(tr);
            } else {
                const tr = document.createElement('tr');
                const phase = proj.phase === 'accumulation' ? 'Saving' : 'Spending';
                const amount = proj.phase === 'accumulation' ? proj.annual_contribution : proj.annual_withdrawal;
                
                tr.innerHTML = `
                    <td>${proj.year}</td>
                    <td>${proj.age}</td>
                    <td>R${formatNumber(proj.fund_balance)}</td>
                    <td>${phase}</td>
                    <td>R${formatNumber(amount)}</td>
                `;
                tbody.appendChild(tr);
            }
        });
    }

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
});
