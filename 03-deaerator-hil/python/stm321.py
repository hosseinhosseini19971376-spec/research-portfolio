import os
import json
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.optimize import differential_evolution, fsolve
import scipy.optimize as opt
from pyXSteam.XSteam import XSteam
from scipy.optimize import least_squares
import serial
import threading
# سایر ایمپورت‌های قبلی شما...

# ==========================================
# 1. Steady State & Thermodynamic Initialization
# ==========================================
SYSTEM_PARAMS = {
    "m_w_in_nom": {"val": 24.04, "desc": "Initial inlet water flow [kg/s]", "show_in_table": True},
    "m_s_in_nom": {"val": 0.1585, "desc": "Initial inlet steam flow [kg/s]", "show_in_table": True},
    "T_w_in_C": {"val": 140.0, "desc": "Inlet water temp [C]", "show_in_table": True},
    "P_s_in": {"val": 35.0, "desc": "Inlet steam pressure [bar]", "show_in_table": True},
    "T_s_in": {"val": 300.0, "desc": "Inlet steam temp [C]", "show_in_table": True},
    "d_t": {"val": 2.44, "desc": "Diameter of the tank [m]", "show_in_table": True},
    "L_t": {"val": 4.0, "desc": "Length of the tank [m]", "show_in_table": True},
    "V_w_pct": {"val": 0.75, "desc": "Water volume percentage", "show_in_table": True},
    "mc_min": {"val": 0.0, "desc": "Min water valve flow rate [kg/s]", "show_in_table": False},
    "ms_min": {"val": 0.0, "desc": "Min steam valve flow rate [kg/s]", "show_in_table": False},
    "v_min_op": {"val": 20.0, "desc": "Min Normal Operation Valve Opening [%]", "show_in_table": True},
    "v_max_op": {"val": 80.0, "desc": "Max Normal Operation Valve Opening [%]", "show_in_table": True},
    "rate_limit_v": {"val": 50.0, "desc": "Max Valve Rate of Change [%/s]", "show_in_table": True},
    "tau_c": {"val": 1.0, "desc": "Water valve time constant [s]", "show_in_table": True},
    "tau_s": {"val": 1.0, "desc": "Steam valve time constant [s]", "show_in_table": True},
    "ramp_rate_max": {"val": 5.0, "desc": "Max ramp rate for demand [kg/s^2]", "show_in_table": True},
}

# Steady-State Compution
def initialize_deaerator_properties(params):
    steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
    
  
    m_w_in_nom = params["m_w_in_nom"]["val"]
    m_s_in_nom = params["m_s_in_nom"]["val"]
    T_w_in_C = params["T_w_in_C"]["val"]
    P_s_in = params["P_s_in"]["val"]
    T_s_in = params["T_s_in"]["val"]
    d_t = params["d_t"]["val"]
    L_t = params["L_t"]["val"]
    V_w_pct = params["V_w_pct"]["val"]
    

    m_w_out_nom = m_w_in_nom + m_s_in_nom
    

    h_s_in = steamTable.h_pt(P_s_in, T_s_in)
    
    # Bisection Method for SS
    a, b = 1.0, 10.0
    P0 = 5.0
    
    for _ in range(100):
        m = (a + b) / 2.0
        h_w_in1 = steamTable.h_pt(m, T_w_in_C)
        if np.isnan(h_w_in1): h_w_in1 = steamTable.hL_p(m)
        h_w_out1 = steamTable.hL_p(m)
        
        error = abs(m_s_in_nom * h_s_in + m_w_in_nom * h_w_in1 - m_w_out_nom * h_w_out1)
        if error < 0.001:
            P0 = m
            break
            
        h_w_in2 = steamTable.h_pt(a, T_w_in_C)
        if np.isnan(h_w_in2): h_w_in2 = steamTable.hL_p(a)
        h_w_out2 = steamTable.hL_p(a)
        
        f1 = m_s_in_nom * h_s_in + m_w_in_nom * h_w_in1 - m_w_out_nom * h_w_out1
        f2 = m_s_in_nom * h_s_in + m_w_in_nom * h_w_in2 - m_w_out_nom * h_w_out2
        
        if f1 * f2 < 0: b = m
        else: a = m
            
    # Calculate fixed properties at SS
    rho_w = steamTable.rhoL_p(P0)
    rho_s = steamTable.rhoV_p(P0)
    h_w_in = steamTable.h_pt(P0, T_w_in_C)
    if np.isnan(h_w_in): h_w_in = steamTable.hL_p(P0)
    h_w_out = steamTable.hL_p(P0)
    h_w_sat = h_w_out
    h_st_sat = steamTable.hV_p(P0)
    
    # Calculate initial mass from Geometry based on inputs
    V_tot = 0.25 * np.pi * (d_t**2) * L_t
    V_w = V_w_pct * V_tot
    V_s = (1 - V_w_pct) * V_tot
    
    m_w_init = V_w * rho_w
    m_s_init = V_s * rho_s

    #computing nominal level based on V_w_pct
    R = d_t / 2.0
    def calc_volume_error(L_val):
        L_val = float(L_val[0])
        if L_val <= 0 or L_val >= d_t: 
            return 1e6
        h = abs(R - L_val)
        theta = 2 * np.arccos(h / R)
        area_segment = 0.5 * R**2 * (theta - np.sin(theta))
        if L_val <= R:
            v_calc = area_segment * L_t
        else:
            v_calc = (np.pi * R**2 - area_segment) * L_t
        return v_calc - V_w

    res = opt.root(calc_volume_error, [d_t * V_w_pct])
    L_nom = res.x[0]
    
    # -----------------------------------------------------
    delta_L = 0.5  # Permissible level changes in meters
    delta_P = 0.1  # Permissible pressure changes in bar

    delta_L_trip = 0.8  # Level trip range
    delta_P_trip = 0.2  # pressure trip range

    # Updating SYSTEM_PARAMS 
    params.update({
        "mc_max": {"val": m_w_in_nom * 2.0, "desc": "Max water valve flow rate [kg/s]", "show_in_table": True},
        "ms_max": {"val": m_s_in_nom * 2.0, "desc": "Max steam valve flow rate [kg/s]", "show_in_table": True},
        "L_min_op": {"val": L_nom - delta_L, "desc": "Min Normal Operation Level [m]", "show_in_table": True},
        "L_max_op": {"val": L_nom + delta_L, "desc": "Max Normal Operation Level [m]", "show_in_table": True},
        "L_min_trip": {"val": L_nom - delta_L_trip, "desc": "Min Trip Level [m]", "show_in_table": True},
        "L_max_trip": {"val": L_nom + delta_L_trip, "desc": "Max Trip Level [m]", "show_in_table": True},
        "P_min_op": {"val": max(1.0, P0 - delta_P), "desc": "Min Normal Operation Pressure [bar]", "show_in_table": True},
        "P_max_op": {"val": P0 + delta_P, "desc": "Max Normal Operation Pressure [bar]", "show_in_table": True},
        "P_min_trip": {"val": max(0.5, P0 - delta_P_trip), "desc": "Min Trip Pressure [bar]", "show_in_table": True},
        "P_max_trip": {"val": P0 + delta_P_trip, "desc": "Max Trip Pressure [bar]", "show_in_table": True},
        "m_w_out_actual": {"val": m_w_out_nom, "desc": "Initial feedwater demand [kg/s]", "show_in_table": False},
        "rho_w": {"val": rho_w, "desc": "Water density [kg/m^3]", "show_in_table": False},
        "rho_st": {"val": rho_s, "desc": "Steam density [kg/m^3]", "show_in_table": False},
        "hw_out": {"val": h_w_out, "desc": "Outlet water enthalpy [kJ/kg]", "show_in_table": False},
        "hw_sat": {"val": h_w_sat, "desc": "Saturated water enthalpy [kJ/kg]", "show_in_table": False},
        "hst_sat": {"val": h_st_sat, "desc": "Saturated steam enthalpy [kJ/kg]", "show_in_table": False},
        "hw_in": {"val": h_w_in, "desc": "Inlet water enthalpy [kJ/kg]", "show_in_table": False},
        "hst_in": {"val": h_s_in, "desc": "Inlet steam enthalpy [kJ/kg]", "show_in_table": False},
        "L_set": {"val": L_nom, "desc": "Initial Level Setpoint [m]", "show_in_table": False},
        "P_set": {"val": P0, "desc": "Initial Pressure Setpoint [bar]", "show_in_table": False},
        "m_w_in": {"val": m_w_in_nom, "desc": "Initial inlet water flow [kg/s]", "show_in_table": True},
        "m_st_in": {"val": m_s_in_nom, "desc": "Initial inlet steam flow [kg/s]", "show_in_table": True},
        "m_w_init": {"val": m_w_init, "desc": "Initial water mass [kg]", "show_in_table": False},
        "m_s_init": {"val": m_s_init, "desc": "Initial steam mass [kg]", "show_in_table": False},
    })



