import numpy as np
import matplotlib.pyplot as plt

# Coeficientes oficiais do NIST (ITS-90) para a faixa que cobre 0 a 400 °C
coefficients = {
    # Faixa original NIST: 0.000 a 630.615 °C 
    'B': [0.0, -0.246508183460e-3, 0.590404211710e-5, -0.132579316360e-8, 0.156682919010e-11, -0.169445292400e-14, 0.629903470940e-18],
    # - Faixa original NIST: 0.000 a 1000.000 °C 
    'E': [0.0, 0.586655087100e-1, 0.450322755820e-4, 0.289084072120e-7, -0.330568966520e-09, 0.650244032700e-12, -0.191974955040e-15, -0.125366004970e-17, 0.214892175690e-20, -0.143880417820e-23, 0.359608994810e-27],
    # Faixa original NIST: 0.000 a 760.000 °C 
    'J': [0.0, 0.50381187815e-1, 0.30475836930e-4, -0.85681065720e-7, 0.13228195295e-9, -0.17052958337e-12, 0.20948090697e-15, -0.12538395336e-18, 0.15631725697e-22],
    # Faixa original NIST: 0.000 a 1372.000 °C
    'K': [-0.176004136860e-1, 0.389212049750e-1, 0.185587700320e-4, -0.994575928740e-7, 0.318409457190e-9, -0.560728448890e-12, 0.560750590590e-15, -0.320207200030e-18, 0.971511471520e-22, -0.121047212750e-25],
    # Faixa original NIST: 0.000 a 1300.000 °C 
    'N': [0.0, 0.259293946010e-1, 0.157101418800e-4, 0.438256272370e-07, -0.252611697940e-09, 0.643118193390e-12, -0.100634715190e-14, 0.997453389920e-18, -0.608632456070e-21, 0.208492293390e-24, -0.306821961510e-28],
    # Faixa original NIST: -50.000 a 1064.180 °C 
    'R': [0.0, 0.528961729765e-02, 0.139166589782e-04, -0.238855693017e-07, 0.356916001063e-10, -0.462347666298e-13, 0.500777441034e-16, -0.373105886191e-19, 0.157716482367e-22, -0.281038625251e-26],
    # Faixa original NIST: -50.000 a 1064.180 °C 
    'S': [0.0, 0.540313308631e-02, 0.125934289740e-04, -0.232477968689e-07, 0.322028823036e-10, -0.331465196389e-13, 0.255744251786e-16, -0.125068871393e-19, 0.271443176145e-23],
    # Faixa original NIST: 0.000 a 400.000 °C 
    'T': [0.0, 0.387481063640e-01, 0.332922278800e-04, 0.206182434040e-06, -0.218822568460e-08, 0.109968809280e-10, -0.308157587720e-13, 0.454791352900e-16, -0.275129016730e-19]
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
    thermocouple_type = input("Diga qual tipo de termopar gostarias de ver o gráfico:").upper().strip()

    if thermocouple_type in coefficients:
        mV_calculados = calcular_mv(thermocouple_type, t_valores)
    
        plt.plot(t_valores, mV_calculados, label =f'Tipo {thermocouple_type}', color = 'blue')
        plt.title(f'Termopar Tipo {thermocouple_type}: Temperatura x mV')
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
        print(f"Tipo do termopar inválido, {thermocouple_type} não é uma opção válida")

