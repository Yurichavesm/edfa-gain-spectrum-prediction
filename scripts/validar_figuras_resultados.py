# 11 - VALIDACAO INDEPENDENTE DAS FIGURAS E DOS RESULTADOS
# Pode ser executada em notebook Python novo, sem FIG_DADOS ou outras variáveis prévias.
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path('/Volumes/workspace/default/ofc2026')
RESULTADOS = RAIZ / 'resultados/modelagem_espectral_transferencia'
FIGURAS = RESULTADOS / 'figuras_relatorio'

nomes_figuras = [
    'figura_01_esquema_edfa',
    'figura_02_pipeline',
    'figura_03_arquitetura_mlp',
    'figura_04_pretrain_cosmos',
    'figura_05_exemplos_canais_ativos',
    'figura_06_distribuicao_mae',
]

for nome in nomes_figuras:
    for extensao in ('png', 'pdf'):
        arquivo = FIGURAS / f'{nome}.{extensao}'
        if not arquivo.is_file() or arquivo.stat().st_size == 0:
            raise FileNotFoundError(
                f'Figura ausente/vazia: {arquivo}. Execute a seção 10 das figuras.'
            )
print('1. Figuras: seis PNGs e seis PDFs presentes e não vazios. OK')

colunas_ganho = [f'calculated_gain_spectra_{i:02d}' for i in range(95)]
colunas_mascara = [f'DUT_WSS_activated_channel_index_{i:02d}' for i in range(95)]

entrada = RAIZ / 'Features/TestGround/test_features.csv'
rotulos = RAIZ / 'Features/TestGround/test_labels.csv'
previsoes = RESULTADOS / 'predicoes_mlp_v2_48ep_testground.csv'

for arquivo in (entrada, rotulos, previsoes):
    if not arquivo.is_file():
        raise FileNotFoundError(f'Dados necessários ausentes: {arquivo}')

X = pd.read_csv(entrada)
Y = pd.read_csv(rotulos, usecols=colunas_ganho)[colunas_ganho].to_numpy(float)
P = pd.read_csv(previsoes, usecols=colunas_ganho)[colunas_ganho].to_numpy(float)
M = X[colunas_mascara].to_numpy(bool)

if X.shape[0] != 21056 or Y.shape != (21056, 95) or P.shape != Y.shape or M.shape != Y.shape:
    raise AssertionError(f'Dimensões incorretas: X={X.shape}, Y={Y.shape}, P={P.shape}, M={M.shape}')

ativos_por_registro = M.sum(axis=1)
if np.any(ativos_por_registro == 0):
    raise AssertionError('Há registros sem canais ativos')
if int(M.sum()) != 262144:
    raise AssertionError(f'Total de canais ativos inesperado: {int(M.sum())}')
if not (np.isfinite(Y[M]).all() and np.isfinite(P[M]).all()):
    raise AssertionError('Ganho não finito em canal ativo')

mae_por_registro = np.where(M, np.abs(Y-P), 0.0).sum(axis=1) / ativos_por_registro

def conferir(rotulo, obtido, esperado, tol=1e-5):
    if not np.isclose(obtido, esperado, rtol=0, atol=tol):
        raise AssertionError(f'{rotulo}: {obtido:.9f} dB, esperado {esperado:.9f} dB')
    print(f'{rotulo}: {obtido:.6f} dB — OK')

conferir('2. MAE global por observação', float(mae_por_registro.mean()), 0.124232492)
conferir('3. MAE por canal ativo', float(np.abs(Y[M]-P[M]).mean()), 0.106953)

for categoria, n, esperado in [
    ('aging', 4400, 0.087264),
    ('shb', 864, 0.105130),
    ('unseen', 15792, 0.135578),
]:
    selecionadas = X['Category'].astype(str).str.lower().eq(categoria).to_numpy()
    if int(selecionadas.sum()) != n:
        raise AssertionError(f'Cenário {categoria}: número inesperado de observações')
    conferir(f'4. {categoria.upper()}', float(mae_por_registro[selecionadas].mean()), esperado)

for uso, esperado in [('public', 0.127922), ('private', 0.120543)]:
    selecionadas = X['Usage'].astype(str).str.lower().eq(uso).to_numpy()
    if int(selecionadas.sum()) != 10528:
        raise AssertionError(f'Partição {uso}: número inesperado de observações')
    conferir(f'5. {uso.title()}', float(mae_por_registro[selecionadas].mean()), esperado)

print('VALIDAÇÃO INDEPENDENTE CONCLUÍDA: resultados numéricos e arquivos gráficos conferidos.')
print('Observação: é necessário verificar visualmente a legibilidade das imagens.')
