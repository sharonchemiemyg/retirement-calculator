import math
from app.models.retirement import RetirementInput, RetirementResult
from app.services.projections import ProjectionService

class RetirementCalculator:
    """Main calculator for IRR (Income Replacement Ratio)"""
    
    # Constants
    TARGET_REPLACEMENT_RATIO = 0.75  # 75% is comfortable retirement
    WITHDRAWAL_RATE = 0.04  # 4% rule
    SPOUSE_PENSION_PERCENTAGE = 0.50  # 50% of pension
    GUARANTEE_PERIOD_YEARS = 5
    
    @staticmethod
    def calculate(input_data: RetirementInput) -> RetirementResult:
        """Calculate retirement metrics and projections"""
        
        # Basic calculations
        years_to_retirement = input_data.retirement_age - input_data.age
        projected_lifespan = input_data.life_expectancy - input_data.retirement_age
        
        # Calculate fund balance at retirement
        fund_at_retirement = RetirementCalculator._calculate_fund_at_retirement(
            input_data, years_to_retirement
        )
        
        # Calculate retirement income using 4% rule
        retirement_income = fund_at_retirement * RetirementCalculator.WITHDRAWAL_RATE
        
        # Adjust for inflation to get today's equivalent
        retirement_income_today_equivalent = retirement_income / (
            (1 + input_data.inflation_rate) ** years_to_retirement
        )
        
        # Calculate salary at retirement (for comparison)
        salary_at_retirement = input_data.current_salary * (
            (1 + input_data.annual_salary_escalation) ** years_to_retirement
        )
        
        # Calculate income replacement ratio
        if salary_at_retirement > 0:
            irr = (retirement_income / salary_at_retirement) * 100
        else:
            irr = 0
        
        # Determine status
        if irr >= (RetirementCalculator.TARGET_REPLACEMENT_RATIO * 100):
            status = 'on_track'
        elif irr >= (RetirementCalculator.TARGET_REPLACEMENT_RATIO * 100 * 0.8):
            status = 'below_target'
        else:
            status = 'below_target'
        
        # Calculate spouse pension
        spouse_pension = retirement_income * RetirementCalculator.SPOUSE_PENSION_PERCENTAGE
        
        # Generate year-by-year projections
        projections = ProjectionService.generate_projections(
            input_data, years_to_retirement, fund_at_retirement
        )
        
        return RetirementResult(
            income_replacement_ratio=round(irr, 2),
            projected_retirement_income=round(retirement_income, 2),
            status=status,
            projected_fund_at_retirement=round(fund_at_retirement, 2),
            spouse_pension=round(spouse_pension, 2),
            years_to_retirement=years_to_retirement,
            projected_lifespan_years=projected_lifespan,
            projections=projections
        )
    
    @staticmethod
    def _calculate_fund_at_retirement(input_data: RetirementInput, years: int) -> float:
        """Calculate fund balance at retirement using Future Value formula"""
        
        # Future value of current balance
        current_balance_fv = input_data.current_fund_balance * (
            (1 + input_data.annual_investment_return) ** years
        )
        
        # Future value of annuity (monthly contributions)
        monthly_rate = (1 + input_data.annual_investment_return) ** (1/12) - 1
        months = years * 12
        
        # FV of annuity formula: PMT * [((1 + r)^n - 1) / r]
        if monthly_rate > 0:
            annuity_fv = input_data.monthly_contribution * (
                ((1 + monthly_rate) ** months - 1) / monthly_rate
            )
        else:
            annuity_fv = input_data.monthly_contribution * months
        
        total_fund = current_balance_fv + annuity_fv
        return total_fund
