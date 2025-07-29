from datetime import timedelta

def evaluate_slos(df, config):
    results = []
    for svc in config['services']:
        svc_result = {'service': svc['name'], 'slos': []}
        for slo in svc['slos']:
            df_metric = df[df['metric_name'] == slo['metric_name']]
            if slo['type'] == 'ratio':
                success = df_metric[slo['success_col']].sum()
                total = df_metric[slo['total_col']].sum()
                percent = (success / total) * 100 if total > 0 else 0
                compliant = percent >= slo['target']
                svc_result['slos'].append({
                    'name': slo['name'],
                    'actual': round(percent, 2),
                    'target': slo['target'],
                    'compliant': compliant,
                    'data': df_metric
                })
            elif slo['type'] == 'threshold':
                within_threshold = df_metric[df_metric[slo['value_col']] <= slo['threshold_ms']]
                percent = (len(within_threshold) / len(df_metric)) * 100 if len(df_metric) > 0 else 0
                compliant = percent >= slo['target']
                svc_result['slos'].append({
                    'name': slo['name'],
                    'actual': round(percent, 2),
                    'target': slo['target'],
                    'compliant': compliant,
                    'data': df_metric
                })
        results.append(svc_result)
    return results