# --- Load parameters from JSON if exists ---
CONFIG_FILE = "deaerator_config.json"
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            saved_params = json.load(f)
            for k, v in saved_params.items():
                if k in SYSTEM_PARAMS:
                    SYSTEM_PARAMS[k]["val"] = v
    except Exception as e:
        print("Error loading config:", e)

# Updating SYSTEM_PARAMS
initialize_deaerator_properties(SYSTEM_PARAMS)



class ParameterSetupWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Parameters Configuration")
        self.geometry("850x700")
        ctk.set_appearance_mode("dark")
        
        self.entries = {}
        
        title_label = ctk.CTkLabel(self, text="Configure Design Parameters", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=15)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=800, height=550)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(self.scroll_frame, text="Parameter", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.scroll_frame, text="Value", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.scroll_frame, text="Description", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        row = 1
        for key, data in SYSTEM_PARAMS.items():
            if data.get("show_in_table", False): 
                ctk.CTkLabel(self.scroll_frame, text=key).grid(row=row, column=0, padx=10, pady=5, sticky="w")
                
                entry = ctk.CTkEntry(self.scroll_frame, width=120)
                entry.insert(0, f"{data['val']:.3f}")
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                self.entries[key] = entry
                
                ctk.CTkLabel(self.scroll_frame, text=data["desc"], text_color="gray").grid(row=row, column=2, padx=10, pady=5, sticky="w")
                row += 1
            
        start_btn = ctk.CTkButton(self, text="Save & Start System", command=self.save_and_start, fg_color="green", hover_color="darkgreen")
        start_btn.pack(pady=15)
        
    def save_and_start(self):
        try:
            saved_dict = {}
            for key, entry in self.entries.items():
                new_val = float(entry.get())
                SYSTEM_PARAMS[key]["val"] = new_val

            initialize_deaerator_properties(SYSTEM_PARAMS) 
            # Uodating all of parameters in SYSTEM_PARAMS
            for key, data in SYSTEM_PARAMS.items():
                saved_dict[key] = data["val"]
            
            # Saving in a file
            with open(CONFIG_FILE, "w") as f:
                json.dump(saved_dict, f, indent=4)
            
            if SYSTEM_PARAMS["L_max_op"]["val"] > SYSTEM_PARAMS["d_t"]["val"]:
                SYSTEM_PARAMS["L_max_op"]["val"] = SYSTEM_PARAMS["d_t"]["val"] - 0.2

            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all parameters.")

class PIController:
    def __init__(self, Kp, Ki, out_min, out_max, nominal_out, rate_limit=5.0):
        self.Kp = Kp
        self.Ki = Ki
        self.out_min = out_min
        self.out_max = out_max
        self.nominal_out = nominal_out
        self.integral = 0.0
        self.rate_limit = rate_limit
        self.prev_output = nominal_out


    def compute(self, setpoint, pv, dt, ff=None):
        error = setpoint - pv
        self.integral += error * dt
        
        base_out = ff if ff is not None else self.nominal_out
        
        output_unclamped = base_out + (self.Kp * error) + (self.Ki * self.integral)
        output = np.clip(output_unclamped, self.out_min, self.out_max)
        
        max_change = self.rate_limit * dt
        if output > self.prev_output + max_change:
            output = self.prev_output + max_change
        elif output < self.prev_output - max_change:
            output = self.prev_output - max_change
            
        if output != output_unclamped:
            self.integral -= error * dt
            
        self.prev_output = output
        return output

class PowerPlantSCADA:
    def __init__(self, root, gains_L, gains_P):
        self.lcv_auto_mv = 50.0
        self.pcv_auto_mv = 50.0
        self.mc_max = SYSTEM_PARAMS["mc_max"]["val"]
        self.mc_min = SYSTEM_PARAMS["mc_min"]["val"]
        self.ms_max = SYSTEM_PARAMS["ms_max"]["val"]
        self.ms_min = SYSTEM_PARAMS["ms_min"]["val"]
        
        self.v_min_pct = SYSTEM_PARAMS["v_min_op"]["val"]
        self.v_max_pct = SYSTEM_PARAMS["v_max_op"]["val"]
        self.rate_limit_v = SYSTEM_PARAMS["rate_limit_v"]["val"]
        
        self.L_min_op = SYSTEM_PARAMS["L_min_op"]["val"]
        self.L_max_op = SYSTEM_PARAMS["L_max_op"]["val"]
        self.P_min_op = SYSTEM_PARAMS["P_min_op"]["val"]
        self.P_max_op = SYSTEM_PARAMS["P_max_op"]["val"]

        self.L_min_trip = SYSTEM_PARAMS["L_min_trip"]["val"]
        self.L_max_trip = SYSTEM_PARAMS["L_max_trip"]["val"]
        self.P_min_trip = SYSTEM_PARAMS["P_min_trip"]["val"]
        self.P_max_trip = SYSTEM_PARAMS["P_max_trip"]["val"]
        
        self.mc_limit_min = self.mc_max * (self.v_min_pct / 100.0)
        self.mc_limit_max = self.mc_max * (self.v_max_pct / 100.0)
        self.ms_limit_min = self.ms_max * (self.v_min_pct / 100.0)
        self.ms_limit_max = self.ms_max * (self.v_max_pct / 100.0)

        rate_limit_mc = self.mc_max * (self.rate_limit_v / 100.0)
        rate_limit_ms = self.ms_max * (self.rate_limit_v / 100.0)

        self.tau_c = SYSTEM_PARAMS["tau_c"]["val"]
        self.tau_s = SYSTEM_PARAMS["tau_s"]["val"]
        
        self.d_t = SYSTEM_PARAMS["d_t"]["val"]
        self.L_t = SYSTEM_PARAMS["L_t"]["val"]
        self.m_w_out_actual = SYSTEM_PARAMS["m_w_out_actual"]["val"]
        self.ramp_rate_max = SYSTEM_PARAMS["ramp_rate_max"]["val"]
        
        self.rho_w = SYSTEM_PARAMS["rho_w"]["val"]
        self.rho_st = SYSTEM_PARAMS["rho_st"]["val"]
        self.hw_out = SYSTEM_PARAMS["hw_out"]["val"]
        self.hw_sat = SYSTEM_PARAMS["hw_sat"]["val"]
        self.hst_sat = SYSTEM_PARAMS["hst_sat"]["val"]
        self.hw_in = SYSTEM_PARAMS["hw_in"]["val"]
        self.hst_in = SYSTEM_PARAMS["hst_in"]["val"]
        
        self.dt = 0.2
        self.time = 0.0
        
        self.steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
        
        self.L_set = np.clip(SYSTEM_PARAMS["L_set"]["val"], self.L_min_op, self.L_max_op)
        self.P_set = np.clip(SYSTEM_PARAMS["P_set"]["val"], self.P_min_op, self.P_max_op)
        
        self.L = self.L_set
        self.P = self.P_set
        
        # محاسبه دقیق V_w از روی L_set
        R = self.d_t / 2.0
        theta = 2 * np.arccos((R - self.L) / R)
        V_w = 0.5 * R**2 * (theta - np.sin(theta)) * self.L_t
        V_tot = np.pi * R**2 * self.L_t
        V_s = V_tot - V_w
        
        rho_w_curr = self.steamTable.rhoL_p(self.P)
        rho_s_curr = self.steamTable.rhoV_p(self.P)
        
        self.m_w = V_w * rho_w_curr
        self.m_s = V_s * rho_s_curr
        
        self.m_w_in = np.clip(SYSTEM_PARAMS["m_w_in"]["val"], self.mc_limit_min, self.mc_limit_max)
        self.m_st_in = np.clip(SYSTEM_PARAMS["m_st_in"]["val"], self.ms_limit_min, self.ms_limit_max)
        
        self.LC = PIController(gains_L[0], gains_L[1], self.mc_limit_min, self.mc_limit_max, self.m_w_in, rate_limit=rate_limit_mc)  
        self.PC = PIController(gains_P[0], gains_P[1], self.ms_limit_min, self.ms_limit_max, self.m_st_in, rate_limit=rate_limit_ms)   

        

        self.root = root
        self.root.title("Power Plant SCADA - Deaerator Digital Twin - Designed by 1043")

        self.root.geometry("1400x950")
        
        ctk.set_appearance_mode("dark")
        
        self.bg_color = "#0f111a"
        self.panel_color = "#181b28"
        self.accent_blue = "#00e5ff"   
        self.accent_red = "#ff1744"    
        self.accent_green = "#00e676"  
        self.accent_purple = "#d500f9"
        self.text_color = "#a6accd"
        self.warning_color = "#ffea00"
        
        # --- در انتهای متد __init__ کلاس PowerPlantSCADA ---
        self.P_tank_init = self.P_set + (rho_w_curr * 9.81 * self.L_set / 10**5)
        
        self.window_size = 400
        self.t_data = [(i - self.window_size) * self.dt for i in range(self.window_size)]
        self.L_data = [self.L_set] * self.window_size
        self.P_data = [self.P_set] * self.window_size # اصلاح به P_tank
        self.lcv_data = [(self.m_w_in/self.mc_max)*100 if self.mc_max!=0 else 0] * self.window_size
        self.pcv_data = [(self.m_st_in/self.ms_max)*100 if self.ms_max!=0 else 0] * self.window_size
        
        self.particles = []
        self.alarm_blink = False
        self.plots_visible = False

        self.lcv_mode = "Auto"
        self.pcv_mode = "Auto"
        self.lcv_manual_pct = 50.0  # مقدار پیش‌فرض
        self.pcv_manual_pct = 50.0  # مقدار پیش‌فرض

        self.setup_ui()
        self.update_simulation()
        # --- Serial Communication Setup ---
        self.serial_port = 'COM4' # پورت مربوط به STM32 را اینجا وارد کنید
        self.baud_rate = 115200
        self.serial_running = True
        
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
            self.serial_thread.start()
            print(f"Connected to {self.serial_port}")
        except Exception as e:
            print(f"Warning: Could not connect to serial port. Running without hardware. Error: {e}")

    def toggle_lcv_mode(self):
        if self.lcv_mode == "Auto":
            self.lcv_mode = "Manual"
            self.lcv_am_btn.configure(text="MAN", fg_color=self.warning_color, text_color="black")
            self.lcv_slider.configure(state="normal")
            # سینک کردن اسلایدر با مقدار فعلی
            current_pct = (self.m_w_in / self.mc_max) * 100 if self.mc_max != 0 else 0
            self.lcv_manual_pct = np.clip(current_pct, 0, 100)
            self.lcv_slider.set(self.lcv_manual_pct)
        else:
            self.lcv_mode = "Auto"
            self.lcv_am_btn.configure(text="AUTO", fg_color=self.accent_green, text_color="white")
            self.lcv_slider.configure(state="disabled")
            # ریست کردن انتگرال‌گیر کنترل‌کننده برای جلوگیری از پرش (Bumpless Transfer)
            self.LC.integral = 0 
            self.LC.prev_output = self.m_w_in

    def toggle_pcv_mode(self):
        if self.pcv_mode == "Auto":
            self.pcv_mode = "Manual"
            self.pcv_am_btn.configure(text="MAN", fg_color=self.warning_color, text_color="black")
            self.pcv_slider.configure(state="normal")
            current_pct = (self.m_st_in / self.ms_max) * 100 if self.ms_max != 0 else 0
            self.pcv_manual_pct = np.clip(current_pct, 0, 100)
            self.pcv_slider.set(self.pcv_manual_pct)
        else:
            self.pcv_mode = "Auto"
            self.pcv_am_btn.configure(text="AUTO", fg_color=self.accent_green, text_color="white")
            self.pcv_slider.configure(state="disabled")
            self.PC.integral = 0
            self.PC.prev_output = self.m_st_in
    

 

    def send_and_receive_hil(self, command):
        """ Sends a command to the STM32 and waits for a response. """
        if hasattr(self, 'ser') and self.ser.is_open:
            try:
                self.ser.write(command.encode('utf-8'))
                # منتظر پاسخ می‌مانیم. timeout مهم است.
                response = self.ser.readline().decode('utf-8').strip()
                if response:
                    # مثلا پاسخ 'L:58' را پارس می‌کنیم
                    parts = response.split(':')
                    if len(parts) == 2:
                        return float(parts[1])
            except Exception as e:
                print(f"HIL Communication Error: {e}")
                return None
        return None

    # ... در کلاس PowerPlantSCADA در __init__ اضافه کنید
# ... در کلاس PowerPlantSCADA در __init__ اضافه کنید


# ...
    def read_serial_data(self):
        while self.serial_running:
            if hasattr(self, 'ser') and self.ser.is_open:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        prefix, val_str = line.split(':')
                        pct_val = float(val_str)
                        
                        # بررسی کنید شیر مربوطه در چه حالتی است
                        if prefix == 'L':
                            if self.lcv_mode == "Manual":
                                # در حالت دستی، مقدار پتانسیومتر اسلایدر را آپدیت می‌کند
                                self.lcv_manual_pct = np.clip(pct_val, 0, 100)
                            else: # Auto
                                # در حالت خودکار، مقدار محاسبه شده توسط STM32 را ذخیره می‌کنیم
                                self.lcv_auto_mv = np.clip(pct_val, 0, 100)
                                
                        elif prefix == 'P':
                            if self.pcv_mode == "Manual":
                                self.pcv_manual_pct = np.clip(pct_val, 0, 100)
                            else: # Auto
                                self.pcv_auto_mv = np.clip(pct_val, 0, 100)

                except Exception as e:
                    # این خطا ممکن است در زمان بستن برنامه رخ دهد، اشکالی ندارد
                    pass


    def update_lcv_manual(self, value):
        if self.lcv_mode == "Manual":
            self.lcv_manual_pct = value

    def update_pcv_manual(self, value):
        if self.pcv_mode == "Manual":
            self.pcv_manual_pct = value

        
    def setup_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=3)
        self.root.grid_rowconfigure(1, weight=2)

        self.sidebar_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color=self.panel_color, border_width=1, border_color="#2b2f42", width=350)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        
       
        ctk.CTkLabel(self.sidebar_frame, text="SCADA CONTROL", font=ctk.CTkFont(family="Courier", size=22, weight="bold"), text_color=self.warning_color).pack(pady=(10, 5), padx=20)
        
        
        self.status_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#12141f", corner_radius=10)
        self.status_frame.pack(pady=5, padx=15, fill="x")
        
        self.led_canvas = tk.Canvas(self.status_frame, width=30, height=30, bg="#12141f", highlightthickness=0)
        self.led_canvas.pack(pady=(5, 5))
        self.status_led = self.led_canvas.create_oval(5, 5, 25, 25, fill=self.accent_green, outline="#000")
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="SYSTEM NORMAL", font=ctk.CTkFont(family="Courier", size=14, weight="bold"), text_color=self.accent_green)
        self.status_label.pack(pady=(0, 5))
       
        setpoint_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#12141f", corner_radius=10)
        setpoint_frame.pack(pady=5, padx=15, fill="x")
        
        ctk.CTkLabel(setpoint_frame, text="Level Setpoint ($L$)", font=ctk.CTkFont(size=12), text_color=self.text_color).pack(pady=(10, 0))
        self.l_set_label = ctk.CTkLabel(setpoint_frame, text=f"{self.L_set:.2f} m", font=ctk.CTkFont(family="Courier", size=16, weight="bold"), text_color=self.accent_blue)
        self.l_set_label.pack()
        delta_L = min(self.L_set - self.L_min_op, self.L_max_op - self.L_set)
        # حذف خط محاسبه delta_L و تغییر from_ و to 
        self.l_slider = ctk.CTkSlider(setpoint_frame, from_=self.L_min_op, to=self.L_max_op, command=self.update_L_setpoint, button_color=self.accent_blue, progress_color=self.accent_blue)
        self.l_slider.set(self.L_set)
        self.l_slider.pack(pady=(0, 10), padx=20)


        ctk.CTkLabel(setpoint_frame, text="Pressure Setpoint ($P$)", font=ctk.CTkFont(size=12), text_color=self.text_color).pack(pady=(5, 0))
        self.p_set_label = ctk.CTkLabel(setpoint_frame, text=f"{self.P_set:.2f} bar", font=ctk.CTkFont(family="Courier", size=16, weight="bold"), text_color=self.accent_red)
        self.p_set_label.pack()
        delta_P = min(self.P_set - self.P_min_op, self.P_max_op - self.P_set)
        # حذف خط محاسبه delta_P و تغییر from_ و to
        self.p_slider = ctk.CTkSlider(setpoint_frame, from_=self.P_min_op, to=self.P_max_op, command=self.update_P_setpoint, button_color=self.accent_red, progress_color=self.accent_red)
        self.p_slider.set(self.P_set)
        self.p_slider.pack(pady=(0, 10), padx=20)


        dist_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#12141f", corner_radius=10)
        dist_frame.pack(pady=5, padx=15, fill="x")
        ctk.CTkLabel(dist_frame, text="DISTURBANCES", font=ctk.CTkFont(family="Courier", size=14, weight="bold"), text_color=self.accent_purple).pack(pady=(10, 5))

        ctk.CTkLabel(dist_frame, text="Feedwater Demand ($m_{w,out}$)", font=ctk.CTkFont(size=12), text_color=self.text_color).pack()
        self.mf_val_label = ctk.CTkLabel(dist_frame, text=f"{self.m_w_out_actual:.1f} kg/s", font=ctk.CTkFont(family="Courier", size=14, weight="bold"), text_color=self.accent_green)
        self.mf_val_label.pack()
        mf_nom = self.m_w_out_actual
        delta_mf = mf_nom * 0.5
        self.mf_slider = ctk.CTkSlider(dist_frame, from_=mf_nom - delta_mf, to=mf_nom + delta_mf, command=self.slider_event, button_color=self.accent_green, progress_color=self.accent_green)
        self.mf_slider.set(mf_nom)
        self.mf_slider.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(dist_frame, text="Inlet Water Enthalpy ($h_{w,in}$)", font=ctk.CTkFont(size=12), text_color=self.text_color).pack()
        self.hw_val_label = ctk.CTkLabel(dist_frame, text=f"{self.hw_in:.1f} kJ/kg", font=ctk.CTkFont(family="Courier", size=14, weight="bold"), text_color=self.accent_blue)
        self.hw_val_label.pack()
        hw_nom = self.hw_in
        delta_hw = hw_nom * 0.02
        self.hw_slider = ctk.CTkSlider(dist_frame, from_=hw_nom - delta_hw, to=hw_nom + delta_hw, command=self.update_hw_dist, button_color=self.accent_blue, progress_color=self.accent_blue)
        self.hw_slider.set(hw_nom)
        self.hw_slider.pack(pady=(0, 10), padx=20)

        ctk.CTkLabel(dist_frame, text="Inlet Steam Enthalpy ($h_{st,in}$)", font=ctk.CTkFont(size=12), text_color=self.text_color).pack()
        self.hst_val_label = ctk.CTkLabel(dist_frame, text=f"{self.hst_in:.1f} kJ/kg", font=ctk.CTkFont(family="Courier", size=14, weight="bold"), text_color=self.accent_red)
        self.hst_val_label.pack()
        hst_nom = self.hst_in
        delta_hst = hst_nom * 0.2
        self.hst_slider = ctk.CTkSlider(dist_frame, from_=hst_nom - delta_hst, to=hst_nom + delta_hst, command=self.update_hst_dist, button_color=self.accent_red, progress_color=self.accent_red)
        self.hst_slider.set(hst_nom)
        self.hst_slider.pack(pady=(0, 10), padx=20)

        # --- Valve Control Frame ---
        valve_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="#12141f", corner_radius=10)
        valve_frame.pack(pady=2.5, padx=7.5, fill="x")
        ctk.CTkLabel(valve_frame, text="VALVE CONTROLS", font=ctk.CTkFont(family="Courier", size=14, weight="bold"), text_color="#ffb300").pack(pady=(5, 2.5))

        # LCV Control
        lcv_ctrl_frame = ctk.CTkFrame(valve_frame, fg_color="transparent")
        lcv_ctrl_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(lcv_ctrl_frame, text="Water Valve (LCV)", font=ctk.CTkFont(size=12)).pack(anchor="w")
        
        self.lcv_am_btn = ctk.CTkButton(lcv_ctrl_frame, text="AUTO", width=60, command=self.toggle_lcv_mode, fg_color=self.accent_green)
        self.lcv_am_btn.pack(side="left", padx=(0, 10))
        
        self.lcv_slider = ctk.CTkSlider(lcv_ctrl_frame, from_=0, to=100, command=self.update_lcv_manual, state="disabled")
        self.lcv_slider.set(self.lcv_manual_pct)
        self.lcv_slider.pack(side="left", fill="x", expand=True)

        # PCV Control
        pcv_ctrl_frame = ctk.CTkFrame(valve_frame, fg_color="transparent")
        pcv_ctrl_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(pcv_ctrl_frame, text="Steam Valve (PCV)", font=ctk.CTkFont(size=12)).pack(anchor="w")
        
        self.pcv_am_btn = ctk.CTkButton(pcv_ctrl_frame, text="AUTO", width=60, command=self.toggle_pcv_mode, fg_color=self.accent_green)
        self.pcv_am_btn.pack(side="left", padx=(0, 10))
        
        self.pcv_slider = ctk.CTkSlider(pcv_ctrl_frame, from_=0, to=100 , command=self.update_pcv_manual, state="disabled")
        self.pcv_slider.set(self.pcv_manual_pct)
        self.pcv_slider.pack(side="left", fill="x", expand=True)



        
        ctk.CTkLabel(self.sidebar_frame, text="Click on Tank to Toggle Plots", font=ctk.CTkFont(size=12, slant="italic"), text_color=self.text_color).pack(pady=5)
        
        self.schematic_frame = ctk.CTkFrame(self.root, fg_color=self.panel_color, corner_radius=15, border_width=1, border_color="#2b2f42")
        self.schematic_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 5), sticky="nsew")
        
        self.canvas = tk.Canvas(self.schematic_frame, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.draw_schematic()

        self.plot_frame = ctk.CTkFrame(self.root, fg_color=self.panel_color, corner_radius=15, border_width=1, border_color="#2b2f42")
        self.setup_plots()

    def setup_plots(self):
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(10, 3), dpi=100)
        self.fig.patch.set_facecolor(self.panel_color)
        
        self.axs = [self.fig.add_subplot(141), self.fig.add_subplot(142), self.fig.add_subplot(143), self.fig.add_subplot(144)]
        
        for ax in self.axs:
            ax.set_facecolor(self.bg_color)
            ax.grid(color='#2b2f42', linestyle='-', linewidth=1)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#4a4d70')
            ax.spines['left'].set_color('#4a4d70')
            ax.tick_params(colors=self.text_color)
            
        self.fig.tight_layout(pad=2.0)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.line_L, = self.axs[0].plot([], [], color=self.accent_blue, linewidth=2)
        self.axs[0].set_title('Level ($L$) [m]', color='white', fontname='Courier New', fontweight='bold', fontsize=10)
        self.hline_L = self.axs[0].axhline(y=self.L_set, color=self.accent_green, linestyle='-', alpha=0.5)
        self.axs[0].axhline(y=self.L_min_op, color=self.warning_color, linestyle='--', alpha=0.8)
        self.axs[0].axhline(y=self.L_max_op, color=self.warning_color, linestyle='--', alpha=0.8)
        self.axs[0].axhline(y=self.L_min_trip, color=self.accent_red, linestyle='-.', alpha=0.9)
        self.axs[0].axhline(y=self.L_max_trip, color=self.accent_red, linestyle='-.', alpha=0.9)

        self.line_P, = self.axs[1].plot([], [], color=self.accent_red, linewidth=2)
        self.axs[1].set_title('Pressure  [bar]', color='white', fontname='Courier New', fontweight='bold', fontsize=10)
        self.hline_P = self.axs[1].axhline(y=self.P_set, color=self.accent_green, linestyle='-', alpha=0.5)
        self.axs[1].axhline(y=self.P_min_op, color=self.warning_color, linestyle='--', alpha=0.8)
        self.axs[1].axhline(y=self.P_max_op, color=self.warning_color, linestyle='--', alpha=0.8)
        self.axs[1].axhline(y=self.P_min_trip, color=self.accent_red, linestyle='-.', alpha=0.9)
        self.axs[1].axhline(y=self.P_max_trip, color=self.accent_red, linestyle='-.', alpha=0.9)

        self.line_lcv, = self.axs[2].plot([], [], color=self.accent_blue, linewidth=2)
        self.axs[2].set_title('LCV Opening [%]', color='white', fontname='Courier New', fontweight='bold', fontsize=10)
        self.axs[2].set_ylim(0, 100)
        self.axs[2].axhline(y=self.v_min_pct, color=self.warning_color, linestyle='--', alpha=0.8)
        self.axs[2].axhline(y=self.v_max_pct, color=self.warning_color, linestyle='--', alpha=0.8)

        self.line_pcv, = self.axs[3].plot([], [], color=self.accent_red, linewidth=2)
        self.axs[3].set_title('PCV Opening [%]', color='white', fontname='Courier New', fontweight='bold', fontsize=10)
        self.axs[3].set_ylim(0, 100)
        self.axs[3].axhline(y=self.v_min_pct, color=self.warning_color, linestyle='--', alpha=0.8)
        self.axs[3].axhline(y=self.v_max_pct, color=self.warning_color, linestyle='--', alpha=0.8)

    def update_L_setpoint(self, value):
        self.L_set = value
        self.l_set_label.configure(text=f"{value:.2f} m")
        self.hline_L.set_ydata([value, value])

    def update_P_setpoint(self, value):
        self.P_set = value
        self.p_set_label.configure(text=f"{value:.2f} bar")
        self.hline_P.set_ydata([value, value])

    def slider_event(self, value):
        self.mf_val_label.configure(text=f"{value:.1f} kg/s")
        
    def update_hw_dist(self, value):
        self.hw_in = value
        self.hw_val_label.configure(text=f"{value:.1f} kJ/kg")
        
    def update_hst_dist(self, value):
        self.hst_in = value
        self.hst_val_label.configure(text=f"{value:.1f} kJ/kg")

    def draw_valve(self, x, y, color, tag, vertical=False):
        c = self.canvas
        if vertical:
            c.create_rectangle(x-12, y-22, x+12, y-18, fill="#4a4d70", outline="", tags=tag)
            c.create_rectangle(x-12, y+18, x+12, y+22, fill="#4a4d70", outline="", tags=tag)
            c.create_polygon(x-15, y-20, x+15, y-20, x-15, y+20, x+15, y+20, fill="#181b28", outline=color, width=2, tags=tag)
            c.create_line(x+5, y, x+25, y, fill=color, width=3, tags=tag)
            c.create_polygon(x+25, y-15, x+25, y+15, x+35, y+20, x+35, y-20, fill=color, outline="#fff", tags=tag)
        else:
            c.create_rectangle(x-22, y-12, x-18, y+12, fill="#4a4d70", outline="", tags=tag)
            c.create_rectangle(x+18, y-12, x+22, y+12, fill="#4a4d70", outline="", tags=tag)
            c.create_polygon(x-20, y-15, x-20, y+15, x+20, y-15, x+20, y+15, fill="#181b28", outline=color, width=2, tags=tag)
            c.create_line(x, y-5, x, y-25, fill=color, width=3, tags=tag)
            c.create_polygon(x-15, y-25, x+15, y-25, x+20, y-35, x-20, y-35, fill=color, outline="#fff", tags=tag)

    def draw_pump(self, x, y, color):
        c = self.canvas
        c.create_rectangle(x+20, y-15, x+50, y+15, fill="#2b2f42", outline=color, width=2)
        c.create_oval(x-25, y-25, x+25, y+25, fill="#181b28", outline=color, width=3)
        c.create_polygon(x+5, y-25, x+5, y-10, x-15, y-5, x-25, y-25, fill=color, outline="")

    def draw_schematic(self):
        c = self.canvas
        for i in range(0, 1050, 40):
            c.create_line(i, 0, i, 800, fill="#1c1f2e", dash=(2, 4))
            c.create_line(0, i, 1050, i, fill="#1c1f2e", dash=(2, 4))

        pipe_w = 12
        c.create_line(950, 120, 550, 120, fill="#2b2f42", width=pipe_w+4, capstyle=tk.ROUND)
        c.create_line(250, 40, 250, 320, fill="#2b2f42", width=pipe_w+4, capstyle=tk.ROUND)
        c.create_line(250, 320, 350, 320, fill="#2b2f42", width=pipe_w+4, capstyle=tk.ROUND)
        c.create_line(500, 380, 500, 430, fill="#2b2f42", width=pipe_w+4, capstyle=tk.ROUND)
        c.create_line(500, 430, 50, 430, fill="#2b2f42", width=pipe_w+4, capstyle=tk.ROUND)

        c.create_line(950, 120, 550, 120, fill="#181b28", width=pipe_w)
        c.create_line(250, 40, 250, 320, fill="#181b28", width=pipe_w)
        c.create_line(250, 320, 350, 320, fill="#181b28", width=pipe_w)
        c.create_line(500, 380, 500, 430, fill="#181b28", width=pipe_w)
        c.create_line(500, 430, 50, 430, fill="#181b28", width=pipe_w)

        self.tank_x1, self.tank_y1 = 350, 160
        self.tank_x2, self.tank_y2 = 650, 380
        
        dome_x1, dome_y1 = 430, 80
        dome_x2, dome_y2 = 570, 160
        c.create_rectangle(dome_x1-3, dome_y1-3, dome_x2+3, dome_y2+3, fill="", outline="#2b2f42", width=6, tags="clickable")
        c.create_rectangle(dome_x1, dome_y1, dome_x2, dome_y2, fill="#12141f", outline="#4a4d70", width=3, tags="clickable")

        c.create_oval(self.tank_x1-20, self.tank_y1-5, self.tank_x1+20, self.tank_y2+5, fill="", outline="#2b2f42", width=10, tags="clickable")
        c.create_oval(self.tank_x2-20, self.tank_y1-5, self.tank_x2+20, self.tank_y2+5, fill="", outline="#2b2f42", width=10, tags="clickable")
        c.create_rectangle(self.tank_x1, self.tank_y1-5, self.tank_x2, self.tank_y2+5, fill="", outline="#2b2f42", width=10, tags="clickable")
        
        c.create_oval(self.tank_x1-15, self.tank_y1, self.tank_x1+15, self.tank_y2, fill="#12141f", outline="#4a4d70", width=3, tags="clickable")
        c.create_oval(self.tank_x2-15, self.tank_y1, self.tank_x2+15, self.tank_y2, fill="#12141f", outline="#4a4d70", width=3, tags="clickable")
        c.create_rectangle(self.tank_x1, self.tank_y1, self.tank_x2, self.tank_y2, fill="#12141f", outline="#4a4d70", width=3, tags="clickable")
        
        self.water_rect = c.create_rectangle(self.tank_x1, 250, self.tank_x2, self.tank_y2-3, fill="#003f5c", outline="", tags="clickable")
        
        self.draw_valve(800, 120, self.accent_blue, "lcv")          
        self.draw_valve(300, 320, self.accent_red, "pcv")           
        self.draw_pump(150, 430, self.accent_green)                 

        c.create_text(500, 30, text="DEAERATOR TOWER & STORAGE\n(Click Tank to Toggle Plots)", fill="#ffffff", font=('Courier', 16, 'bold'), justify=tk.CENTER)
        
        def draw_box(x, y, color):
            c.create_rectangle(x-70, y-15, x+70, y+15, fill="#181b28", outline=color, width=1)
            
        draw_box(800, 150, self.accent_blue)
        self.txt_mc = c.create_text(800, 150, text="000.0 kg/s", fill=self.accent_blue, font=('Courier', 12, 'bold'))
        
        draw_box(300, 350, self.accent_red)
        self.txt_ms = c.create_text(300, 350, text="000.0 kg/s", fill=self.accent_red, font=('Courier', 12, 'bold'))
        
        draw_box(300, 460, self.accent_green)
        self.txt_mf = c.create_text(300, 460, text="000.0 kg/s", fill=self.accent_green, font=('Courier', 12, 'bold'))
        
        c.create_rectangle(750, 300, 980, 420, fill="#181b28", outline="#4a4d70", width=2, tags="clickable")
        c.create_text(865, 320, text="VESSEL STATES", fill=self.text_color, font=('Courier', 10), tags="clickable")
        self.txt_L = c.create_text(865, 355, text=f"{self.L_set:.2f} m", fill="#ffffff", font=('Courier', 22, 'bold'), tags="clickable")
        self.txt_P = c.create_text(865, 395, text=f"{self.P_set:.2f} bar", fill="#ffffff", font=('Courier', 22, 'bold'), tags="clickable")

        self.canvas.tag_bind("clickable", "<Button-1>", self.toggle_plots)

    def toggle_plots(self, event=None):
        if not self.plots_visible:
            self.plot_frame.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="nsew")
            self.plots_visible = True
        else:
            self.plot_frame.grid_forget()
            self.plots_visible = False

    def create_particle(self, start_pos, path, color):
        p = self.canvas.create_oval(-4, -4, 4, 4, fill=color, outline="")
        self.particles.append({"id": p, "path": path, "progress": 0.0, "color": color})

    def animate_flow(self):
        if self.mc_max > 0 and np.random.rand() < (self.m_w_in / self.mc_max) * 0.5:
            self.create_particle((950, 120), [950, 120, 550, 120], self.accent_blue)
        if self.ms_max > 0 and np.random.rand() < (self.m_st_in / self.ms_max) * 0.5:
            self.create_particle((250, 40), [250, 40, 250, 320, 350, 320], self.accent_red)
        if np.random.rand() < (self.m_w_out_actual / 80.0) * 0.5:
            self.create_particle((500, 380), [500, 380, 500, 430, 50, 430], self.accent_green)
            
        speed = 10
        alive_particles = []
        for p in self.particles:
            p['progress'] += speed
            path = p['path']
            
            current_dist = 0
            x, y = path[0], path[1]
            for i in range(0, len(path)-2, 2):
                seg_len = abs(path[i+2] - path[i]) + abs(path[i+3] - path[i+1])
                if p['progress'] <= current_dist + seg_len:
                    ratio = (p['progress'] - current_dist) / seg_len
                    x = path[i] + (path[i+2] - path[i]) * ratio
                    y = path[i+1] + (path[i+3] - path[i+1]) * ratio
                    break
                current_dist += seg_len
            
            if p['progress'] < sum([abs(path[i+2]-path[i]) + abs(path[i+3]-path[i+1]) for i in range(0, len(path)-2, 2)]):
                self.canvas.coords(p['id'], x-3, y-3, x+3, y+3)
                alive_particles.append(p)
            else:
                self.canvas.delete(p['id'])
                
        self.particles = alive_particles

    def update_simulation(self):
        g = 9.81
        l_mode = 1 if self.lcv_mode == "Auto" else 0
        p_mode = 1 if self.pcv_mode == "Auto" else 0

        if hasattr(self, 'ser') and self.ser.is_open:
            hil_command = f"B,{l_mode},{self.L_set:.4f},{self.L:.4f},{p_mode},{self.P_set:.4f},{self.P:.4f}\n"
            self.ser.write(hil_command.encode('utf-8'))
        for _ in range(5):
            m_w_out_target = self.mf_slider.get() 
            
            diff = m_w_out_target - self.m_w_out_actual
            max_step = self.ramp_rate_max * self.dt
            if abs(diff) > max_step:
                self.m_w_out_actual += np.sign(diff) * max_step
            else:
                self.m_w_out_actual = m_w_out_target
                
            m_w_out = self.m_w_out_actual
            
            # --- بخش مربوط به محاسبه فرمان شیر آب (LCV) ---
            # --- بخش مربوط به محاسبه فرمان شیر آب (LCV) ---
            if self.lcv_mode == "Auto":
                m_w_in_cmd = self.mc_max * (self.lcv_auto_mv / 100.0)
            else:
                m_w_in_cmd = self.mc_max * (self.lcv_manual_pct / 100.0)

            # --- بخش مربوط به محاسبه فرمان شیر بخار (PCV) ---
            # --- بخش مربوط به محاسبه فرمان شیر بخار (PCV) ---
            if self.pcv_mode == "Auto":
                m_st_in_cmd = self.ms_max * (self.pcv_auto_mv / 100.0)
            else:
                m_st_in_cmd = self.ms_max * (self.pcv_manual_pct / 100.0)


            # ==============================================================
            # ارسال مقادیر به STM32 (فقط یک بار برای هر دو کنترل‌کننده)
            # ==============================================================

 
            max_valve_speed_c = (self.mc_limit_max - self.mc_limit_min) * (self.rate_limit_v / 100.0) * self.dt  
            max_valve_speed_s = (self.ms_limit_max - self.ms_limit_min) * (self.rate_limit_v / 100.0) * self.dt
            
            dm_w = (m_w_in_cmd - self.m_w_in) / self.tau_c * self.dt
            dm_st = (m_st_in_cmd - self.m_st_in) / self.tau_s * self.dt
            
            self.m_w_in += np.clip(dm_w, -max_valve_speed_c, max_valve_speed_c)
            self.m_st_in += np.clip(dm_st, -max_valve_speed_s, max_valve_speed_s)

            u_s = self.steamTable.uV_p(self.P)
            u_w = self.steamTable.uL_p(self.P)
            nu_s = self.steamTable.vV_p(self.P)
            nu_w = self.steamTable.vL_p(self.P)
            h_w_out_curr = self.steamTable.hL_p(self.P)
            rho_w_curr = self.steamTable.rhoL_p(self.P)

            dP_epsilon = 0.001
            vV_plus = self.steamTable.vV_p(self.P + dP_epsilon)
            vV_minus = self.steamTable.vV_p(self.P - dP_epsilon)
            vL_plus = self.steamTable.vL_p(self.P + dP_epsilon)
            vL_minus = self.steamTable.vL_p(self.P - dP_epsilon)
            
            dnu_s_dp = ((vV_plus - vV_minus) / (2 * dP_epsilon)) / 100 
            dnu_w_dp = ((vL_plus - vL_minus) / (2 * dP_epsilon)) / 100 

            a11, b11, c11 = 538, 0.2149, -120.6
            a22, b22, c22, d22 = 2420, 0.6137, 2.364, 2650
            
            du_w_dp = (a11 * b11 * (self.P)**(b11 - 1)) / 100
            du_s_dp = (-(a22 - d22) * (b22/c22) * ((self.P)/c22)**(b22 - 1) / (1 + ((self.P)/c22)**b22)**2) / 100

            a1, a2 = u_s, u_w
            b1, b2 = nu_s, nu_w
            
            a3 = (self.m_s * du_s_dp + self.m_w * du_w_dp)
            b3 = (self.m_s * dnu_s_dp + self.m_w * dnu_w_dp)

            d1 = self.m_st_in * self.hst_in + self.m_w_in * self.hw_in - m_w_out * h_w_out_curr
            d2 = self.m_st_in + self.m_w_in - m_w_out

            term_denom = (b2 - b1 + (b3*a1)/a3 - (b3*a2)/a1)
            dm_w_dt = (-b1*d2 - (b3*d1)/a3 + (b3*a1*d2)/a3) / term_denom if term_denom != 0 else 0
            dm_s_dt = d2 - dm_w_dt
            dp_dt = (1/a3) * (d1 - a1*dm_s_dt - a2*dm_w_dt) if a3 != 0 else 0

            self.m_w += dm_w_dt * self.dt
            self.m_s += dm_s_dt * self.dt
            self.P += dp_dt * self.dt

            V_tot = 0.25 * np.pi * (self.d_t**2) * self.L_t
            V_w_curr = self.m_w / rho_w_curr
            
            drho_w_dp = - (rho_w_curr**2) * dnu_w_dp
            dV_wdt = (1/rho_w_curr)*(dm_w_dt - V_w_curr*drho_w_dp*dp_dt)
            
            def fun1(theta):
                return V_w_curr - 0.25 * (self.d_t**2) * self.L_t * (theta[0] - np.sin(theta[0])*np.cos(theta[0]))
            def fun2(theta):
                return V_w_curr - (0.25*np.pi*(self.d_t**2)*self.L_t - 0.25*(self.d_t**2)*self.L_t*(theta[0] - np.sin(theta[0])*np.cos(theta[0])))

            try:
                from scipy.optimize import least_squares
                if V_w_curr <= V_tot / 2:
                    res = least_squares(fun1, [np.pi/2], bounds=(0, np.pi))
                    sol1 = res.x[0]
                    self.L = (self.d_t / 2) * (1 - np.cos(sol1))
                    dtheta_dt = dV_wdt / (0.25*(self.d_t**2) * self.L_t *(1 + np.sin(sol1)**2 - np.cos(sol1)**2))
                    self.dL_dt = 0.5 * self.d_t * np.sin(sol1) * dtheta_dt
                else:
                    res = least_squares(fun2, [np.pi/2], bounds=(0, np.pi))
                    sol1 = res.x[0]
                    self.L = (self.d_t / 2) * (1 + np.cos(sol1))
                    dtheta_dt = dV_wdt / (-0.25*(self.d_t**2) * self.L_t *(1 + np.sin(sol1)**2 - np.cos(sol1)**2))
                    self.dL_dt = -0.5 * self.d_t * np.sin(sol1) * dtheta_dt
            except:
                pass 

            self.P_tank = self.P + (rho_w_curr * g * self.L / 10**5)

            self.time += self.dt
            
            self.t_data.append(self.time)
            self.L_data.append(self.L) 
            self.P_data.append(self.P)
            self.lcv_data.append((self.m_w_in / self.mc_max) * 100 if self.mc_max!=0 else 0)
            self.pcv_data.append((self.m_st_in / self.ms_max) * 100 if self.ms_max!=0 else 0)
            
            self.t_data.pop(0)
            self.L_data.pop(0)
            self.P_data.pop(0)
            self.lcv_data.pop(0)
            self.pcv_data.pop(0)

        self.update_gui_visuals()
        self.animate_flow()
        self.root.after(100, self.update_simulation)

    def update_gui_visuals(self):
        if self.lcv_mode == "Manual":
            self.lcv_slider.set(self.lcv_manual_pct)
        if self.pcv_mode == "Manual":
            self.pcv_slider.set(self.pcv_manual_pct)   
        m_f = self.m_w_out_actual
        
        self.canvas.itemconfig(self.txt_mc, text=f"{self.m_w_in:05.1f} kg/s")
        self.canvas.itemconfig(self.txt_ms, text=f"{self.m_st_in:05.1f} kg/s")
        self.canvas.itemconfig(self.txt_mf, text=f"{m_f:05.1f} kg/s")
        self.canvas.itemconfig(self.txt_L, text=f"{self.L:.2f} m")
        self.canvas.itemconfig(self.txt_P, text=f"{self.P:.2f} bar")
        
        tank_height = self.tank_y2 - self.tank_y1
        fill_ratio = max(0.0, min(self.L / self.d_t, 1.0))
        water_y = self.tank_y2 - (fill_ratio * tank_height)
        self.canvas.coords(self.water_rect, self.tank_x1+3, water_y, self.tank_x2-3, self.tank_y2-3)
        
        # --- سیستم مدیریت آلارم و تریپ ---
        alarm_state = "NORMAL" # NORMAL, ALARM, TRIP
        alarm_msg = "SYSTEM NORMAL"
        color_L = "#fff"
        color_P = "#fff"

        # بررسی وضعیت سطح ($L$)
        if self.L >= self.L_max_trip or self.L <= self.L_min_trip:
            alarm_state = "TRIP"
            alarm_msg = "TRIP: Level Limit ($L$)"
            color_L = self.accent_red
        elif self.L >= self.L_max_op or self.L <= self.L_min_op:
            alarm_state = "ALARM"
            alarm_msg = "ALARM: Level Warning ($L$)"
            color_L = self.warning_color

        # بررسی وضعیت فشار ($P$) - تریپ اولویت بالاتری دارد
        if self.P >= self.P_max_trip or self.P <= self.P_min_trip:
            if alarm_state != "TRIP":
                alarm_msg = "TRIP: Pressure Limit ($P$)"
            else:
                alarm_msg = "TRIP: Level ($L$) & Pressure ($P$)"
            alarm_state = "TRIP"
            color_P = self.accent_red
        elif self.P >= self.P_max_op or self.P <= self.P_min_op:
            if alarm_state == "NORMAL":
                alarm_msg = "ALARM: Pressure Warning ($P$)"
                alarm_state = "ALARM"
            elif alarm_state == "ALARM":
                alarm_msg = "ALARM: Level ($L$) & Pressure ($P$)"
            color_P = self.warning_color if color_P != self.accent_red else color_P

        # اعمال تغییرات گرافیکی
        self.canvas.itemconfig(self.txt_L, fill=color_L)
        self.canvas.itemconfig(self.txt_P, fill=color_P)

        if alarm_state != "NORMAL":
            self.alarm_blink = not self.alarm_blink
            blink_color = self.panel_color
                        if alarm_state == "TRIP":
                active_color = self.accent_red
                blink_color = self.accent_red if self.alarm_blink else self.panel_color
            else:
                active_color = self.warning_color
                blink_color = self.warning_color if self.alarm_blink else self.panel_color
                
            self.led_canvas.itemconfig(self.status_led, fill=blink_color)
            self.status_label.configure(text=alarm_msg, text_color=active_color)
        else:
            self.led_canvas.itemconfig(self.status_led, fill=self.accent_green)
            self.status_label.configure(text="SYSTEM NORMAL", text_color=self.accent_green)


        if self.plots_visible:
            self.line_L.set_data(self.t_data, self.L_data)
            self.axs[0].set_xlim(self.t_data[0], max(10, self.t_data[-1]))
            self.axs[0].set_ylim(min(self.L_min_op - 0.5, self.L_set - 0.5), max(self.L_max_op + 0.5, self.L_set + 0.5))
            
            self.line_P.set_data(self.t_data, self.P_data)
            self.axs[1].set_xlim(self.t_data[0], max(10, self.t_data[-1]))
            self.axs[1].set_ylim(min(self.P_min_op - 0.2, self.P_set - 0.2), max(self.P_max_op + 0.2, self.P_set + 0.2))
            
            self.line_lcv.set_data(self.t_data, self.lcv_data)
            self.axs[2].set_xlim(self.t_data[0], max(10, self.t_data[-1]))
            
            self.line_pcv.set_data(self.t_data, self.pcv_data)
            self.axs[3].set_xlim(self.t_data[0], max(10, self.t_data[-1]))

            self.canvas_plot.draw_idle()


