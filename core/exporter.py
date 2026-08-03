import pandas as pd
import io

def export_data(df, format='csv'):
    buffer = io.BytesIO()
    if format == 'csv':
        df.to_csv(buffer, index=False)
        mime = 'text/csv'
    elif format == 'excel':
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif format == 'json':
        buffer.write(df.to_json(orient='records').encode())
        mime = 'application/json'
    buffer.seek(0)
    return buffer, mime