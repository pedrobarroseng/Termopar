import numpy as np
import matplotlib.pyplot as plt

# Coeficientes oficiais do NIST (ITS-90) para a faixa que cobre 0 a 400 °C
coefficients = {
    # Faixa original NIST: 0.000 a 630.615 °C (Perfeito para nosso range)
    'B': [0.0, -0.246508183460e-3, 0.590404211710e-5, -0.132579316360e-8, 0.156682919010e-11, -0.169445292400e-14, 0.629903470940e-18],
    # Faixa original NIST: 0.000 a 1000.000 °C (Perfeito para nosso range)
    'E': [0.0, 0.58665505700e-1, 0.45411050900e-4, -0.29441258600e-7, 0.10279313500e-10, -0.31047582700e-13, 0.55107333400e-16, -0.56546682100e-19, 0.25260828200e-22],
    # Faixa original NIST: 0.000 a 760.000 °C (Perfeito para nosso range)
    'J': [0.0, 0.50381187815e-1, 0.30475836930e-4, -0.85681065720e-7, 0.13228195295e-9, -0.17052958337e-12, 0.20948090697e-15, -0.12538395336e-18, 0.15631725697e-22],
    # Faixa original NIST: 0.000 a 1372.000 °C (CORRIGIDO: Faixa positiva que contém o range 0-400 °C)
    'K': [-0.176004136860e-1, 0.389212049750e-1, 0.185587700320e-4, -0.994575928740e-7, 0.318409457190e-9, -0.560728448890e-12, 0.560750590590e-15, -0.320207200030e-18, 0.971511471520e-22, -0.121047212750e-25],
    # Faixa original NIST: 0.000 a 1300.000 °C (Perfeito para nosso range)
    'N': [0.0, 0.25929394601e-1, 0.15710141880e-4, -0.43825627237e-7, 0.25261169794e-10, -0.91707073056e-14, 0.20493494285e-16, -0.27035706786e-19, 0.19846983828e-22, -0.61564175373e-26],
    # Faixa original NIST: -50.000 a 1064.180 °C (Perfeito para nosso range)
    'R': [0.0, 0.52896172970e-2, 0.13916658978e-4, -0.23885569305e-7, 0.35691600106e-10, -0.46234766629e-13, 0.46589269141e-16, -0.32658083445e-19, 0.14408561999e-22, -0.35887343270e-26, 0.38011116055e-30],
    # Faixa original NIST: -50.000 a 1064.180 °C (Perfeito para nosso range)
    'S': [0.0, 0.54031330266e-2, 0.12593428974e-4, -0.15247048156e-7, 0.23887673819e-10, -0.29141375376e-13, 0.29235728779e-16, -0.20054186064e-19, 0.87138566785e-23, -0.21661065921e-26, 0.22414791914e-30],
    # Faixa original NIST: 0.000 a 400.000 °C (Casamento exato com o range do trabalho)
    'T': [0.0, 0.38748106364e-1, 0.33190198092e-4, -0.16307418306e-6, 0.53544663799e-9, -0.11156384414e-11, 0.15174005256e-14, -0.11878147683e-17, 0.41324442900e-21]
}

def calcular_mv(tipo, t):
    c = coefficients[tipo]
    # Executa o somatório do polinômio c_j * t^j
    val = sum(coef * (t**j) for j, coef in enumerate(c))
    
    # Ajuste exponencial obrigatório do NIST específico para o tipo K
    if tipo == 'K':
        a0, a1, a2 = 0.1185976, -0.1183432e-3, 0.1269686e3
        val += a0 * np.exp(a1 * (t - a2)**2)
    return val

# Gerar temperaturas de 0 a 400 °C com passos de 0,5 °C
t_valores = np.arange(0, 400.5, 0.5)

while True:
    print("Tipos de termopar: B, E, J, K, N, R, S, T")
    tipo_termopar = input("Diga qual tipo de termopar gostarias de ver o gráfico:").upper().strip()

    if tipo_termopar in coefficients:
        mV_calculados = calcular_mv(tipo_termopar, t_valores)
    
        plt.plot(t_valores, mV_calculados, label =f'Tipo {tipo_termopar}', color = 'blue')
        plt.title(f'Termopar Tipo {tipo_termopar}: Temperatura x mV')
        plt.xlabel('Temperatura (°C)')
        plt.ylabel(f'Tensão (mV)')
        plt.grid(True)
        plt.legend()
        
        # Plotar o gráfico com todos os tipos juntos
        print("\nPlotando todos os tipos de termopares juntos:")

        plt.figure(figsize=(11, 7))
        for tipo in sorted(coefficients.keys()):
            mv_valores = calcular_mv(tipo, t_valores) 
            plt.plot(t_valores, mv_valores, label=f'Tipo {tipo}', linewidth=2)

        plt.title('Curvas Características de Termopares (ITS-90): 0 a 400 °C', fontsize=14, fontweight='bold')
        plt.xlabel('Temperatura (°C)', fontsize=12)
        plt.ylabel('Força Eletromotriz (mV)', fontsize=12)
        plt.xlim(0, 400)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(loc='upper left', shadow=True)
        plt.tight_layout()
        plt.savefig('grafico_termopares_0_400.png', dpi=300)
        plt.show()

        break
    
    else:
        print(f"Tipo do termopar inválido, {tipo_termopar} não é uma opção válida")