def simulate_system(gains):
    Kp_L, Ki_L, Kp_P, Ki_P = gains
    dt = 0.2
    sim_time = 1000
    steps = int(sim_time / dt)
    g = 9.81
    
    
    steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)
    
    d_t = SYSTEM_PARAMS["d_t"]["val"]
    L_t = SYSTEM_PARAMS["L_t"]["val"]
    ramp_rate_max = SYSTEM_PARAMS["ramp_rate_max"]["val"]
    mc_max = SYSTEM_PARAMS["mc_max"]["val"]
    ms_max = SYSTEM_PARAMS["ms_max"]["val"]
    
    min_L_op = SYSTEM_PARAMS["L_min_op"]["val"]
    max_L_op = SYSTEM_PARAMS["L_max_op"]["val"]
    min_P_op = SYSTEM_PARAMS["P_min_op"]["val"]
    max_P_op = SYSTEM_PARAMS["P_max_op"]["val"]
    
    v_min_pct = SYSTEM_PARAMS["v_min_op"]["val"]
    v_max_pct = SYSTEM_PARAMS["v_max_op"]["val"]
    rate_limit_v = SYSTEM_PARAMS["rate_limit_v"]["val"]
    
    mc_lim_min = mc_max * (v_min_pct / 100.0)
    mc_lim_max = mc_max * (v_max_pct / 100.0)
    ms_lim_min = ms_max * (v_min_pct / 100.0)
    ms_lim_max = ms_max * (v_max_pct / 100.0)

    tau_c, tau_s = SYSTEM_PARAMS["tau_c"]["val"], SYSTEM_PARAMS["tau_s"]["val"]

    L, P = SYSTEM_PARAMS["L_set"]["val"], SYSTEM_PARAMS["P_set"]["val"]
       
    rho_w_curr = steamTable.rhoL_p(P)
    rho_s_curr = steamTable.rhoV_p(P)
    
    R = d_t / 2.0
    theta = 2 * np.arccos((R - L) / R)
    V_w = 0.5 * R**2 * (theta - np.sin(theta)) * L_t
    V_tot = np.pi * R**2 * L_t
    V_s = V_tot - V_w
    
    m_w = V_w * rho_w_curr
    m_s = V_s * rho_s_curr

    
    L_set_arr = np.ones(steps) * L
    P_set_arr = np.ones(steps) * P
    L_set_arr[int(steps*0.1):] = min(L + 0.3, max_L_op)   
    P_set_arr[int(steps*0.25):] = min(P + 0.2, max_P_op)   
    
    m_w_out_target = np.ones(steps) * SYSTEM_PARAMS["m_w_out_actual"]["val"]
    m_w_out_target[int(steps*0.4):] = SYSTEM_PARAMS["m_w_out_actual"]["val"] + 10.0 
    
    hw_in_arr = np.ones(steps) * SYSTEM_PARAMS["hw_in"]["val"]
    hw_in_arr[int(steps*0.6):] -= 10.0
    
    hst_in_arr = np.ones(steps) * SYSTEM_PARAMS["hst_in"]["val"]
    hst_in_arr[int(steps*0.75):] -= 50.0 
    
    m_w_in, m_st_in = np.clip(SYSTEM_PARAMS["m_w_in"]["val"], mc_lim_min, mc_lim_max), np.clip(SYSTEM_PARAMS["m_st_in"]["val"], ms_lim_min, ms_lim_max)
    int_L, int_P = 0.0, 0.0
    m_w_out_actual = SYSTEM_PARAMS["m_w_out_actual"]["val"]
    
    cost = 0.0
    
    max_v_speed_c = (mc_lim_max - mc_lim_min) * (rate_limit_v / 100.0) * dt
    max_v_speed_s = (ms_lim_max - ms_lim_min) * (rate_limit_v / 100.0) * dt
    
    prev_cmd_L = m_w_in
    prev_cmd_P = m_st_in
    
    hw_sat_val = SYSTEM_PARAMS["h_w_sat"]["val"]

    for i in range(steps):
        L_set, P_set = L_set_arr[i], P_set_arr[i]
        hw_in_tune = hw_in_arr[i]
        hst_in_tune = hst_in_arr[i]
        
        diff = m_w_out_target[i] - m_w_out_actual
        max_step = ramp_rate_max * dt
        if abs(diff) > max_step:
            m_w_out_actual += np.sign(diff) * max_step
        else:
            m_w_out_actual = m_w_out_target[i]
            
        m_w_out = m_w_out_actual
        
        gamma = (hw_sat_val - hw_in_tune) / (hst_in_tune - hw_sat_val)
        water_ff = m_w_out / (1 + gamma)
        
        err_L = L_set - L
        int_L += err_L * dt
        cmd_L_unclamped = water_ff + (Kp_L * err_L) + (Ki_L * int_L)

        cmd_L = np.clip(cmd_L_unclamped, mc_lim_min, mc_lim_max)
        if cmd_L_unclamped != cmd_L: int_L -= err_L * dt
            
        err_P = P_set - P
        int_P += err_P * dt
        steam_ff = m_w_in * gamma
        cmd_P_unclamped = steam_ff + (Kp_P * err_P) + (Ki_P * int_P) 
        
        cmd_P = np.clip(cmd_P_unclamped, ms_lim_min, ms_lim_max)
        if cmd_P_unclamped != cmd_P: int_P -= err_P * dt

        dm_w_c = (cmd_L - m_w_in) / tau_c * dt
        dm_st_c = (cmd_P - m_st_in) / tau_s * dt
        
        m_w_in += np.clip(dm_w_c, -max_v_speed_c, max_v_speed_c)
        m_st_in += np.clip(dm_st_c, -max_v_speed_s, max_v_speed_s)
        
        u_s = steamTable.uV_p(P)
        u_w = steamTable.uL_p(P)
        nu_s = steamTable.vV_p(P)
        nu_w = steamTable.vL_p(P)
        h_w_out_curr = steamTable.hL_p(P)
        rho_w_curr = steamTable.rhoL_p(P)

        dP_epsilon = 0.001
        vV_plus = steamTable.vV_p(P + dP_epsilon)
        vV_minus = steamTable.vV_p(P - dP_epsilon)
        vL_plus = steamTable.vL_p(P + dP_epsilon)
        vL_minus = steamTable.vL_p(P - dP_epsilon)
        
        dnu_s_dp = ((vV_plus - vV_minus) / (2 * dP_epsilon)) / 100 
        dnu_w_dp = ((vL_plus - vL_minus) / (2 * dP_epsilon)) / 100 

        a11, b11, c11 = 538, 0.2149, -120.6
        a22, b22, c22, d22 = 2420, 0.6137, 2.364, 2650
        
        du_w_dp = (a11 * b11 * (P)**(b11 - 1)) / 100
        du_s_dp = (-(a22 - d22) * (b22/c22) * ((P)/c22)**(b22 - 1) / (1 + ((P)/c22)**b22)**2) / 100

        a1, a2 = u_s, u_w
        b1, b2 = nu_s, nu_w
        
        a3 = (m_s * du_s_dp + m_w * du_w_dp)
        b3 = (m_s * dnu_s_dp + m_w * dnu_w_dp)

        d1 = m_st_in * hst_in_tune + m_w_in * hw_in_tune - m_w_out * h_w_out_curr
        d2 = m_st_in + m_w_in - m_w_out

        term_denom = (b2 - b1 + (b3*a1)/a3 - (b3*a2)/a1)
        if term_denom != 0 and a3 != 0:
            dm_w_dt = (-b1*d2 - (b3*d1)/a3 + (b3*a1*d2)/a3) / term_denom
            dm_s_dt = d2 - dm_w_dt
            dp_dt = (1/a3) * (d1 - a1*dm_s_dt - a2*dm_w_dt)
        else:
            dm_w_dt, dm_s_dt, dp_dt = 0, 0, 0
        
        m_w += dm_w_dt * dt
        m_s += dm_s_dt * dt
        P += dp_dt * dt
        
        V_tot = 0.25 * np.pi * (d_t**2) * L_t
        V_w_curr = m_w / rho_w_curr
        
        drho_w_dp = - (rho_w_curr**2) * dnu_w_dp
        dV_wdt = (1/rho_w_curr)*(dm_w_dt - V_w_curr*drho_w_dp*dp_dt)

        def fun1(theta): return V_w_curr - 0.25 * (d_t**2) * L_t * (theta[0] - np.sin(theta[0])*np.cos(theta[0]))
        def fun2(theta): return V_w_curr - (0.25*np.pi*(d_t**2)*L_t - 0.25*(d_t**2)*L_t*(theta[0] - np.sin(theta[0])*np.cos(theta[0])))

        try:
            if V_w_curr <= V_tot / 2: 
                res = least_squares(fun1, [np.pi/2], bounds=(0, np.pi))
                sol1 = res.x[0]
                L = (d_t / 2) * (1 - np.cos(sol1))
                dtheta_dt = dV_wdt / (0.25*(d_t**2) * L_t *(1 + np.sin(sol1)**2 - np.cos(sol1)**2))
                dL_dt = 0.5 * d_t * np.sin(sol1) * dtheta_dt
            else: 
                res = least_squares(fun2, [np.pi/2], bounds=(0, np.pi))
                sol1 = res.x[0]
                L = (d_t / 2) * (1 + np.cos(sol1))
                dtheta_dt = dV_wdt / (-0.25*(d_t**2) * L_t *(1 + np.sin(sol1)**2 - np.cos(sol1)**2))
                dL_dt = -0.5 * d_t * np.sin(sol1) * dtheta_dt
        except: pass
        
        P_tank = P + (rho_w_curr * g * L / 10**5)

        if L < min_L_op or L > max_L_op:
            cost += 1e5
        if P_tank < min_P_op or P_tank > max_P_op:
            cost += 1e5
            
        t = i * dt
        cost += 2000 * (500 * abs(err_L) +  abs(P_set - P)) * t * dt
        
        delta_L_cmd = abs(cmd_L - prev_cmd_L)
        delta_P_cmd = abs(cmd_P - prev_cmd_P)
        cost += (delta_L_cmd + delta_P_cmd) * 10
        
        prev_cmd_L = cmd_L
        prev_cmd_P = cmd_P

    return cost

