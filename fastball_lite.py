
# fastball_lite.py

from math import log, pow, exp
import numpy as np

def generate_pnl_forecast(units_sold, avg_price, material_cost, conversion_cost, dev_cost, years=5):
    pnl = []
    for year in range(years):
        revenue = units_sold * avg_price
        cost = material_cost[year] + conversion_cost[year] + dev_cost[year]
        profit = revenue - cost
        pnl.append({
            'Year': year + 1,
            'Revenue': revenue,
            'Cost': cost,
            'Profit': profit
        })
    return pnl

def apply_experience_curve(cost_t0, ct0, ct1, lp):
    decay_factor = -log(lp, 2)
    ratio = (ct0 - ct1) / ct0
    new_cost = cost_t0 * pow(ratio, decay_factor)
    return new_cost

def apply_half_life(d0, dmin, t0, tn, half_life):
    return dmin + (d0 - dmin) * exp(-log(2) * (tn - t0) / half_life)

def monte_carlo_forecast(mean, low, high, runs=1000):
    samples = np.random.triangular(left=low, mode=mean, right=high, size=runs)
    return {
        'mean': float(np.mean(samples)),
        'std_dev': float(np.std(samples)),
        'p5': float(np.percentile(samples, 5)),
        'p95': float(np.percentile(samples, 95))
    }

def evaluate_a3_t(investment, forecast_return, duration):
    npv = forecast_return - investment
    roi = npv / investment if investment != 0 else 0
    return {
        'Investment': investment,
        'Forecast Return': forecast_return,
        'NPV': npv,
        'ROI': roi,
        'Duration': duration
    }

def synthesize_x_matrix(a3_t_list):
    total_investment = sum(item['Investment'] for item in a3_t_list)
    total_npv = sum(item['NPV'] for item in a3_t_list)
    return {
        'Total Investment': total_investment,
        'Total NPV': total_npv,
        'Portfolio ROI': total_npv / total_investment if total_investment != 0 else 0,
        'A3 Bundle': a3_t_list
    }
