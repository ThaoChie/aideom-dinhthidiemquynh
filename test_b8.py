import numpy as np
from scipy.optimize import minimize

def solve_bai08(discount=0.05, capital_growth=0.06, target_ai=0.85, budget_growth=0.08):
    T = 10
    years = list(range(2026, 2036))
    
    K0, D0, H0, AI0 = 25900.0, 100.0, 500.0, 0.60
    
    def simulate_given_rates(rates, shock_year=None):
        rates = rates.reshape((T, 3))
        K = np.zeros(T+1)
        D = np.zeros(T+1)
        H = np.zeros(T+1)
        AI = np.zeros(T+1)
        Y = np.zeros(T)
        C = np.zeros(T)
        
        K[0], D[0], H[0], AI[0] = K0, D0, H0, AI0
        
        welfare = 0.0
        
        for t in range(T):
            A = 5.0
            if shock_year == years[t]:
                A *= 0.92  # 8% drop in Y
                
            Y[t] = A * (K[t]**0.4) * (H[t]**0.3) * (D[t]**0.1) * (AI[t]**0.2)
            
            i_K, i_D, i_H = rates[t]
            c_t = Y[t] * (1.0 - i_K - i_D - i_H)
            c_t = max(c_t, 1e-6)
            C[t] = c_t
            
            welfare += (c_t ** 0.5) / ((1 + discount) ** t)
            
            K[t+1] = K[t] * (1 - 0.05) + i_K * Y[t]
            D[t+1] = D[t] * (1 - 0.10) + i_D * Y[t]
            H[t+1] = H[t] * (1 - 0.02) + i_H * Y[t]
            
            AI[t+1] = min(1.0, AI[t] + 0.05 * (D[t]/100.0))
            
        return Y, K, C, D, H, AI, welfare

    def objective(rates, shock_year=None):
        *_, welfare = simulate_given_rates(rates, shock_year)
        return -welfare

    def constraint_func(rates):
        rates = rates.reshape((T, 3))
        return 0.9 - np.sum(rates, axis=1)

    bounds = [(0.01, 0.9)] * (3 * T)
    cons = {'type': 'ineq', 'fun': constraint_func}
    
    x0 = np.tile([0.25, 0.05, 0.05], T)
    
    res_opt = minimize(objective, x0, args=(None,), bounds=bounds, constraints=cons, method='SLSQP')
    rates_opt = res_opt.x
    Y_opt, K_opt, C_opt, D_opt, H_opt, AI_opt, w_opt = simulate_given_rates(rates_opt, None)
    
    res_shock = minimize(objective, x0, args=(2028,), bounds=bounds, constraints=cons, method='SLSQP')
    Y_shock, *_ = simulate_given_rates(res_shock.x, 2028)
    w_shock = -res_shock.fun
    
    rates_even = np.tile([0.25, 0.05, 0.05], T)
    _, _, _, _, _, _, w_even = simulate_given_rates(rates_even, None)
    
    rates_front = np.zeros((T, 3))
    rates_front[:5, :] = [0.35, 0.08, 0.08]
    rates_front[5:, :] = [0.15, 0.02, 0.02]
    _, _, _, _, _, _, w_front = simulate_given_rates(rates_front.flatten(), None)
    
    better_strategy = "Tối ưu động (Scipy SLSQP)" if w_opt > w_even else "Trải đều (Đầu tư ổn định)"

    return {
        'years': years,
        'welfare_opt': float(w_opt),
        'K': [float(x) for x in K_opt[:-1]],
        'Y': [float(x) for x in Y_opt],
        'C': [float(x) for x in C_opt],
        'D': [float(x) for x in D_opt[:-1]],
        'H': [float(x) for x in H_opt[:-1]],
        'AI': [float(x) for x in AI_opt[:-1]],
        'welfare_shock': float(w_shock),
        'Y_shock': [float(x) for x in Y_shock],
        'welfare_even': float(w_even),
        'welfare_front': float(w_front),
        'better_strategy': better_strategy,
    }

if __name__ == '__main__':
    res = solve_bai08()
    print("Welfare Opt:", res['welfare_opt'])
    print("Welfare Even:", res['welfare_even'])
    print("Better Strategy:", res['better_strategy'])
    print("Optimization success!")
