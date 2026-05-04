"""
=============================================================================
GCPV DESIGN AND SIZING — GROUP 24
=============================================================================
Course      : Renewable Energy (Spring 2025/2026)
PV Module   : Trina Solar ALLMAXPLUS 310W
Inverter    : Sungrow SG250HX
DC/AC Ratio : 1.24
=============================================================================
"""

import math


# =============================================================================
# SECTION 1: PARAMETERS
# All values sourced directly from datasheets or coursework Table 1.
# =============================================================================

# --- PV Module: Trina Solar ALLMAXPLUS 310W (STC) ---
Pmax_STC  = 310     # W      | Peak power at STC
Voc_STC   = 40.2    # V      | Open circuit voltage at STC
Vmp_STC   = 33.1    # V      | Max power voltage at STC
Isc_STC   = 9.94    # A      | Short circuit current at STC
Imp_STC   = 9.37    # A      | Max power current at STC
beta_voc  = -0.29   # %/°C   | Temperature coefficient of Voc
gamma_pmax= -0.39   # %/°C   | Temperature coefficient of Pmax (used as beta_vpmax)
Vsys_max  = 1000    # V      | Max system voltage (IEC) — module damage limit


# --- Inverter: Sungrow SG250HX ---
Pnom_inv      = 225_000  # W  | Rated AC output power @ 40°C (derated from 250kVA)
N_mppt        = 12       # —  | Number of independent MPPT inputs
Vmax_abs_inv  = 1500     # V  | Absolute max DC input voltage (inverter damage limit)
Vmin_mppt_inv = 860      # V  | MPPT operating window — minimum
Vmax_mppt_inv = 1300     # V  | MPPT operating window — maximum
Vstart_inv    = 600      # V  | Startup (minimum) voltage to wake inverter
Vrated_inv    = 1160     # V  | Nominal/rated DC input voltage (max efficiency point)
Isc_max_MPPT  = 50       # A  | Max DC short-circuit current per MPPT input

"""
# --- Inverter: Huawei SUN2000-8KTL ---
Pnom_inv      = 8000     # W  | Rated AC output power @ 40°C (derated from 250kVA)
N_mppt        = 2        # —  | Number of independent MPPT inputs
Vmax_abs_inv  = 1000     # V  | Absolute max DC input voltage (inverter damage limit)
Vmin_mppt_inv = 320      # V  | MPPT operating window — minimum
Vmax_mppt_inv = 800      # V  | MPPT operating window — maximum
Vstart_inv    = 200      # V  | Startup (minimum) voltage to wake inverter
Vrated_inv    = 620      # V  | Nominal/rated DC input voltage (max efficiency point)
Isc_max_MPPT  = 25       # A  | Max DC short-circuit current per MPPT input
"""

# --- Design Assumptions: Group 24 ---
T_mod_max  = 72     # °C  | Highest module temperature (from Table 1)
T_mod_min  = 25     # °C  | Lowest module temperature (from Table 1)
T_STC      = 25     # °C  | Standard Test Condition reference temperature
DC_AC      = 1.24   # —   | DC/AC oversizing ratio (from Table 1)
cable_loss = 3      # %   | Maximum DC cable loss
eta_cable  = 1 - (cable_loss / 100)   # = 0.97 | Cable efficiency factor
sf1        = 1.25   # —   | Safety factor for short circuit current (industry standard)


# =============================================================================
# SECTION 2: HELPER FUNCTIONS
# Small reusable utilities used across all calculations.
# =============================================================================

def print_section(title):
    """Prints a formatted section header."""
    width = 80
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def print_result(label, value, unit=""):
    """Prints a clearly formatted final result."""
    unit_str = f" {unit}" if unit else ""
    print(f"  >>> {label} = {value}{unit_str}")


def voc_at_temperature(T_mod):
    """
    Calculates Voc adjusted for a given module temperature.

    Formula: Voc(T) = Voc_STC × [1 + (beta_voc/100) × (T_mod - T_STC)]

    Args:
        T_mod (float): Module temperature in °C.

    Returns:
        float: Temperature-corrected Voc in Volts.
    """
    return Voc_STC * (1 + (beta_voc / 100) * (T_mod - T_STC))


