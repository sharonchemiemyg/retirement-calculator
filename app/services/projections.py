from app.models.retirement import RetirementInput

class ProjectionService:
    """Service for generating year-by-year projections"""
    
    @staticmethod
    def generate_projections(input_data: RetirementInput, years_to_retirement: int, fund_at_retirement: float) -> list:
        """Generate year-by-year projection until retirement and beyond"""
        
        projections = []
        current_balance = input_data.current_fund_balance
        current_salary = input_data.current_salary
        current_age = input_data.age
        
        # Accumulation phase (until retirement)
        for year in range(years_to_retirement + 1):
            age = current_age + year
            
            # Calculate balance for this year
            if year == 0:
                balance = current_balance
                salary = current_salary
            else:
                # Apply investment return
                balance = current_balance * ((1 + input_data.annual_investment_return) ** year)
                # Add accumulated contributions
                monthly_contributions = input_data.monthly_contribution * 12 * year
                balance += monthly_contributions
                # Apply salary growth
                salary = current_salary * ((1 + input_data.annual_salary_escalation) ** year)
            
            projections.append({
                'year': year,
                'age': age,
                'fund_balance': round(balance, 2),
                'annual_salary': round(salary, 2),
                'annual_contribution': round(input_data.monthly_contribution * 12, 2),
                'phase': 'accumulation'
            })
        
        # Post-retirement phase (next 10 years for illustration)
        retirement_income = fund_at_retirement * 0.04
        withdrawal_rate = 0.04
        
        for year in range(1, 11):
            age = input_data.retirement_age + year
            # Simple withdrawal based on 4% rule
            balance = fund_at_retirement - (retirement_income * year)
            
            projections.append({
                'year': years_to_retirement + year,
                'age': age,
                'fund_balance': max(0, round(balance, 2)),
                'annual_withdrawal': round(retirement_income, 2),
                'phase': 'distribution'
            })
        
        return projections
