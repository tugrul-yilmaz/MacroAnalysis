import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from libs.dataStructure import DataManagement
from libs.utils import rolling_mean
##
def main():
    st.title("Veri Yönetimi ve Görselleştirme")

    try:
        data_manager = DataManagement()
    except Exception as e:
        st.error(f"DataManagement sınıfı başlatılamadı: {e}")
        return

    selected_data = st.multiselect(
        "Bir veya birden fazla veri seti seçin:",
        options=data_manager.get_data_names()
    )

    if not selected_data:
        st.warning("Lütfen en az bir veri seti seçin!")
        return

    combined_data = pd.DataFrame()

    for data_name in selected_data:
        df = data_manager.read_data(data_name)

        if "observation_date" in df.columns:
            df["observation_date"] = pd.to_datetime(df["observation_date"])
            df.set_index("observation_date", inplace=True)

        if combined_data.empty:
            combined_data = df
        else:
            combined_data = combined_data.join(df, how="outer", rsuffix=f"_{data_name}")

    combined_data.sort_index(inplace=True)


    numeric_cols = combined_data.select_dtypes(include=["float", "int"]).columns

    if numeric_cols.empty:
        st.warning("Seçilen veri setinde görselleştirilebilecek sayısal sütunlar bulunamadı!")
        return


    if st.button("Birleştirilmiş Veriyi Göster"):
        st.subheader("Birleştirilmiş Veri")
        st.line_chart(combined_data[numeric_cols])


    window_size = st.slider("Rolling Mean Pencere Boyutu", min_value=1, max_value=30, value=3)
    if st.button("Rolling Mean"):
        st.subheader("Rolling Mean")
        rolling_df = rolling_mean(combined_data, numeric_cols, window_size)


        fig = go.Figure()

        for col in rolling_df.columns:
            if "average" in col:
                fig.add_trace(
                    go.Scatter(
                        x=rolling_df.index,
                        y=rolling_df[col],
                        mode="lines",
                        name=col,
                        line=dict(dash="dash")
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=rolling_df.index,
                        y=rolling_df[col],
                        mode="lines",
                        name=col,
                        line=dict(dash="solid")
                    )
                )

        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