def vmp_at_temperature(T_mod):
    """
    Calculates Vmp adjusted for a given module temperature.
    Note: beta_vpmax is not listed in the ALLMAX datasheet,
    so we use gamma_pmax as an approximation (standard practice).

    Formula: Vmp(T) = Vmp_STC × [1 + (gamma_pmax/100) × (T_mod - T_STC)]

    Args:
        T_mod (float): Module temperature in °C.

    Returns:
        float: Temperature-corrected Vmp in Volts.
    """
    return Vmp_STC * (1 + (gamma_pmax / 100) * (T_mod - T_STC))


# =============================================================================
# SECTION 3: CALCULATION FUNCTIONS (Parts a–k)
# Each function handles exactly one sub-question.
# =============================================================================

def part_a_total_modules():
    """
    (a) Total number of PV modules per inverter and per MPPT.

    The DC array size is determined by the DC/AC oversizing ratio applied
    to the inverter's rated AC power. The number of modules is then found
    by dividing total DC power by each module's rated power.
    """
    print_section("(a) Total PV Modules per Inverter and per MPPT")

    P_array_STC = DC_AC * Pnom_inv
    print(f"  P_array_STC = DC/AC × Pnom_inv")
    print(f"              = {DC_AC} × {Pnom_inv:,} W")
    print(f"              = {P_array_STC:,.1f} W")

    N_t_per_inv = math.floor(P_array_STC / Pmax_STC)
    print(f"\n  N_t_per_inv = floor(P_array_STC / Pmax_STC)")
    print(f"              = floor({P_array_STC:,.1f} / {Pmax_STC})")
    print(f"              = floor({P_array_STC / Pmax_STC:.4f})")

    N_t_per_mppt = math.ceil(N_t_per_inv / N_mppt)
    print(f"\n  N_t_per_mppt = ceil(N_t_per_inv / N_mppt)")
    print(f"               = ceil({N_t_per_inv} / {N_mppt})")
    print(f"               = ceil({N_t_per_inv / N_mppt:.4f})")

    print_result("N_t_per_inv",  N_t_per_inv,  "modules")
    print_result("N_t_per_mppt", N_t_per_mppt, "modules per MPPT")

    return N_t_per_inv, N_t_per_mppt


def part_b_max_series_inverter():
    """
    (b) Maximum modules in series that will NOT damage the inverter.

    At lowest temperature, Voc is at its highest (cold = higher voltage).
    This maximum string voltage must not exceed the inverter's absolute
    maximum DC input voltage.
    """
    print_section("(b) Max Series Modules — Won't Damage Inverter")

    Voc_max = voc_at_temperature(T_mod_min)
    print(f"  Voc_max = Voc_STC × [1 + (beta_voc/100) × (T_mod_min - T_STC)]")
    print(f"          = {Voc_STC} × [1 + ({beta_voc}/100) × ({T_mod_min} - {T_STC})]")
    print(f"          = {Voc_STC} × [1 + {(beta_voc/100)*(T_mod_min - T_STC):.5f}]")
    print(f"          = {Voc_max:.4f} V")

    Ns_max_abs = math.floor(Vmax_abs_inv / Voc_max)
    print(f"\n  Ns_max_abs = floor(Vmax_abs_inv / Voc_max)")
    print(f"             = floor({Vmax_abs_inv} / {Voc_max:.4f})")
    print(f"             = floor({Vmax_abs_inv / Voc_max:.4f})")

    print_result("Voc_max",    round(Voc_max, 4), "V")
    print_result("Ns_max_abs", Ns_max_abs, "modules")

    return Ns_max_abs, Voc_max


def part_c_max_series_mppt_low_temp():
    """
    (c) Maximum modules in series for MPPT operation at lowest temperature.

    During normal operation, string voltage follows Vmp (not Voc).
    At lowest temperature, Vmp is highest, and it must stay within
    the inverter's MPPT operating window maximum.
    """
    print_section("(c) Max Series Modules — MPPT Mode at Lowest Temperature")

    Vmp_max = vmp_at_temperature(T_mod_min)
    print(f"  Vmp_max = Vmp_STC × [1 + (gamma_pmax/100) × (T_mod_min - T_STC)]")
    print(f"          = {Vmp_STC} × [1 + ({gamma_pmax}/100) × ({T_mod_min} - {T_STC})]")
    print(f"          = {Vmp_STC} × [1 + {(gamma_pmax/100)*(T_mod_min - T_STC):.5f}]")
    print(f"          = {Vmp_max:.4f} V")
    print(f"  Note: beta_vpmax not listed in datasheet → using gamma_pmax = {gamma_pmax} %/°C")

    Ns_max_mppt = math.floor(Vmax_mppt_inv / Vmp_max)
    print(f"\n  Ns_max_mppt = floor(Vmax_mppt_inv / Vmp_max)")
    print(f"              = floor({Vmax_mppt_inv} / {Vmp_max:.4f})")
    print(f"              = floor({Vmax_mppt_inv / Vmp_max:.4f})")

    print_result("Vmp_max",     round(Vmp_max, 4), "V")
    print_result("Ns_max_mppt", Ns_max_mppt, "modules")

    return Ns_max_mppt, Vmp_max


