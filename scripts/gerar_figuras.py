"""Figuras 1--6 do estudo dirigido OFC/EDFA.

Dados reais somente: as figuras 4, 5 e 6 lêem históricos, rótulos
TestGround e previsões auditadas; nenhuma série é sintetizada.
Figuras 1 a 3 sao esquemas conceituais. Gera PNG/PDF em arquivo temporario local
e depois copia ao Volume, evitando escrita aleatoria no Unity Catalog.

Execução em Databricks:
  python scripts/gerar_figuras.py --root /Volumes/workspace/default/ofc2026
Ou execute o conteúdo da cópia notebook/celula_26_figuras.py em uma célula.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile
import shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

N_CANAIS = 95
COLUNAS_LABEL = [f'calculated_gain_spectra_{i:02d}' for i in range(N_CANAIS)]
COLUNAS_MASK = [f'DUT_WSS_activated_channel_index_{i:02d}' for i in range(N_CANAIS)]


def salvar(fig, destino, nome):
    destino.mkdir(parents=True, exist_ok=True)
    # Gera em disco local: alguns sistemas de arquivo (Unity Catalog
    # Volumes) não suportam todas as operações de escrita do backend PDF.
    with tempfile.TemporaryDirectory(prefix='edfa_fig_') as temp:
        for ext in ('png', 'pdf'):
            origem = Path(temp) / f'{nome}.{ext}'
            fig.savefig(origem, dpi=240, bbox_inches='tight')
            shutil.copyfile(origem, destino / origem.name)
    plt.close(fig)
    print(f'Figura salva: {destino / (nome + ".png")}')


def bloco(ax, x, y, w, h, titulo, tamanho=11):
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.025',
                           linewidth=1.3, facecolor='none', edgecolor='0.30')
    ax.add_patch(patch)
    ax.text(x+w/2, y+h/2, titulo, ha='center', va='center', fontsize=tamanho)


def seta(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',
                                 mutation_scale=14, linewidth=1.25))


def figura1(destino):
    """Esquema conceitual, não um modelo físico detalhado."""
    fig, ax = plt.subplots(figsize=(11,3.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis('off')
    bloco(ax, .3, 1.6, 2, .9, 'Sinais WDM\n(entrada)')
    bloco(ax, 3.25, 1.6, 3.1, .9, 'Fibra dopada com érbio\n(EDFA)')
    bloco(ax, 7.2, 1.6, 2.4, .9, 'Sinais amplificados\n(saída)')
    bloco(ax, 3.75, 3.05, 2.1, .65, 'Bombeamento\nóptico', 10)
    seta(ax, 2.35, 2.05, 3.2, 2.05)
    seta(ax, 6.4, 2.05, 7.15, 2.05)
    seta(ax, 4.8, 3.02, 4.8, 2.55)
    ax.set_title('Figura 1 — Esquema conceitual de um EDFA', pad=12)
    salvar(fig, destino, 'figura_01_esquema_edfa')


def figura2(destino):
    """Fluxo experimental: ambos checkpoint e Challenge entram no ajuste fino."""
    fig, ax = plt.subplots(figsize=(13, 4.8))
    ax.set_xlim(0, 14); ax.set_ylim(0, 5.7); ax.axis('off')
    bloco(ax, .2, 3.65, 2.4, 1.05, 'COSMOS\n138.624 observações', 10)
    bloco(ax, 3.05, 3.65, 2.55, 1.05, 'Pré-treinamento MLP\n48 épocas', 10)
    bloco(ax, 6.1, 3.65, 2.5, 1.05, 'Checkpoint\npré-treinado', 10)
    bloco(ax, .2, 1.08, 2.4, 1.05, 'Challenge Train\n490 observações', 10)
    bloco(ax, 6.1, 1.08, 2.5, 1.05, 'Ajuste fino\n40 épocas', 10)
    bloco(ax, 9.15, 1.08, 1.7, 1.05, 'MLP final\n95 saídas', 10)
    bloco(ax, 11.32, .94, 2.45, 1.33,
          'Avaliação retrospectiva\nTestGround online\n21.056 observações', 9)
    seta(ax, 2.65, 4.17, 3.00, 4.17)
    seta(ax, 5.65, 4.17, 6.05, 4.17)
    seta(ax, 7.35, 3.60, 7.35, 2.18)
    seta(ax, 2.65, 1.60, 6.05, 1.60)
    seta(ax, 8.65, 1.60, 9.10, 1.60)
    seta(ax, 10.90, 1.60, 11.27, 1.60)
    ax.text(7.57, 2.92, 'Transferência\ndos pesos',
            fontsize=9, ha='left', va='center')
    ax.set_title('Figura 2 — Fluxo metodológico do estudo', pad=10, fontsize=13)
    salvar(fig, destino, 'figura_02_pipeline')


def figura3(destino):
    fig, ax = plt.subplots(figsize=(12,3.7))
    ax.set_xlim(0, 13); ax.set_ylim(0, 4); ax.axis('off')
    blocos = [(0.15, 'Entradas\n204'),(2.2,'Linear + GELU\n256'),
              (4.45,'Linear + GELU\n256'),(6.7,'Linear + GELU\n128'),
              (8.95,'Resíduos\n95'),(11.1,'Ganho previsto\n95')]
    for x, s in blocos:
        bloco(ax, x, 1.5, 1.72, .9, s, 9.5)
    for (xa,_),(xb,_) in zip(blocos,blocos[1:]):
        seta(ax, xa+1.76, 1.95, xb-.06, 1.95)
    ax.text(10.05, .65, 'Somar referência linear de ganho e tilt',
            ha='center', fontsize=9)
    ax.text(3.3, 1.12, 'Dropout 0,10 nas duas primeiras camadas ocultas',
            ha='center', fontsize=9)
    ax.set_title('Figura 3 — Arquitetura MLP residual', pad=8)
    salvar(fig, destino, 'figura_03_arquitetura_mlp')


def figura4(destino, resultados):
    arquivos = [
        (resultados/'historico_mlp_v2.csv', 'mae_cosmos_val'),
        (resultados/'historico_pretrain_extended.csv', 'mae_val'),
        (resultados/'historico_pretrain_48ep.csv', 'mae_cosmos_val')
    ]
    partes = []
    for caminho, coluna in arquivos:
        if not caminho.exists():
            raise FileNotFoundError(f'Histórico necessário ausente: {caminho}')
        df = pd.read_csv(caminho)
        if not {'epoca', coluna}.issubset(df.columns):
            raise ValueError(f'Colunas inesperadas em {caminho}: {list(df.columns)}')
        partes.append(df[['epoca', coluna]].rename(columns={coluna: 'mae'}))
    hist = pd.concat(partes, ignore_index=True).sort_values('epoca')
    hist = hist.drop_duplicates('epoca', keep='last')
    if not set(range(1,49)).issubset(set(hist['epoca'].astype(int))):
        raise ValueError('Histórico incompleto: conferir épocas 1 a 48')
    fig, ax = plt.subplots(figsize=(9,4.2))
    ax.plot(hist['epoca'], hist['mae'], marker='.', linewidth=1.7)
    ax.axvline(8, linestyle='--', linewidth=1, alpha=.65)
    ax.axvline(24, linestyle='--', linewidth=1, alpha=.65)
    ax.set_xlabel('Época de pré-treinamento COSMOS')
    ax.set_ylabel('MAE de validação COSMOS (dB)')
    ax.set_title('Figura 4 — Evolução do MAE durante o pré-treinamento')
    ax.grid(alpha=.2)
    salvar(fig, destino, 'figura_04_pretrain_cosmos')


def carregar_validar(root, resultados):
    X = pd.read_csv(root/'Features/TestGround/test_features.csv')
    Y = pd.read_csv(root/'Features/TestGround/test_labels.csv')[COLUNAS_LABEL].to_numpy(float)
    P = pd.read_csv(resultados/'predicoes_mlp_v2_48ep_testground.csv')[COLUNAS_LABEL].to_numpy(float)
    M = X[COLUNAS_MASK].to_numpy(bool)
    if Y.shape != P.shape or P.shape != M.shape or P.shape != (21056,95):
        raise ValueError(f'Dimensões incompatíveis: Y={Y.shape}, P={P.shape}, M={M.shape}')
    if not (M.sum(axis=1)>0).all():
        raise ValueError('Observações sem canais ativos')
    if not (np.isfinite(Y[M]).all() and np.isfinite(P[M]).all()):
        raise ValueError('Valores não finitos em canais ativos')
    erro = (np.where(M, np.abs(Y-P), 0).sum(axis=1) / M.sum(axis=1))
    print(f'MAE local reproduzido: {erro.mean():.9f} dB')
    if not np.isclose(erro.mean(), 0.124232492, rtol=0, atol=1e-5):
        raise ValueError('O MAE não coincide com o resultado auditado; conferir arquivos!')
    cat = X['Category'].str.lower()
    for nome,n,mae_esperado in [('aging',4400,0.087264),
                                 ('shb',864,0.105130),
                                 ('unseen',15792,0.135578)]:
        sub = erro[cat.eq(nome).to_numpy()]
        if len(sub)!=n or not np.isclose(sub.mean(),mae_esperado,rtol=0,atol=1e-5):
            raise ValueError(f'Cenário {nome} inesperado: n={len(sub)}, MAE={sub.mean()}')
    usage = X['Usage'].astype(str)
    for nome,n,mae_esperado in [('Public',10528,0.127922),
                                 ('Private',10528,0.120543)]:
        sub = erro[usage.eq(nome).to_numpy()]
        if len(sub)!=n or not np.isclose(sub.mean(),mae_esperado,rtol=0,atol=1e-5):
            raise ValueError(f'Partição {nome} inesperada: n={len(sub)}, MAE={sub.mean()}')
    mae_canal_ativo = float(np.mean(np.abs(Y[M]-P[M])))
    if not np.isclose(mae_canal_ativo,0.106953,rtol=0,atol=1e-5):
        raise ValueError(f'MAE por canal ativo inesperado: {mae_canal_ativo}')
    print(f'MAE global por canal ativo: {mae_canal_ativo:.6f} dB')
    print('Conferência por cenário e Public/Private: aprovada')
    return X,Y,P,M,erro


def figura5(destino, X, Y, P, M, erro):
    """Escolhe observação com MAE próximo à mediana por cenário.

    Todos os pontos apresentados correspondem a canais ativos;
    não conecta pontos distantes, evitando interpolação inexistente.
    """
    categorias = X['Category'].str.lower().to_numpy()
    fig, eixos = plt.subplots(1,3,figsize=(14,4.3),sharey=False)
    escolhidos = []
    for ax,cat in zip(eixos, ('aging','shb','unseen')):
        idx_cat = np.flatnonzero(categorias == cat)
        if not len(idx_cat): raise ValueError(f'Categoria ausente: {cat}')
        # Se possível, evita uma única amostra ativa; caso não, mantém o registro.
        possiveis = idx_cat[M[idx_cat].sum(axis=1)>=2]
        if len(possiveis)==0: possiveis=idx_cat
        alvo = np.median(erro[possiveis])
        idx = int(possiveis[np.argmin(np.abs(erro[possiveis]-alvo))])
        canais = np.flatnonzero(M[idx])
        ax.scatter(canais,Y[idx,canais],s=40,marker='o',label='Observado')
        ax.scatter(canais,P[idx,canais],s=40,marker='x',label='Previsto')
        ax.set_xlim(-1,95)
        ax.set_xlabel('Índice do canal óptico')
        ax.set_title(f'{cat.upper()}\nMAE = {erro[idx]:.4f} dB',fontsize=10)
        ax.grid(alpha=.2)
        ax.legend(fontsize=8)
        escolhidos.append({'cenario':cat,'indice_linha_csv':idx,
                           'id':str(X.iloc[idx]['ID']) if 'ID' in X else '',
                           'ativos':len(canais),'mae_observacao':erro[idx]})
    eixos[0].set_ylabel('Ganho espectral (dB)')
    fig.suptitle('Figura 5 — Ganho observado e previsto apenas nos canais WSS ativos',fontsize=12)
    fig.tight_layout()
    salvar(fig, destino, 'figura_05_exemplos_canais_ativos')
    pd.DataFrame(escolhidos).to_csv(destino/'figura_05_indices_selecionados.csv',index=False)
    print('Observações representadas na Figura 5:')
    print(pd.DataFrame(escolhidos).to_string(index=False))


def figura6(destino, X, erro):
    """Boxplot da distribuicao do MAE por registro, como no relatorio.

    Hastes P5--P95, todos os pontos fora da faixa mostrados; valores
    nulos ou abaixo do limite positivo do eixo log nao sao desenhados.
    """
    categorias = X['Category'].str.lower().to_numpy()
    grupos = [erro[categorias==cat] for cat in ('aging','shb','unseen')]
    fig, ax = plt.subplots(figsize=(9,4.8))
    ax.boxplot(grupos, tick_labels=['Aging','SHB','Unseen'],
               whis=(5,95), showfliers=True,
               flierprops={'marker':'.','markersize':2,'alpha':.3})
    ax.set_yscale('log')
    ax.set_ylim(bottom=1e-5)
    ax.set_ylabel('MAE por observação (dB) — escala logarítmica')
    ax.set_title('Figura 6 — Distribuição do MAE por cenário')
    ax.grid(axis='y',alpha=.25,which='both')
    fig.tight_layout()
    salvar(fig,destino,'figura_06_distribuicao_mae')
    resumo = []
    for cat,v in zip(('aging','shb','unseen'),grupos):
        resumo.append({'cenario':cat,'n':len(v),'mae_medio':np.mean(v),
                       'mediana':np.median(v),'p95':np.quantile(v,.95),
                       'p99':np.quantile(v,.99),'maximo':np.max(v),
                       'erros_iguais_zero':int((v==0).sum())})
    tab = pd.DataFrame(resumo)
    tab.to_csv(destino/'figura_06_resumo_mae.csv',index=False)
    print('Resumo por cenário:')
    print(tab.to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description='Gerar figuras com dados OFC auditados')
    parser.add_argument('--root',default='/Volumes/workspace/default/ofc2026')
    parser.add_argument('--outdir',default=None)
    parser.add_argument('--only',nargs='*',type=int,default=list(range(1,7)))
    args, extras = parser.parse_known_args()  # compatibilidade com notebooks
    root = Path(args.root)
    resultados = root/'resultados/modelagem_espectral_transferencia'
    outdir = Path(args.outdir) if args.outdir else resultados/'figuras_relatorio'
    escolhidas = set(args.only)
    for k in escolhidas:
        if k not in range(1,7): raise ValueError(f'Figura inválida: {k}')
    if 1 in escolhidas: figura1(outdir)
    if 2 in escolhidas: figura2(outdir)
    if 3 in escolhidas: figura3(outdir)
    if 4 in escolhidas: figura4(outdir,resultados)
    if 5 in escolhidas or 6 in escolhidas:
        X,Y,P,M,erro = carregar_validar(root,resultados)
        if 5 in escolhidas: figura5(outdir,X,Y,P,M,erro)
        if 6 in escolhidas: figura6(outdir,X,erro)
    print('\nFiguras geradas em:',outdir)


if __name__ == '__main__':
    main()