# Predição do espectro de ganho em EDFAs — pipeline essencial

Repositório preparado a partir dos notebooks do estudo dirigido OFC 2026. **Somente os componentes da MLP residual final** estão incluídos: preprocessor SJTU (commit fixado), divisão COSMOS, pré-treinamento em etapas (8, 24, 48 épocas), validação cruzada agrupada, ajuste fino Challenge, avaliação TestGround e auditoria. Não há experimentos descartados com FFT, Ridge, CatBoost, GPR, CNN ou ensembles.

**Notebook principal:** `notebooks/01_pipeline_mlp_essencial.ipynb`. Execute as células sequencialmente no Databricks. Requer dados oficiais acessíveis em `/Volumes/workspace/default/ofc2026`.

**Resultado de referência:** MAE médio por observação 0,124232492 dB nas 21.056 observações do TestGround online, somente nos canais WSS ativos. Esta medida é retrospectiva e não equivale à pontuação oficial da final. O TestGround foi consultado durante desenvolvimento experimental.

**Dependências:** Python, numpy, pandas, torch, scikit-learn, matplotlib para figuras. O pré-processamento utiliza código original dos autores SJTU, `https://github.com/kayneZhu/ofc_ml`, commit `61c9788c20ad5052cd5bedc089d1784c504871d2`. A arquitetura MLP e protocolo residual pertencem a este estudo.

**Validação de execução (23/11/2026):** o autor enviou o notebook filtrado após execução no Databricks com os dados oficiais. A análise dos outputs confirmou o treinamento em etapas, o ajuste fino, o MAE TestGround de **0,124232492 dB** e a auditoria do checkpoint. As nove células originais de código correspondem às publicadas aqui; foi acrescentada uma célula de instalação de PyTorch. Veja [o registro de validação](docs/VALIDACAO_EXECUCAO_2026-11-23.md). Esta conferência foi realizada sobre os outputs enviados, **sem uma reexecução independente em outro ambiente**. Checkpoints podem não reproduzir bit a bit entre ambientes distintos.

Os dados estão em `https://github.com/ofc-ml-challenge/ofc-ml-challenge-data-code`.

**Exportação:** `scripts/exportar_artefatos_databricks_corrigido.py` deve ser colado em uma única célula de um notebook Python no Databricks. O ZIP é criado em disco local antes de ser copiado para o Volume. Não executar esse exportador antes de gerar os artefatos.

**Figuras:** `scripts/gerar_figuras.py` contém os diagramas e visualizações baseadas no histórico e predições; executar após completar o pipeline.