def part_d_max_series_pv_cell(Voc_max):
    """
    (d) Maximum modules in series that will NOT damage the PV cell.

    The PV module itself has a maximum rated system voltage (Vsys_max).
    The open circuit voltage of the string must not exceed this limit,
    using Voc_max (worst case at lowest temperature).
    """
    print_section("(d) Max Series Modules — Won't Damage PV Cell")

    Ns_max_pv = math.floor(Vsys_max / Voc_max)
    print(f"\n  Ns_max_pv = floor(Vsys_max / Voc_max)")
    print(f"            = floor({Vsys_max} / {Voc_max:.4f})")
    print(f"            = floor({Vsys_max / Voc_max:.4f})")

    print_result("Vsys_max",  Vsys_max, "V")
    print_result("Ns_max_pv", Ns_max_pv, "modules")

    return Ns_max_pv


def part_e_final_max_series(Ns_max_abs, Ns_max_mppt, Ns_max_pv):
    """
    (e) Final maximum number of modules in series for this project.

    Takes the LOWEST (most restrictive) value from parts (b), (c), and (d).
    This ensures all three constraints — inverter damage, MPPT window,
    and PV cell damage — are simultaneously satisfied.
    """
    print_section("(e) Final Maximum Modules in Series")

    Ns_max = min(Ns_max_abs, Ns_max_mppt, Ns_max_pv)
    constraints = {
        "Ns_max_abs  (inverter damage limit)": Ns_max_abs,
        "Ns_max_mppt (MPPT upper window)    ": Ns_max_mppt,
        "Ns_max_pv   (PV cell damage limit) ": Ns_max_pv,
    }

    print(f"\n  Summary of upper constraints:")
    for label, val in constraints.items():
        marker = "  ← BINDING" if val == Ns_max else ""
        print(f"    {label} = {val}{marker}")

    print_result("Ns_max (final)", Ns_max, "modules per string")

    return Ns_max


def part_f_min_series_startup():
    """
    (f) Minimum modules in series to start up the inverter at highest temperature.

    At the highest temperature, Voc is at its lowest. Before startup,
    the string operates at open circuit voltage. The inverter requires
    a minimum startup voltage to begin operation.
    """
    print_section("(f) Min Series Modules — Inverter Start-Up at Highest Temperature")

    Voc_min = voc_at_temperature(T_mod_max)
    print(f"  Voc_min = Voc_STC × [1 + (beta_voc/100) × (T_mod_max - T_STC)]")
    print(f"          = {Voc_STC} × [1 + ({beta_voc}/100) × ({T_mod_max} - {T_STC})]")
    print(f"          = {Voc_STC} × [1 + {(beta_voc/100)*(T_mod_max - T_STC):.5f}]")
    print(f"          = {Voc_min:.4f} V")

    Ns_min_start = math.ceil(Vstart_inv / Voc_min)
    print(f"\n  Ns_min_start = ceil(Vstart_inv / Voc_min)")
    print(f"               = ceil({Vstart_inv} / {Voc_min:.4f})")
    print(f"               = ceil({Vstart_inv / Voc_min:.4f})")

    print_result("Voc_min",      round(Voc_min, 4), "V")
    print_result("Ns_min_start", Ns_min_start, "modules")

    return Ns_min_start, Voc_min


