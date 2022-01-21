import numpy as np
import pandas as pd
import statistics
import click


@click.command()
@click.option('--input', '-i', required=True,
              help='Path to file(.csv) to be processed',
              type=click.Path(exists=True, dir_okay=False, readable=True), )
@click.option('--header', '-1', default=None,
              help='Replace header with first row? "False" to leave as is',
              type=click.Path(dir_okay=False), )
@click.option('--output', '-o', default="output.html",
              help='Path to file to store result in markdown, html or xlsx',
              type=click.Path(dir_okay=False), )
def df_informer(input, output, header):
    path = input
    file = open(path, 'r')
    switch = header
    if header != switch:
        switch = 1

    df = pd.read_csv(file, header=switch)

    cat = df.select_dtypes('object').columns.tolist()
    beginning = [('Metric name', 'Metric stats')]
    df_out = pd.DataFrame(beginning, columns=['Metric', 'Values'],
                          index=[])

    for (column, values) in df.items():
        if column not in cat:
            tile = np.percentile(values, 75) - np.percentile(values, 25)
            list_of_num_series = [pd.Series(['Numerical Column Name:', column], index=df_out.columns),
                                  pd.Series(['Column type:', values.dtype], index=df_out.columns),
                                  pd.Series(['Min:', values.min()], index=df_out.columns),
                                  pd.Series(['Max:', values.max()], index=df_out.columns),
                                  pd.Series(['Mean:', values.mean()], index=df_out.columns),
                                  pd.Series(['Median:', values.median()], index=df_out.columns),
                                  pd.Series(['Mode:', values.mode()[0]], index=df_out.columns),
                                  pd.Series(['Percent of Zero rows:', values[values == 0].count() / len(values)],
                                            index=df_out.columns),
                                  pd.Series(['Variance:', statistics.variance(values)], index=df_out.columns),
                                  pd.Series(['Std Deviation (SqRoot of Variance):', statistics.stdev(values)],
                                            index=df_out.columns),
                                  pd.Series(['Interquartile range:', tile], index=df_out.columns),
                                  pd.Series(
                                      ['Coefficient of Variation (CV):', statistics.stdev(values) / values.mean()],
                                      index=df_out.columns),
                                  pd.Series(['Distinct values number:', len(set(values))], index=df_out.columns),
                                  pd.Series(['Distinct values:', list(set(values))], index=df_out.columns),
                                  ]
            df_out = df_out.append(list_of_num_series, ignore_index=True)
        else:
            list_of_cat_series = [pd.Series(['Categorical Column Name:', column], index=df_out.columns),
                                  pd.Series(['Distinct values number:', len(set(values))], index=df_out.columns),
                                  pd.Series(['Distinct values:', list(set(values))], index=df_out.columns),
                                  pd.Series(['Column type:', values.dtype], index=df_out.columns),
                                  ]
            df_out = df_out.append(list_of_cat_series, ignore_index=True)

    if output.split(".")[-1] == "html":
        f = open(output, 'w')
        result = df_out.to_html()
        f.write(result)
        f.close()
    elif output.split(".")[-1] == "md":
        f = open('output.md', 'w')
        result = df_out.to_markdown()
        f.write(result)
        f.close()
    else:
        df_out.to_excel('output1.xlsx', engine='xlsxwriter')


if __name__ == "__main__":
    df_informer()
