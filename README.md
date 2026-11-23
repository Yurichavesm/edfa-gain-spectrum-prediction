# Predição do espectro de ganho em EDFAs — pipeline essencial

Repositório preparado a partir dos notebooks do estudo dirigido OFC 2026. **Somente os componentes da MLP residual final** estão incluídos: preprocessor SJTU (commit fixado), divisão COSMOS, pré-treinamento em etapas (8, 24, 48 épocas), validação cruzada agrupada, ajuste fino Challenge, avaliação TestGround e auditoria. Não há experimentos descartados com FFT, Ridge, CatBoost, GPR, CNN ou ensembles.

**Notebook principal:** `notebooks/01_pipeline_mlp_essencial.ipynb`. Execute as células sequencialmente no Databricks. Requer dados oficiais acessíveis em `/Volumes/workspace/default/ofc2026`.

**Resultado de referência:** MAE médio por observação 0,124232492 dB nas 21.056 observações do TestGround online, somente nos canais WSS ativos. Esta medida é retrospectiva e não equivale à pontuação oficial da final. O TestGround foi consultado durante desenvolvimento experimental.

**Dependências:** Python, numpy, pandas, torch, scikit-learn, matplotlib para figuras. O pré-processamento utiliza código original dos autores SJTU, `https://github.com/kayneZhu/ofc_ml`, commit `61c9788c20ad5052cd5bedc089d1784c504871d2`. A arquitetura MLP e protocolo residual pertencem a este estudo.

**Ressalva:** o notebook filtrado foi reconstruído a partir das células originais e verificado sintaticamente, mas não foi reexecutado no Databricks com os datasets oficiais. Para validar a reprodutibilidade integral, é necessário realizar essa execução limpa e comparar os checkpoints, as métricas e o ambiente de software. Os checkpoints podem não reproduzir bit a bit em ambientes distintos.

Os dados estão em `https://github.com/ofc-ml-challenge/ofc-ml-challenge-data-code`.

**Exportação:** `scripts/exportar_artefatos_databricks_corrigido.py` deve ser colado em uma única célula de um notebook Python no Databricks. O ZIP é criado em disco local antes de ser copiado para o Volume. Não executar esse exportador antes de gerar os artefatos.

**Figuras:** `scripts/gerar_figuras.py` contém os diagramas e visualizações baseadas no histórico e predições; executar após completar o pipeline.