def part_g_min_series_mppt_high_temp():
    """
    (g) Minimum modules in series for MPPT operation at highest temperature.

    During normal operation the string voltage follows Vmp. At highest
    temperature Vmp is at its lowest. The derated string voltage
    (after cable losses) must still reach the inverter's MPPT minimum.
    """
    print_section("(g) Min Series Modules — MPPT Mode at Highest Temperature")

    Vmp_min = vmp_at_temperature(T_mod_max)
    print(f"  Vmp_min = Vmp_STC × [1 + (gamma_pmax/100) × (T_mod_max - T_STC)]")
    print(f"          = {Vmp_STC} × [1 + ({gamma_pmax}/100) × ({T_mod_max} - {T_STC})]")
    print(f"          = {Vmp_STC} × [1 + {(gamma_pmax/100)*(T_mod_max - T_STC):.5f}]")
    print(f"          = {Vmp_min:.4f} V")
    print(f"\n  Cable efficiency (eta_cable) = 1 - {cable_loss}% = {eta_cable}")

    Ns_min_mppt = math.ceil(Vmin_mppt_inv / (Vmp_min * eta_cable))
    print(f"\n  Ns_min_mppt = ceil(Vmin_mppt_inv / (Vmp_min × eta_cable))")
    print(f"              = ceil({Vmin_mppt_inv} / ({Vmp_min:.4f} × {eta_cable}))")
    print(f"              = ceil({Vmin_mppt_inv} / {Vmp_min * eta_cable:.4f})")
    print(f"              = ceil({Vmin_mppt_inv / (Vmp_min * eta_cable):.4f})")

    print_result("Vmp_min",     round(Vmp_min, 4), "V")
    print_result("Ns_min_mppt", Ns_min_mppt, "modules")

    return Ns_min_mppt


def part_h_final_min_series(Ns_min_start, Ns_min_mppt):
    """
    (h) Final minimum number of modules in series for this project.

    Takes the HIGHEST (most demanding) value from parts (f) and (g).
    This ensures both the startup condition AND MPPT operation are met
    even in the worst-case high-temperature scenario.
    """
    print_section("(h) Final Minimum Modules in Series")

    Ns_min = max(Ns_min_start, Ns_min_mppt)
    constraints = {
        "Ns_min_start (startup voltage)  ": Ns_min_start,
        "Ns_min_mppt  (MPPT lower window)": Ns_min_mppt,
    }

    print(f"\n  Summary of lower constraints:")
    for label, val in constraints.items():
        marker = "  ← BINDING" if val == Ns_min else ""
        print(f"    {label} = {val}{marker}")

    print_result("Ns_min (final)", Ns_min, "modules per string")

    return Ns_min


def part_i_recommended_series(Ns_min_mppt, Ns_max_mppt, Ns_max):
    """
    (i) Recommended number of modules in series for maximum inverter efficiency.

    Finds where the rated (optimal) inverter voltage sits within the MPPT
    window as a percentage, then maps that percentage onto the Ns range
    to get the operating point closest to peak inverter efficiency.

    Args:
        Ns_min_mppt (int): Minimum series modules for MPPT (from part g).
        Ns_max_mppt (int): Maximum series modules for MPPT (from part c).
        Ns_max      (int): Hard maximum series modules (from part e).

    Returns:
        int: Recommended number of modules in series.
    """
    print_section("(i) Recommended Modules in Series — Maximum Inverter Efficiency")

    W_pct = ((Vrated_inv - Vmin_mppt_inv) / (Vmax_mppt_inv - Vmin_mppt_inv)) * 100
    print(f"  W% = (Vrated_inv - Vmin_mppt_inv) / (Vmax_mppt_inv - Vmin_mppt_inv) × 100")
    print(f"     = ({Vrated_inv} - {Vmin_mppt_inv}) / ({Vmax_mppt_inv} - {Vmin_mppt_inv}) × 100")
    print(f"     = {Vrated_inv - Vmin_mppt_inv} / {Vmax_mppt_inv - Vmin_mppt_inv} × 100")
    print(f"     = {W_pct:.2f}%")

    Ns_rec_raw = Ns_min_mppt + (W_pct / 100) * (Ns_max_mppt - Ns_min_mppt)
    print(f"\n  Ns_rec (raw) = Ns_min_mppt + (W%/100) × (Ns_max_mppt - Ns_min_mppt)")
    print(f"               = {Ns_min_mppt} + ({W_pct:.2f}/100) × ({Ns_max_mppt} - {Ns_min_mppt})")
    print(f"               = {Ns_min_mppt} + {(W_pct/100)*(Ns_max_mppt - Ns_min_mppt):.4f}")
    print(f"               = {Ns_rec_raw:.4f}")

    Ns_rec_floor = math.floor(Ns_rec_raw)
    Ns_rec_ceil  = math.ceil(Ns_rec_raw)

    # Both options must be checked: they must not exceed Ns_max
    candidates = []
    for candidate in [Ns_rec_floor, Ns_rec_ceil]:
        if candidate <= Ns_max:
            candidates.append(candidate)

    Ns_rec = max(candidates) if candidates else Ns_max
    print(f"\n  Candidate values: floor={Ns_rec_floor}, ceil={Ns_rec_ceil}")
    print(f"  Ns_max constraint check (must be ≤ {Ns_max}):")
    for candidate in [Ns_rec_floor, Ns_rec_ceil]:
        status = "✓ valid" if candidate <= Ns_max else "✗ exceeds Ns_max — excluded"
        print(f"    {candidate} → {status}")

    print(f"\n  W% = {W_pct:.2f}%")
    print_result("Ns_rec", Ns_rec, "modules per string")

    return Ns_rec


