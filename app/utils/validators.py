def validate_input(data: dict) -> list:
    """Validate input data"""
    
    errors = []
    required_fields = [
        'age', 'retirement_age', 'current_salary', 'current_fund_balance',
        'monthly_contribution', 'annual_investment_return', 
        'annual_salary_escalation', 'inflation_rate'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    if not errors:
        # Validate values
        try:
            age = int(data['age'])
            retirement_age = int(data['retirement_age'])
            current_salary = float(data['current_salary'])
            
            if age < 18:
                errors.append("Age must be at least 18")
            if retirement_age <= age:
                errors.append("Retirement age must be greater than current age")
            if current_salary < 0:
                errors.append("Current salary cannot be negative")
            if float(data['current_fund_balance']) < 0:
                errors.append("Fund balance cannot be negative")
            if float(data['monthly_contribution']) < 0:
                errors.append("Monthly contribution cannot be negative")
                
        except ValueError as e:
            errors.append(f"Invalid data type: {str(e)}")
    
    return errors
