import math

def read_netlist(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    V_m = 0
    frequency = 0
    R = 0
    L = 0

    for line in lines:
        parts = line.split()
        if parts[0].startswith('*') or parts[0].startswith('.'):
            continue
        if parts[0].startswith('V'):
            # Extract the amplitude and frequency from SINE(0 220 60)
            sine_params = line[line.index('SINE(') + 5:line.index(')')].split()
            V_m = float(sine_params[1])
            frequency = float(sine_params[2])
        elif parts[0].startswith('R'):
            R = float(parts[3].replace('R', ''))
        elif parts[0].startswith('L'):
            L = float(parts[3].replace('L', ''))
    
    return V_m, frequency, R, L

def calculate_power_factor(V_m, frequency, R, L):
    omega = 2 * math.pi * frequency
    X_L = omega * L
    Z = math.sqrt(R**2 + X_L**2)
    phi = math.atan(X_L / R)
    power_factor = math.cos(phi)
    return power_factor, phi, Z

def calculate_corrective_capacitor(V_m, frequency, R, L, target_pf):
    V_rms = V_m / math.sqrt(2)
    omega = 2 * math.pi * frequency
    power_factor, phi_old, Z = calculate_power_factor(V_m, frequency, R, L)
    
    S = V_rms**2 / Z
    P = S * power_factor
    Q_old = S * math.sin(phi_old)
    
    phi_new = math.acos(target_pf)
    Q_new = P * math.tan(phi_new)
    
    Q_C = Q_old - Q_new
    C = Q_C / (V_rms**2 * omega)
    
    return C, power_factor

def main():
    netlist_path = 'C:\\Users\\leona\\Desktop\\trabalhoCE\\circuito_e_codigo\\Circuito_sem_capacitor.net'  # Update with your netlist file path
    target_pf = float(input("Enter desired power factor (e.g., 0.95): "))
    
    V_m, frequency, R, L = read_netlist(netlist_path)
    power_factor, phi, Z = calculate_power_factor(V_m, frequency, R, L)
    C, current_pf = calculate_corrective_capacitor(V_m, frequency, R, L, target_pf)
    
    print(f"Current Power Factor: {current_pf:.3f}")
    print(f"Required Capacitor to correct PF to {target_pf}: {C * 1e6:.3f} μF")

if __name__ == "__main__":
    main()
