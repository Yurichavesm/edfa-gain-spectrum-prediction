# Validação da execução do pipeline essencial — 23/11/2026

## Escopo e evidência
Esta nota registra a **inspeção dos códigos e outputs** do notebook `01_pipeline_mlp_essencial_executado.ipynb`, exportado do Databricks pelo autor. Os nove blocos de código do pipeline publicados no repositório foram comparados com o notebook executado e **têm o mesmo conteúdo de origem**. A versão executada acrescenta apenas uma célula `%pip install torch --extra-index-url https://download.pytorch.org/whl/cpu` antes da configuração do ambiente. O notebook exportado tem formato Jupyter válido; todas as células de código possuem outputs; não há outputs do tipo erro nem avisos de execução detectados.

**Limite da evidência:** auditoria dos outputs fornecidos, não reexecução independente em outro ambiente. Os dados brutos e os checkpoints não acompanharam o notebook.

## Ambiente informado nos outputs
- Python **3.12.3**
- PyTorch **2.15.0+cpu**
- scikit-learn **1.7.2**
- Pré-processador SJTU no commit `61c9788c20ad5052cd5bedc089d1784c504871d2`
- Semente: **42** (células de treinamento, divisão e validação)

## Conferência numérica

| Etapa | Resultado observado | Situação |
| --- | --- | --- |
| COSMOS | 138.624 amostras, 131.693 treino, 6.931 validação | Coerente |
| Pré-processamento | 204 atributos tanto no COSMOS quanto no Challenge | Coerente |
| Pré-treinamento de 8 épocas | MAE COSMOS de 0,051365 dB | Reproduzido nos logs |
| Continuação até 24 épocas | MAE COSMOS de 0,046427 dB | Reproduzido nos logs |
| Continuação até 48 épocas | MAE COSMOS de 0,0456335744 dB | Reproduzido nos logs |
| Challenge CV com 4 folds | 0,8223719 dB (folds 2,215428; 0,152949; 0,441428; 0,188810 dB) | Reproduzido nos logs |
| Ajuste fino | 40 épocas | Concluído nos logs |
| TestGround online | 21.056 observações, 95 saídas por observação | Coerente |
| **MAE TestGround** | **0,124232492 dB** | **Reproduzido nos logs** |
| Auditoria checkpoint | MAE 0,12423249110077061 dB | Compatível |

### TestGround por cenário

| Cenário | Amostras | MAE (dB) |
| --- | ---: | ---: |
| Aging | 4.400 | 0,087264 |
| SHB | 864 | 0,105130 |
| Unseen | 15.792 | 0,135578 |

### Partições de uso (atenção à ordem)

| Partição | Amostras | MAE (dB) |
| --- | ---: | ---: |
| **Private** | 10.528 | **0,120543** |
| **Public** | 10.528 | **0,127922** |

**Correção necessária no relatório anterior:** os valores Public/Private foram escritos na ordem inversa no PDF do relatório. O notebook executado agrupa diretamente os erros conforme `X_test['Usage']`, produzindo os valores desta tabela.

### Auditoria final
- Diferença máxima de atributos após reconstruir o pré-processamento: **0,0**.
- Diferença máxima entre previsões recalculadas e salvas: **2,783975805442651 × 10⁻⁶ dB** (abaixo do limite de 10⁻⁴ dB definido no código).
- Checkpoint SHA-256 informado pela execução: `4508945eb8372a3c2eb882156bc947a11625ae3e2a3c35d17173d163349b9bcd`.
- Commit do pré-processamento informado nos outputs: `61c9788c20ad5052cd5bedc089d1784c504871d2`.

O SHA-256 é o identificador do checkpoint gerado nesta execução e não constitui, por si só, prova de identidade bit a bit com um checkpoint anterior cujo hash não tenha sido comparado.

## Interpretação e limitações
A validação cruzada no Challenge tem MAE global muito superior ao da avaliação retrospectiva no TestGround; o fold 0 concentrou casos extremos e apresenta MAE de 2,215428 dB. Portanto, **não reduzir a análise de generalização ao resultado 0,124232492 dB**.

O TestGround online foi consultado durante a exploração dos modelos, logo não é uma avaliação independente definitiva. O atributo `EDFA_output_power_total` é utilizado como entrada e restringe a interpretação para cenários em que essa medida estaria disponível.

## Ajustes de documentação recomendados
1. No relatório PDF, corrigir a ordem Public/Private.
2. No notebook, remover comentários antigos que mencionam comparação com ensemble ou com checkpoint de 24 épocas onde o código só executa a MLP de 48 épocas; são comentários residuais, **não dependências executadas**.
3. Registrar todas as versões de dependências e, idealmente, arquivar os índices COSMOS, checkpoints e manifestos de validação para novos reprodutores.
