# Seleção das células e decisões metodológicas

Este repositório publica **somente o pipeline da MLP residual final**. Os notebooks exploratórios originais permanecem fora desta versão pública.

| Etapa publicada | Origem no estudo | Propósito |
|---|---|---|
| Ambiente | Configuração sintetizada | Clonar o preprocessador SJTU no commit fixado |
| Divisão COSMOS | Notebook 12, divisão original | Guardar índices de treino e validação (seed 42) |
| Pré-treino 8 épocas | Notebook 12, célula 10 | Treinar MLP residual inicial |
| Continuação até 24 | Notebook 12, célula 14 | Refinar pesos e salvar checkpoint |
| Continuação até 48 | Notebook 12, célula 17 | Selecionar checkpoint final de pré-treino |
| Folds agrupados | Notebook 06, célula 05 (somente divisão) | Recriar folds sem executar regressão com FFT |
| Validação cruzada | Notebook 12, célula 18 | Avaliar apenas a MLP de 48 épocas |
| Ajuste fino e TestGround | Notebook 12, célula 20 | Treinar 40 épocas e gerar previsões |
| Auditoria | Notebook 12, célula 25 | Reconstruir preprocessor, inferência e MAE |
| Figuras | Script independente | Produzir diagramas e gráficos dos resultados |

**Fora do repositório essencial:** FFT, GPR, Ridge, CatBoost, CNN e ensembles; não são dependências do modelo selecionado. A operação de definir folds, originalmente localizada no notebook exploratório 06, foi retida porque faz parte do protocolo de validação e não executa o modelo descartado.

**Status de reprodutibilidade (23/11/2026):** o notebook filtrado foi executado pelo autor no Databricks e seus outputs foram enviados para auditoria. O treinamento COSMOS (8/24/48 épocas), a validação agrupada, o ajuste fino de 40 épocas e a auditoria final produziram as métricas de referência, inclusive MAE TestGround online de **0,124232492 dB**. As células originais de código do pipeline publicado correspondem às do notebook executado. Esta é uma **verificação dos outputs e do código enviado**, não uma reexecução independente em outro ambiente. Mais detalhes em [VALIDACAO_EXECUCAO_2026-11-23.md](VALIDACAO_EXECUCAO_2026-11-23.md).

**Cuidados:** o TestGround foi consultado durante o desenvolvimento e não deve ser tratado como teste final independente. O benchmark inclui o atributo `EDFA_output_power_total` como entrada, com limitações de aplicabilidade antes de medir a saída do equipamento.
