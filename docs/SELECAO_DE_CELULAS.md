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

**Status de reprodutibilidade:** o conteúdo foi selecionado e verificado quanto à estrutura/sintaxe; não passou por execução limpa integral no Databricks. O MAE de referência (0,124232492 dB, TestGround online) foi reproduzido anteriormente com o checkpoint salvo, mas **não foi revalidado a partir de um novo treinamento executando este notebook filtrado**. Registre versões de bibliotecas, saídas e divergências caso existam.

**Cuidados:** o TestGround foi consultado durante o desenvolvimento e não deve ser tratado como teste final independente. O benchmark inclui o atributo `EDFA_output_power_total` como entrada, com limitações de aplicabilidade antes de medir a saída do equipamento.
