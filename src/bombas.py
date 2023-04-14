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

    def __init__(self, pressure: float, temperature: float, flow: float, spin: float, params: PumpParams) -> None:
        self.__max_pressure = pressure
        self.__max_temperature = temperature
        self.__max_flow = flow
        self.__max_spin = spin
        self.__params = params
        
        self.__jobs = []
        self.__total_work = 0
        self.__work_before_maintenance = 0

    def operation(self, date: datetime, preventive=False) -> None:
        # Obtêm parâmetros iniciais da operação
        registry = self.__params.get_operation()
        registry["Data Execução"] = date.isoformat()

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
        beta, hours = 250, self.__work_before_maintenance
        prob = 0.05 if hours < 100 else np.exp(hours / beta) / (np.exp(hours / beta) + 1)
        sort = np.random.random_sample()
        return True if sort < prob else False


if __name__ == "__main__":
    # Bomba na área de descarga, transfere o leite do caminhão para os tanques
    params_01 = PumpParams(20, 2, 80, 500, 0.5, 2.2)
    params_01.set_range((-2, 1), (-0.5, 0.5), (-10, 60), (-50, 200), (-0.2, 0.6), (-0.5, 0.3))
    pump_01 = Pump(10, 120, 180, 1800, params_01)

    # Bombas dos tanques de armazenamento para o misturador

    # Bomba para transporte de leite no trocador de calor de aquecimento

    # Bomba para transporte de água no trocador de calor de aquecimento

    # Bomba para transporte de leite no trocador de calor de resfriamento

    # Bomba para transporte de água no trocador de calor de resfriamento

    # Bomba de alimentação de leite no envase

    # Define período de operação
    start_date = datetime(2022, 1, 1, 8, 0, 0)
    end_date = datetime(2023, 4, 30, 18, 0, 0)
    current_date = start_date
    continuous = 0

    while current_date < end_date:
        # Verifica se será executa uma manutenção preventiva
        preventive = False
        if continuous >= 336:
            preventive = True
            continuous = 0

        # Simula operação
        pump_01.operation(current_date, preventive=preventive)

        # Avança no tempo
        current_date = current_date + timedelta(hours=2)
        continuous = continuous + 2

    # Recupera dados
    pump_01.get_data().to_csv("data/simulacao.csv", index=False, sep=";")
