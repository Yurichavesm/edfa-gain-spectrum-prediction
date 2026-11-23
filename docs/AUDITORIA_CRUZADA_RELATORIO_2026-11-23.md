# Auditoria cruzada — Relatório EDFA × notebook essencial × figuras (23/11/2026)

## Fontes inspecionadas
- PDF entregue: `Relatório_estudo_dirigido(1).pdf`, **15 páginas**.
- Notebook executado: `01_pipeline_mlp_essencial_executado.ipynb`, contendo os outputs de treino, CV, ajuste fino e auditoria.
- Notebook publicado: `notebooks/01_pipeline_mlp_essencial.ipynb`, atualizado com seis células de figuras após a auditoria do modelo.
- Gerador publicado: `scripts/gerar_figuras.py`.

## Três conferências realizadas
1. **Números:** comparar resumo, Tabelas 1 a 3 e afirmações numéricas do PDF com logs do notebook executado.
2. **Código:** conferir dimensões, fórmulas, origem dos históricos/CSV, correspondência das seis figuras e preservação das nove células originais do pipeline.
3. **Figuras e legibilidade:** inspecionar visualmente os gráficos/legendas no PDF e executar teste de geração PNG/PDF do gerador com dados artificiais apenas para verificar sua operação. Este teste de código não substitui a execução das figuras com os dados OFC no Databricks.

## Resultados de acordo
- COSMOS: **138.624** observações, treino **131.693** e validação **6.931**.
- Challenge Train: **490** registros; TestGround online: **21.056** registros.
- MLP: **204** entradas → 256 → 256 → 128 → **95** saídas residuais; GELU, dropout 0,10, Smooth L1 com beta 0,25, AdamW.
- Pré-treinamento de 8/24/48 épocas: MAE COSMOS **0,051365 / 0,046427 / 0,045634 dB**.
- Ajuste fino de **40** épocas. MAE TestGround online por observação: **0,124232492 dB**; por canal WSS ativo: **0,106953 dB**.
- TestGround por cenário: Aging **4.400 / 0,087264 dB**, SHB **864 / 0,105130 dB**, Unseen **15.792 / 0,135578 dB**.
- Validação cruzada Challenge: **0,8223719 dB**, influenciada por observações difíceis em alguns folds.
- Comparação SJTU: valores indicados no PDF vieram dos experimentos anteriores; **o pipeline essencial não executa o modelo público SJTU** e não os comprova isoladamente.

## Correções que o autor deve fazer no PDF

### Prioridade alta
1. **p. 11, texto Public/Private:** o PDF diz “Public e Private ... 0,120543 e 0,127922, respectivamente”. A saída do notebook mostra **Private = 0,120543 dB** e **Public = 0,127922 dB**. Corrigir para: “As partições Public e Private apresentaram MAEs de 0,127922 e 0,120543 dB, respectivamente.”
2. **p. 11, Figura 5:** a legenda menciona “Evolução do MAE na validação COSMOS”, mas a imagem apresenta comparações de ganhos reais/previsões. Corrigir para: **“Figura 5 — Ganhos observados e previstos nos cenários Aging, SHB e Unseen, considerando canais ativos.”**
3. **p. 8, Equação (3):** no PDF, a predição aparece como `G_i = G_i^ref + R_i`, sem símbolos de estimativa. Para distinguir grandezas observadas e previstas, utilizar **`Ĝ_i = G_i^ref + R̂_i`**.
4. **p. 9, Tabela 2:** usa o nome **E7** e modelos Ridge/boosting que foram deliberadamente excluídos do pipeline essencial. Os valores do TestGround para as MLPs de 8 e 24 épocas também não são recalculados pelo notebook principal. Portanto, a tabela histórica **não é integralmente reproduzível a partir do notebook mínimo**. Opções: publicar um suplemento específico de comparação ou mudar a tabela para os três MAEs de validação COSMOS (8/24/48 épocas), que o notebook comprova diretamente. Não confundir métricas COSMOS com métricas TestGround.
5. **p. 10–11, Tabela 3:** os valores SJTU público (Aging 0,068667; SHB 0,068157; Unseen 0,098597; global 0,091094 dB) não são calculados no notebook essencial. Há evidência de experimentos anteriores, mas, para reprodução integral da tabela, é necessário fornecer script/artefatos da comparação SJTU ou descrevê-la como comparação externa previamente realizada.

### Redação e apresentação
6. **p. 2–3, seção 1.1:** repete a introdução quase integralmente. Substituir por objetivo geral e objetivos específicos, evitando duplicação.
7. **p. 9, seção 4.1:** o PDF cita 17 registros Challenge com potência de saída -50 e 10 SHB concentrados em um fold; estes números não são produzidos pelo notebook mínimo. Acompanhar com a rotina/fonte do levantamento caso se exija reprodutibilidade dessa estatística.
8. **p. 15:** o PDF tem **15 páginas**, ultrapassando o limite de 12 páginas mencionado anteriormente no estudo. Confirmar se esse limite permanece válido antes da entrega.
9. **p. 7:** “Embora os autores empregam” → “Embora os autores empreguem”.

## Verificação das figuras
| Figura | Natureza | Fonte efetiva | Situação |
| --- | --- | --- | --- |
| 1 | Diagrama EDFA | Código Matplotlib, elaboração própria | Código incluído e testado |
| 2 | Fluxograma COSMOS/Challenge/TestGround | Código Matplotlib, elaboração própria | Código incluído e testado |
| 3 | MLP 204→256→256→128→95 | Código Matplotlib e estrutura do notebook | Conferida com a rede |
| 4 | Histórico MAE COSMOS 1–48 | `historico_mlp_v2.csv`, `historico_pretrain_extended.csv`, `historico_pretrain_48ep.csv` | Arquivos gerados pelo pipeline; verificados nomes/colunas e testada renderização |
| 5 | Observado × previsto por cenário | Labels TestGround, máscara WSS e `predicoes_mlp_v2_48ep_testground.csv` | Seleção determinística próxima à mediana, canais ativos apenas; valida MAEs antes de plotar |
| 6 | Boxplot MAE por cenário | Mesmas observações da Figura 5 | Escala log, whiskers P5–P95, outliers visíveis; média por cenário recalculada |

As figuras foram acrescentadas ao notebook **depois da auditoria final**; as nove células de treino/validação/auditoria não foram alteradas. As novas células **ainda não têm outputs Databricks com os dados oficiais**, porque o ambiente remoto e os dados não foram executados nesta auditoria. Ao rodá-las no Databricks, o script salva PNG e PDF no Volume e exibe as imagens na interface. Os arquivos PNG/PDF são gerados inicialmente no disco local e depois copiados para o Volume, reduzindo o risco de erro `Errno 5`.

## Limitações científicas importantes
- O TestGround online foi consultado durante o desenvolvimento e **não constitui teste independente de generalização futura**.
- `EDFA_output_power_total` é entrada do modelo e sua disponibilidade é uma condição de aplicação prática.
- Reproduzir a inferência do checkpoint não garante identidade bit a bit de um novo treinamento em ambiente/hardware diferente.