def part_j_max_parallel_strings():
    """
    (j) Maximum number of parallel strings per MPPT input.

    The total short circuit current from all parallel strings must not
    exceed the inverter's maximum input current per MPPT. A safety
    factor (sf1) is applied to account for irradiance spikes.
    """
    print_section("(j) Maximum Parallel Strings per MPPT")

    Np_max = math.floor(Isc_max_MPPT / (Isc_STC * sf1))
    print(f"  Np_max = floor(Isc_max_MPPT / (Isc_STC × sf1))")
    print(f"         = floor({Isc_max_MPPT} / ({Isc_STC} × {sf1}))")
    print(f"         = floor({Isc_max_MPPT} / {Isc_STC * sf1:.4f})")
    print(f"         = floor({Isc_max_MPPT / (Isc_STC * sf1):.4f})")
    print(f"\n  Note: sf1 = {sf1} is a standard industry safety factor.")

    print_result("Np_max", Np_max, "strings per MPPT")

    return Np_max


def part_k_array_configurations(N_t_per_mppt, Ns_min, Ns_max, Ns_rec, Np_max, N_mppt):
    """
    (k) Determine all possible PV array configurations.

    Systematically evaluates configurations by checking which parameter 
    (Ns or Np) has the smaller range, and iterates based on that parameter
    to find the optimal layout.

    Args:
        N_t_per_mppt (int): Target total modules per MPPT (from part a).
        Ns_min       (int): Minimum series modules per string (from part h).
        Ns_max       (int): Maximum series modules per string (from part e).
        Ns_rec       (int): Recommended series modules (from part i).
        Np_max       (int): Maximum parallel strings per MPPT (from part j).
        N_mppt       (int): Number of MPPT inputs (from part b).
    """
    print_section("(k) Possible PV Array Configurations")

    print(f"  Inputs:")
    print(f"    N_t_per_mppt = {N_t_per_mppt} modules")
    print(f"    Ns_min       = {Ns_min}")
    print(f"    Ns_max       = {Ns_max}")
    print(f"    Ns_rec       = {Ns_rec}")
    print(f"    Np_max       = {Np_max} strings per MPPT")
    print(f"    N_mppt       = {N_mppt} MPPT inputs")

    # --- Catch impossible hardware mismatch ---
    if Ns_min > Ns_max:
        print("\n  [!] CRITICAL DESIGN ERROR: IMPOSSIBLE CONFIGURATION [!]")
        print(f"      The minimum modules required to operate (Ns_min = {Ns_min})")
        print(f"      exceeds the maximum safe limit of the hardware (Ns_max = {Ns_max}).")
        print("      No workable arrays can be formed. Hardware mismatch detected.")
        print("\n  ★  NO WORKABLE CONFIGURATIONS FOUND.")
        return []  # Stop the function here and return empty list

    # 1. Determine which parameter has the smaller range
    range_Ns = (Ns_max - Ns_min) + 1
    range_Np = Np_max
    
    print(f"\n  Range Comparison:")
    print(f"    Ns range: {range_Ns} options ({Ns_min} to {Ns_max})")
    print(f"    Np range: {range_Np} options (1 to {Np_max})")

    options_to_test = []
    
    # 2. Iterate based on the smaller range
    if range_Ns < range_Np:
        print("\n  Iterating based on Ns (smaller range):")
        for Ns_test in range(Ns_min, Ns_max + 1):
            Np_calc = N_t_per_mppt // Ns_test  # Round down per MS1837
            options_to_test.append({
                "Np": Np_calc, "Ns": Ns_test
            })
    else:
        print("\n  Iterating based on Np (smaller or equal range):")
        for Np_test in range(1, Np_max + 1):
            Ns_calc = N_t_per_mppt // Np_test  # Round down per MS1837
            options_to_test.append({
                "Np": Np_test, "Ns": Ns_calc
            })

    # 3. Print Header
    header = f"  {'Np':>5}  {'Ns':>7}  {'Total/MPPT':>11}  {'Total (all)':>12}  {'Workable?':>10} Comments"
    print("\n" + header)
    print("  " + "-" * (len(header) - 2))

    workable_options = []

    # 4. Evaluate the generated options
    for opt in options_to_test:
        Np = opt["Np"]
        Ns = opt["Ns"]
        total_mppt = Ns * Np
        total_all  = total_mppt * N_mppt
        
        # Check validity limits based on both parameters
        valid_Np = 1 <= Np <= Np_max
        valid_Ns = Ns_min <= Ns <= Ns_max
        in_range = valid_Np and valid_Ns
        
        workable = "✓ YES" if in_range else "✗ NO"

        # Build comment
        notes = []
        if not in_range:
            if not valid_Ns:
                if Ns > Ns_max: notes.append(f"Ns={Ns} exceeds Ns_max={Ns_max}")
                else: notes.append(f"Ns={Ns} below Ns_min={Ns_min}")
            if not valid_Np:
                if Np > Np_max: notes.append(f"Np={Np} exceeds Np_max={Np_max}")
                else: notes.append(f"Np={Np} below 1")
        else:
            if total_mppt == N_t_per_mppt:
                notes.append("exact target match")
            else:
                diff = abs(total_mppt - N_t_per_mppt)
                notes.append(f"off by {diff} from target")
                
            if Ns == Ns_rec:
                notes.append("Ns = Ns_rec ✓ preferred")
            elif abs(Ns - Ns_rec) <= 1:
                notes.append("Ns close to Ns_rec")
                
            if Ns == Ns_max or Ns == Ns_min:
                notes.append("Ns at border limit")
                
        comment = "; ".join(notes)

        print(f"  {Np:>5}  {Ns:>7}  {total_mppt:>11}  {total_all:>12}  {workable:>10}  {comment}")

        if in_range:
            workable_options.append({
                "Np": Np, "Ns": Ns,
                "total_mppt": total_mppt, "total_all": total_all,
                "comment": comment
            })

    # 5. Recommend best option
    print(f"\n  Workable options summary:")
    best = None
    for opt in workable_options:
        is_rec = opt["Ns"] == Ns_rec
        not_border = opt["Ns"] not in [Ns_min, Ns_max]
        closest = abs(opt["total_mppt"] - N_t_per_mppt)
        print(f"    Np={opt['Np']}, Ns={opt['Ns']}, Total={opt['total_all']} | {opt['comment']}")
        
        if best is None:
            best = opt
        else:
            best_closest = abs(best["total_mppt"] - N_t_per_mppt)
            # Prioritize Ns_rec match without border limits, then prioritize closest to target total
            if (is_rec and not_border) and (not (best["Ns"] == Ns_rec) or closest < best_closest):
                best = opt
            elif closest < best_closest and not (best["Ns"] == Ns_rec):
                best = opt

    if best:
        print(f"\n  ★  RECOMMENDED CONFIGURATION:")
        print(f"     {best['Np']} strings × {best['Ns']} modules per string per MPPT")
        print(f"     × {N_mppt} MPPTs = {best['total_all']} total modules per inverter")
    else:
        print(f"\n  ★  NO WORKABLE CONFIGURATIONS FOUND.")

    return workable_options

