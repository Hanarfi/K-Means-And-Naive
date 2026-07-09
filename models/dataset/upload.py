# ==========================================
# BACA FILE EXCEL
# ==========================================

def baca_excel(file):

    try:

        df = pd.read_excel(file)

        return True, df

    except Exception as e:

        return False, str(e)

# ==========================================
# VALIDASI DATASET
# ==========================================

def validasi_dataset(df):

    kolom_error = validasi_kolom(df)

    if len(kolom_error) > 0:

        return False, kolom_error

    return True, None

