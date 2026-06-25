from flask import Blueprint, request, jsonify
from app.services.calculator import RetirementCalculator
from app.models.retirement import RetirementInput
from app.utils.validators import validate_input

api_bp = Blueprint('api', __name__)

@api_bp.route('/calculate', methods=['POST'])
def calculate_retirement():
    """Calculate retirement metrics"""
    
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_input(data)
        if errors:
            return jsonify({'error': 'Validation failed', 'details': errors}), 400
        
        # Create input object
        input_data = RetirementInput(
            age=int(data['age']),
            retirement_age=int(data['retirement_age']),
            current_salary=float(data['current_salary']),
            current_fund_balance=float(data['current_fund_balance']),
            monthly_contribution=float(data['monthly_contribution']),
            annual_investment_return=float(data['annual_investment_return']),
            annual_salary_escalation=float(data['annual_salary_escalation']),
            inflation_rate=float(data['inflation_rate']),
            spouse_age_difference=int(data.get('spouse_age_difference', 3)),
            life_expectancy=int(data.get('life_expectancy', 85))
        )
        
        # Calculate
        result = RetirementCalculator.calculate(input_data)
        
        # Format response
        return jsonify({
            'success': True,
            'data': {
                'income_replacement_ratio': result.income_replacement_ratio,
                'projected_retirement_income': result.projected_retirement_income,
                'status': result.status,
                'projected_fund_at_retirement': result.projected_fund_at_retirement,
                'spouse_pension': result.spouse_pension,
                'years_to_retirement': result.years_to_retirement,
                'projected_lifespan_years': result.projected_lifespan_years,
                'projections': result.projections
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200