# =============================================================================
# SECTION 4: SUMMARY TABLE
# Collects all key results and prints a clean consolidated reference table.
# =============================================================================


def print_summary(results: dict):
    """Prints a formatted summary of all computed results."""
    print_section("FINAL RESULTS SUMMARY")

    rows = [
        ("(a) Total modules per inverter",    "N_t_per_inv",  results["N_t_per_inv"],  "modules"),
        ("(a) Total modules per MPPT",         "N_t_per_mppt", results["N_t_per_mppt"], "modules/MPPT"),
        ("(b) Max series — inverter safe",     "Ns_max_abs",   results["Ns_max_abs"],   "modules"),
        ("(c) Max series — MPPT low temp",     "Ns_max_mppt",  results["Ns_max_mppt"],  "modules"),
        ("(d) Max series — PV cell safe",      "Ns_max_pv",    results["Ns_max_pv"],    "modules"),
        ("(e) FINAL max series",               "Ns_max",       results["Ns_max"],       "modules  ◄"),
        ("(f) Min series — startup",           "Ns_min_start", results["Ns_min_start"], "modules"),
        ("(g) Min series — MPPT high temp",    "Ns_min_mppt",  results["Ns_min_mppt"],  "modules"),
        ("(h) FINAL min series",               "Ns_min",       results["Ns_min"],       "modules  ◄"),
        ("(i) Recommended series",             "Ns_rec",       results["Ns_rec"],       "modules  ◄"),
        ("(j) Max parallel strings per MPPT",  "Np_max",       results["Np_max"],       "strings"),
    ]

    print(f"\n  {'Description':<38} {'Symbol':<15} {'Value':>7}  {'Unit'}")
    print("  " + "-" * 72)
    for desc, sym, val, unit in rows:
        print(f"  {desc:<38} {sym:<15} {val:>7}  {unit}")

    # --- NEW: Flag impossible range in summary ---
    if results['Ns_min'] > results['Ns_max']:
        print(f"\n")
        print(f"  Valid Ns range: IMPOSSIBLE [{results['Ns_min']} > {results['Ns_max']}]")
        print(f"  [!] HARDWARE CONFLICT: Inverter requires minimum {results['Ns_min']} modules,")
        print(f"      but PV safety limits restrict strings to maximum {results['Ns_max']} modules.")
    else:
        print(f"\n  Valid Ns range: [{results['Ns_min']} ... {results['Ns_max']}]")
        print(f"  Recommended Ns (max efficiency): {results['Ns_rec']}")

  


