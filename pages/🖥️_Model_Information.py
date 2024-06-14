import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Model Information",
    page_icon="🖥️"
)

def show_model_information():
    st.title('🖥️ Model Information')
    st.write('Saya mencoba 5 model untuk memprediksi penyakit jantung, yaitu:')
    st.write('1. Logistic Regression')
    st.write('2. Gradient Boosting Classifier')
    st.write('3. CatBoost Classifier')
    st.write('4. Naive Bayes')
    st.write('5. XGBoost Classifier')

    st.subheader('📈 Berikut adalah akurasi dari setiap model')

    nama_model = ['Logistic Regression', 'Gradient Boosting', 'CatBoost', 'Naive Bayes', 'XGBoost']
    accTrainArr = [0.8542234332425068, 0.946866485013624, 0.946866485013624, 0.8365122615803815, 0.9373297002724795]
    accTestArr = [0.8913043478260869, 0.8967391304347826, 0.907608695652174, 0.8858695652173914, 0.8804347826086957]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Lebar setiap bar
    bar_width = 0.4

    # Array untuk sumbu x
    x_pos = np.arange(len(nama_model))

    # Plot untuk akurasi train
    train_bars = ax.bar(x_pos, accTrainArr, width=bar_width, align='center', label='Train Accuracy')

    # Plot untuk akurasi test
    test_bars = ax.bar(x_pos + bar_width, accTestArr, width=bar_width, align='center', label='Test Accuracy')

    ax.set_xticks(x_pos + bar_width / 2)
    ax.set_xticklabels(nama_model)

    ax.set_ylabel('Accuracy')

    ax.set_title('Model Accuracy Comparison')

    # Untuk memberikan annotation di setiap puncak bar
    for bar1, bar2 in zip(train_bars, test_bars):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax.annotate(f'{height1:.3f}', xy=(bar1.get_x() + bar1.get_width() / 2, height1),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')
        ax.annotate(f'{height2:.3f}', xy=(bar2.get_x() + bar2.get_width() / 2, height2),
                    xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    ax.set_ylim(0, 1.05)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    st.pyplot(fig)

    st.write('Tampak bahwa model Catboost menghasilkan akurasi tertinggi ketika memprediksi data test. Selain itu, akurasinya pun tidak jauh berbeda dengan akurasi data train.')
    st.write('Hal tersebut menunjukkan bahwa model Catboost tidak overfitting dan tidak underfitting, serta lebih baik dibandingkan model yang lain.')

    st.subheader('😺 Alasan memilih Catboost')

    st.write('Catboost merupakan improvement dari Gradient Boosting yang bekerja dengan cara menggabungkan beberapa decision tree untuk membuat prediksi yang lebih kuat. Setiap pohon akan dibuat sambil memperbaiki kesalahan prediksi pohon sebelumnya. Hal tersebut menyebabkan Catboost dapat menghasilkan akurasi yang cukup tinggi.')

    st.write('Catboost membuat decision tree menggunakan algoritma symmetric binary splitting yang mampu menghasilkan pohon yang seimbang dan simetris sehingga pohon memiliki struktur yang sama pada setiap level. Hal ini mampu mempercepat waktu eksekusinya.')

    st.write('Selain itu, Catboost juga menerapkan ordered boosting untuk menghindari kebocoran data selama pelatihan. Ordered boosting akan mengurutkan data berdasarkan nilai fitur dan membaginya menjadi beberapa bagian supaya informasi dari masa depan tidak digunakan. Hal tersebut mampu mengurangi overfitting.')

    st.write('Berdasarkan berbagai alasan tersebut, saya memilih model Catboost untuk memprediksi data yang diinputkan oleh user.')

show_model_information()