if __name__ == "__main__":
    setup_app = ParameterSetupWindow()
    setup_app.mainloop()

    temp_root = tk.Tk()
    temp_root.withdraw()
    
    should_tune = messagebox.askyesno("Tuning Required", "Do you want to tune the controller coefficients before starting?")
    
    GAIN_FILE = "pid_gains.json"

    if os.path.exists(GAIN_FILE):
        try:
            with open(GAIN_FILE, "r") as f:
                saved_gains = json.load(f)
            gains_L = tuple(saved_gains["LC"])
            gains_P = tuple(saved_gains["PC"])
            print(f"Loaded saved gains: LC={gains_L}, PC={gains_P}")
        except Exception as e:
            print("Error loading gains file:", e)
            gains_L = (160.55664003244027, 0.4142093230508659)
            gains_P = (4.460437671360029, 0.5479391528440942)
    else:
        gains_L = (160.55664003244027, 0.4142093230508659)
        gains_P = (4.460437671360029, 0.5479391528440942)
    
    if should_tune:
        print("Optimizing PID parameters... Please wait...")
        bounds = [
            (0.1, 200.0),   # Kp_L 
            (0.05, 2.0),    # Ki_L 
            (0.1, 30.0),    # Kp_P 
            (0.001, 2.0)    # Ki_P 
        ]

        result = differential_evolution(simulate_system, bounds, strategy='best1bin', maxiter=50, popsize=10, tol=0.01)
        
        gains_L = (result.x[0], result.x[1])
        gains_P = (result.x[2], result.x[3])
        
        with open(GAIN_FILE, "w") as f:
            json.dump({"LC": gains_L, "PC": gains_P}, f, indent=4)

        print("PID gains saved to pid_gains.json.")
        print("\n--- Optimized PID Gains ---")
        print(f"Level Controller (LC): Kp = {gains_L[0]:.2f}, Ki = {gains_L[1]:.2f}")
        print(f"Pressure Controller (PC): Kp = {gains_P[0]:.2f}, Ki = {gains_P[1]:.2f}")
    else:
        print("Using predefined PID parameters.")
        
    temp_root.destroy()

    root = ctk.CTk()
    app = PowerPlantSCADA(root, gains_L, gains_P)
    root.mainloop()