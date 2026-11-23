# Auditoria cruzada — relatório versão 5 e notebook executado (23/11/2026)

## Materiais
- PDF fornecido pelo autor: `Relatório_estudo_dirigido (5).pdf`, 16 páginas.
- Notebook exportado do Databricks: `01_pipeline_mlp_essencial (2) (2).ipynb`, publicado sem alterar seus outputs em [notebook executado](../notebooks/01_pipeline_mlp_essencial_executado_com_outputs.ipynb).
- Notebook de reprodução publicado no GitHub: [pipeline essencial](../notebooks/01_pipeline_mlp_essencial.ipynb).

## Três verificações cruzadas
1. **Outputs e código:** o notebook exportado tem 36 células, das quais 18 células de código possuem saídas, incluindo seis imagens PNG de gráficos e diagramas; nenhum output de exceção. A célula de validação confirma seis PNGs e seis PDFs no Volume, 21.056 observações, 262.144 canais WSS ativos e métricas dentro da tolerância.
2. **Comparação com o GitHub:** 16 dos 17 blocos do código do pipeline (excluída a célula adicional de instalação PyTorch) são literalmente idênticos à versão publicada. **A única diferença está na função que desenha a Figura 2:** a versão do GitHub contém o fluxo de transferência de pesos e TestGround correto; o notebook executado documenta uma versão anterior do diagrama. A alteração não atinge os cálculos da MLP.
3. **PDF contra outputs:** verificadas as Tabelas 1, 2, 3, as seis imagens, estrutura 204 → 256 → 256 → 128 → 95, 48 épocas de pré-treino, 40 de ajuste fino, Smooth L1 beta 0,25, AdamW, dropout 10%, quatro folds e as métricas reportadas. O PDF distingue avaliação local no TestGround de pontuação oficial OFC e informa as limitações do uso repetido do TestGround e da variável `EDFA_output_power_total`.

## Resultados numéricos

| Etapa | Saída Databricks | Relatório | Parecer |
|---|---:|---:|---|
| COSMOS | 138.624 registros, 131.693 treino + 6.931 validação | 138.624 | Consistente |
| Challenge Train | 490 | 490 | Consistente |
| TestGround online | 21.056 | 21.056 | Consistente |
| Pré-treino 8 épocas | 0,051365 | 0,051365 | Consistente |
| Pré-treino 24 épocas | 0,046427 | 0,046427 | Consistente |
| Pré-treino 48 épocas | 0,045634 | 0,045634 | Consistente |
| MAE CV Challenge | 0,8223719 | 0,822372 | Consistente |
| MAE TestGround por observação | 0,124232492 | 0,124232 | Consistente |
| MAE TestGround por canal ativo | 0,106953 | 0,106953 | Consistente |
| Aging | 0,087264 no treino; 0,087263 em CSV da figura/validação | 0,087264 | Variação ~0,000001 dB entre as saídas; abaixo da tolerância, não altera a conclusão |
| SHB | 0,105130 | 0,105130 | Consistente |
| Unseen | 0,135578 | 0,135578 | Consistente |
| Public | 0,127922 | 0,127922 | Consistente |
| Private | 0,120543 | 0,120543 | Consistente |

A auditoria do checkpoint reportou diferença máxima no pré-processamento igual a **0**, diferença máxima de predições **2,783975805442651×10⁻⁶ dB** e MAE recalculado de **0,12423249110077061 dB**, compatível com o valor do relatório.

## Pontos a corrigir/registrar no PDF
1. **Página 8, seção 3.3:** o título `3.3 - Métrica e rastreabilidade` aparece **duplicado consecutivamente**. Remover uma ocorrência. É um erro de edição, não técnico.
2. **Página 10, seção 4.1:** o relatório escreve `potência total de saída igual a -50 dB`. O código verifica **o valor numérico −50 do atributo `EDFA_output_power_total`** sem estabelecer explicitamente a unidade. Para evitar atribuição de unidade não demonstrada, substituir por `valor igual a −50 no atributo EDFA_output_power_total` (ou verificar a unidade original no dicionário de dados antes de indicar dBm). Esses 17 registros (10 SHB e 7 Unseen) e concentração SHB no fold 0 foram constatados nos experimentos anteriores.
3. **Página 7, Equação (3):** falta distinguir previsão de valor observado com chapéus `\hat G_i = G_i^{ref}+\hat R_i`. O autor decidiu **não corrigir neste momento**; não alterar unilateralmente.
4. **Figura 2:** o relatório utiliza o fluxo **corrigido** em que COSMOS → pré-treinamento → checkpoint + Challenge → ajuste fino → MLP final → TestGround. O notebook executado anexado ainda gera o desenho **anterior**. Preservado como registro fiel da execução; o notebook principal do GitHub contém a função corrigida.

## Limites das verificações
- Revisão de texto, código e outputs fornecidos; não houve treinamento independente novo nem acesso direto ao Volume do Databricks.
- A produção dos seis gráficos e respectivos arquivos é comprovada pelos outputs; seus pixels foram inspecionados, mas figuras geradas sob outra sessão e outros dados exigiriam nova conferência.
- TestGround foi consultado durante o desenvolvimento, portanto não deve ser descrito como conjunto de teste final independente.
- Reprodutibilidade integral em ambiente externo depende também dos dados oficiais, índices originais e checkpoints arquivados.

**Conclusão:** não foram encontrados desvios numéricos materiais entre as métricas da MLP e o relatório. As divergências restantes são a unidade atribuída ao valor −50, o título 3.3 duplicado, a Equação (3) deixada intencionalmente pendente e a versão anterior do desenho da Figura 2 no notebook executado (sem efeito nos resultados).