# =============================================================================
# SECTION 5: MAIN ENTRY POINT
# Orchestrates the full design calculation in sequence.
# =============================================================================

def main():
    print("\n" + "#" * 70)
    print("  GCPV DESIGN AND SIZING — GROUP 24")
    print("  Trina Solar ALLMAXPLUS 310W  |  Sungrow SG250HX")
    print("#" * 70)

    # Run calculations in order — each builds on the previous
    N_t_per_inv,  N_t_per_mppt = part_a_total_modules()
    Ns_max_abs,   Voc_max      = part_b_max_series_inverter()
    Ns_max_mppt,  Vmp_max      = part_c_max_series_mppt_low_temp()
    Ns_max_pv                  = part_d_max_series_pv_cell(Voc_max)
    Ns_max                     = part_e_final_max_series(Ns_max_abs, Ns_max_mppt, Ns_max_pv)
    Ns_min_start, Voc_min      = part_f_min_series_startup()
    Ns_min_mppt                = part_g_min_series_mppt_high_temp()
    Ns_min                     = part_h_final_min_series(Ns_min_start, Ns_min_mppt)
    Ns_rec                     = part_i_recommended_series(Ns_min_mppt, Ns_max_mppt, Ns_max)
    Np_max                     = part_j_max_parallel_strings()

    part_k_array_configurations(N_t_per_mppt, Ns_min, Ns_max, Ns_rec, Np_max, N_mppt)

    # Collect all results for the summary table
    results = {
        "N_t_per_inv":  N_t_per_inv,
        "N_t_per_mppt": N_t_per_mppt,
        "Ns_max_abs":   Ns_max_abs,
        "Ns_max_mppt":  Ns_max_mppt,
        "Ns_max_pv":    Ns_max_pv,
        "Ns_max":       Ns_max,
        "Ns_min_start": Ns_min_start,
        "Ns_min_mppt":  Ns_min_mppt,
        "Ns_min":       Ns_min,
        "Ns_rec":       Ns_rec,
        "Np_max":       Np_max,
    }
    print_summary(results)

    print("\n" + "#" * 70)
    print("  END OF CALCULATION")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    main()