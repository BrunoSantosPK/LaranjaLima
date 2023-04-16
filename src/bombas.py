import os
import numpy as np
import pandas as pd
from typing import Tuple
from datetime import datetime, timedelta


class PumpParams:

    def __init__(self, temp: float, press: float, flow: float, spin: float, time: float, visc: float) -> None:
        self.__temperature = temp
        self.__pressure = press
        self.__flow = flow
        self.__spin = spin
        self.__time = time
        self.__viscosity = visc

    def set_range(
            self, temp: Tuple[float, float], press: Tuple[float, float], flow: Tuple[float, float],
            spin: Tuple[float, float], time: Tuple[float, float], visc: Tuple[float, float]
        ) -> None:
        self.__range_temperature = temp
        self.__range_pressure = press
        self.__range_flow = flow
        self.__range_spin = spin
        self.__range_time = time
        self.__range_viscosity = visc

    def generate_value(self, base: float, limits: Tuple[float, float]) -> float:
        return base + (limits[0] + (limits[1] - limits[0]) * np.random.random_sample())
    
    def get_operation(self) -> dict:
        return {
            "Temperatura de Trabalho (°C)": self.generate_value(self.__temperature, self.__range_temperature),
            "Pressão de Trabalho (bar)": self.generate_value(self.__pressure, self.__range_pressure),
            "Vazão de Trabalho (m3/h)": self.generate_value(self.__flow, self.__range_flow),
            "Rotação de Trabalho (rpm)": self.generate_value(self.__spin, self.__range_spin),
            "Tempo de Trabalho (h)": self.generate_value(self.__time, self.__range_time),
            "Viscosidade (mPa.s)": self.generate_value(self.__viscosity, self.__range_viscosity)
        }


class Pump:

    def __init__(self, pressure: float, temperature: float, flow: float, spin: float, params: PumpParams, name: str) -> None:
        self.__max_pressure = pressure
        self.__max_temperature = temperature
        self.__max_flow = flow
        self.__max_spin = spin
        self.__params = params
        self.__name = name
        
        self.__jobs = []
        self.__total_work = 0
        self.__work_before_maintenance = 0

    def get_work_time(self) -> float:
        return self.__work_before_maintenance

    def operation(self, date: datetime, preventive=False) -> None:
        # Obtêm parâmetros iniciais da operação
        registry = self.__params.get_operation()
        registry["Data Execução"] = date.isoformat()
        registry["Local"] = self.__name

        # Realiza manutenção preventiva, caso informado
        if preventive: self.maintenance()
        registry["Manutenção Preditiva"] = 1 if preventive else 0

        # Atualiza tempo de trabalho
        work_time = registry["Tempo de Trabalho (h)"]
        self.add_work_time(work_time)
        registry["Funcionamento Contínuo (h)"] = self.__work_before_maintenance

        # Caso ocorra uma quebra, faz o registro necessário
        is_break = self.break_analysis()
        if is_break: self.maintenance()
        registry["Manutenção Corretiva"] = 1 if is_break else 0

        # Adiciona os dados nominais da bomba
        registry["Pressão Máxima (bar)"] = self.__max_pressure
        registry["Temperatura Máxima (°C)"] = self.__max_temperature
        registry["Vazão Máxima (m3/h)"] = self.__max_flow
        registry["Rotação Máxima (rpm)"] = self.__max_spin

        # Armazena registro de operação
        self.__jobs.append(registry)

    def get_data(self):
        return pd.DataFrame(self.__jobs)


    def add_work_time(self, hours: float) -> None:
        self.__total_work = self.__total_work + hours
        self.__work_before_maintenance = self.__work_before_maintenance + hours

    def add_work_cicle(self, date: datetime) -> None:
        registry = self.__params.get_operation()
        registry["Data de Início"] = date
        self.__jobs.append(registry)

    def maintenance(self) -> None:
        self.__work_before_maintenance = 0

    def break_analysis(self) -> bool:
        beta, hours = 20, self.__work_before_maintenance
        prob = 0.05 if hours < 10 else np.exp(hours / beta) / (np.exp(hours / beta) + 1)
        sort = np.random.random_sample()
        return True if sort < prob else False


if __name__ == "__main__":
    # Bomba na área de descarga, transfere o leite do caminhão para os tanques
    params_01 = PumpParams(20, 2, 80, 500, 1, 2.2)
    params_01.set_range((-2, 1), (-0.5, 0.5), (-10, 60), (-50, 200), (-0.2, 0.6), (-0.5, 0.3))
    pump_01 = Pump(10, 120, 180, 1800, params_01, "Bomba da Entrada")

    # Bombas dos tanques de armazenamento para o misturador
    params_02 = PumpParams(18, 1, 50, 800, 0.8, 2.0)
    params_02.set_range((-1, 4), (-0.1, 0.3), (-10, 60), (-50, 50), (-0.1, 0.3), (-0.1, 0.6))
    pump_02 = Pump(10, 120, 180, 1800, params_02, "Bomba do Misturador")

    # Bomba para transporte de leite no trocador de calor de aquecimento
    # temperatura, pressão, vazão, rotação, tempo e viscosidade
    params_03 = PumpParams(21, 1, 80, 700, 0.1, 2.2)
    params_03.set_range((-1, 2), (0, 0.1), (-10, 20), (-50, 50), (0, 0.1), (-0.1, 0.1))
    pump_03 = Pump(10, 120, 180, 1800, params_03, "Bomba de Leite do Trocador de Calor")

    # Bomba para transporte de água no trocador de calor de aquecimento
    params_04 = PumpParams(50, 1.5, 30, 1000, 0.1, 1)
    params_04.set_range((-2, 5), (0, 0.6), (-5, 10), (-100, 100), (0, 0.1), (-0.1, 0.2))
    pump_04 = Pump(3, 90, 40, 3500, params_04, "Bomba de Água do Trocador de Calor")

    # Bomba para transporte de leite no trocador de calor de resfriamento

    # Bomba para transporte de água no trocador de calor de resfriamento

    # Bomba de alimentação de leite no envase

    # Define período de operação
    start_date = datetime(2022, 1, 1, 8, 0, 0)
    end_date = datetime(2023, 4, 30, 18, 0, 0)
    current_date = start_date

    while current_date < end_date:
        # Caso serja no período noturno, não funcinam as bombas
        if current_date.hour >= 18:
            current_date = current_date + timedelta(hours=2)
            continue

        # Simula operação
        preventive_limit = 15
        pump_01.operation(current_date, preventive=(True if pump_01.get_work_time() > preventive_limit else False))
        pump_02.operation(current_date, preventive=(True if pump_02.get_work_time() > preventive_limit else False))
        pump_03.operation(current_date, preventive=(True if pump_03.get_work_time() > preventive_limit else False))
        pump_04.operation(current_date, preventive=(True if pump_04.get_work_time() > preventive_limit else False))

        # Avança no tempo
        current_date = current_date + timedelta(hours=2)

    # Recupera dados
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    with pd.ExcelWriter(f"{base_path}/data/Laticínio.xlsx", mode="a", if_sheet_exists="replace") as file:
        pd.concat([
            pump_01.get_data(),
            pump_02.get_data(),
            pump_03.get_data(),
            pump_04.get_data()
        ]).to_excel(file, sheet_name="Bombas", index=False)
