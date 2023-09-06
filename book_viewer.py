import streamlit as st
import pandas as pd
import locale


def load_excel_data(file_path):
    df = pd.read_excel(file_path)
    return df


def format_indian_number(number):
    # Set the locale to India
    locale.setlocale(locale.LC_ALL, 'en_IN')
    formatted_amount = locale.format_string('%d', number, grouping=True)
    return formatted_amount


def main():
    # Set page layout to full width
    st.set_page_config(layout="wide")

    st.title("ഓഡിറ്റ് ബുക്ക്")

    excel_file = 'red_book.xlsx'
    df = pd.read_excel(excel_file)

    col1, col2 = st.columns([1, 4])
    table_width = 1000

    with col1:
        column_to_sum = "തുക"
        st.write("##### ഡാറ്റ ഫിൽറ്ററേഷൻ")
        amount_values = ["", 500, 1000, 2000, 5000, 10000, 15000, 20000, 25000]
        selected_amount = st.selectbox("തുക നൽകുക:", amount_values)
        st.write("##### ഡാറ്റ തിരയുക")
        search_term = st.text_input("തിരയൽ പദം നൽകുക:")

    with col2:
        selected_amount = selected_amount if selected_amount else 0
        df = df.iloc[:, :4]
        if search_term:
            search_term = str(search_term)
            filtered_df = df[
                df.apply(lambda row: any(search_term.lower() in str(cell).lower() for cell in row), axis=1)]
            result_heading = "### തിരയൽ ഫലം"
        else:
            filtered_df = df
            result_heading = "### മുഴുവൻ ലിസ്റ്റ്"
        filtered_by_amount = filtered_df[(filtered_df[column_to_sum] >= selected_amount)]
        total_amount = (filtered_by_amount[column_to_sum].sum()
                        if selected_amount else filtered_df[column_to_sum].sum())
        col1, col2, col3 = st.columns([1, 1.25, 1])
        with col1:
            st.write(result_heading)
        with col3:
            st.write(f"###### മൊത്തം തുക: ₹{format_indian_number(total_amount)}")
        st.dataframe(filtered_by_amount, width=table_width, hide_index=True)


if __name__ == "__main__":
    main()
