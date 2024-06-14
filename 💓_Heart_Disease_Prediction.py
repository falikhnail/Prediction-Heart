import streamlit as st
import numpy as np
from catboost import CatBoostClassifier

# Konfigurasi judul dan icon page
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="💓"
)

# Fungsi untuk load model catboost
def load_model():
    model = CatBoostClassifier()
    model.load_model('catboost_model_heart_disease.cbm')
    return model

model = load_model()

# Menampilkan halaman prediksi
def show_predict():
    st.title('💓 Heart Disease Prediction')

    with st.form("user_input"):
        st.info('📢 Untuk keperluan demo, nilai data input akan digenerate secara random jika tidak diisi. Tujuannya supaya memudahkan jika ingin mencoba-coba sistem prediksi ini.')

        rand_age = np.random.randint(27, 77)
        age = st.select_slider('Berapa umur Anda?', options=[i for i in range(1, 126)], value=rand_age, help='Bertambahnya umur meningkatkan risiko penyakit jantung.')

        rand_sex = np.random.randint(0, 2)
        sex = st.selectbox('Apa jenis kelamin Anda?', ("Laki-laki", "Perempuan"), index=rand_sex, help='Laki-laki lebih rawan menderita penyakit jantung.')
        if sex == 'Laki-laki':
            sex = 1
        elif sex == 'Perempuan':
            sex = 2

        rand_chestpain = np.random.randint(0, 4)
        chestpain = st.selectbox('Apa jenis nyeri dada yang Anda rasakan?', ("Asymptomatic", "Non-anginal Pain", "Atypical Angina", "Typical Angina"), index=rand_chestpain, help='Diskusikan gejala nyeri dada yang Anda rasakan dengan dokter.')
        if chestpain == 'Asymptomatic':
            chestpain = 1
        elif chestpain == 'Non-anginal Pain':
            chestpain = 2
        elif chestpain == 'Atypical Angina':
            chestpain = 3
        elif chestpain == 'Typical Angina':
            chestpain = 4
        
        rand_restingbp = np.random.randint(90, 180)
        restingbp = st.select_slider('Berapa tekanan darah Anda dalam satuan mmHg?', options=[i for i in range(90, 181)], value=rand_restingbp, help='Tekanan darah yang tinggi menyebabkan jantung bekerja keras memompa darah ke seluruh tubuh.')

        rand_cholesterol = np.random.randint(145, 360)
        cholesterol = st.select_slider('Berapa total kolestrol Anda dalam satuan mg/dl?', options=[i for i in range(145, 361)], value=rand_cholesterol, help='Kolesterol tinggi menyebabkan penumpukan lemak di dinding arteri')

        rand_fastingbs = np.random.randint(0, 2)
        fastingbs = st.selectbox('Berapa kadar gula darah Anda?', ("Di bawah 120mg/dL", "Di atas 120mg/dL"), index=rand_fastingbs, help='Kadar gula darah yang tinggi menyebabkan rusaknya pembuluh darah dan jantung.')
        if fastingbs == 'Di bawah 120mg/dL':
            fastingbs = 0
        elif fastingbs == 'Di atas 120mg/dL':
            fastingbs = 1

        rand_restingecg = np.random.randint(0, 3)
        restingecg = st.selectbox('Apa hasil tes resting electrocardiogram Anda?', ("Normal", "Penebalan Dinding Ventrikel Kiri", "Segmen ST Abnormal"), index=rand_restingecg, help='Lakukan tes electrocardiogram di laboratorium untuk mendapatkan hasilnya')
        if restingecg == 'Normal':
            restingecg = 0
        elif restingecg == 'Penebalan Dinding Ventrikel Kiri':
            restingecg = 1
        elif restingecg == 'Segmen ST Abnormal':
            restingecg = 2

        rand_maxhr = np.random.randint(60, 201)
        maxhr = st.select_slider('Berapa denyut jantung maksimal Anda dalam satu menit', options=[i for i in range(60, 201)], value=rand_maxhr, help='Jantung yang bermasalah memiliki denyut jantung yang cenderung lambat.')

        rand_exerciseangina = np.random.randint(0, 2)
        exerciseangina = st.selectbox('Apakah Anda merasakan nyeri dada saat berolahraga?', ("Iya", "Tidak"), index=rand_exerciseangina, help='Nyeri dada setelah berolahraga menunjukkan bahwa pasokan darah ke otot jantung tidak cukup atau terganggu.')
        if exerciseangina == 'Iya':
            exerciseangina = 1
        elif exerciseangina == 'Tidak':
            exerciseangina = 0

        rand_oldpeak = np.random.randint(0, 7)
        oldpeak = st.select_slider('Berapa tingkat depresi segmen ST Anda?', options=[i for i in range(0, 7)], value=rand_oldpeak, help="Silakan lakukan tes di laboratorium menggunakan alat EKG (Elektrokardiogram) untuk mengetahui tingkat depresi segmen ST Anda.")

        rand_st_slope = np.random.randint(0, 3)
        st_slope = st.selectbox('Bagaimana kemiringan segmen ST Anda?', ("Upsloping", "Flat", "Downsloping"), index=rand_st_slope, help='Ukur kemiringan segmen ST menggunakan alat EKG (Elektrokardiogram) yang biasa dimiliki laboratorium.')
        if st_slope == 'Upsloping':
            st_slope = 1
        elif st_slope == 'Flat':
            st_slope = 2
        elif st_slope == 'Downsloping':
            st_slope = 3

        ok = st.form_submit_button("Predict")
        if ok:
            X = np.array([[age, sex, chestpain, restingbp, cholesterol, fastingbs, restingecg, maxhr, exerciseangina, oldpeak, st_slope]])
            pred = model.predict(X)
            proba = model.predict_proba(X)[0]
            confidence = max(proba) * 100
            if pred == 0:
                font_color = 'green'
                st.markdown(f"<h3>You <span style='color: {font_color}'>do not have a heart disease</span></h3>", unsafe_allow_html=True)
            if pred == 1:
                font_color = 'red'
                st.markdown(f"<h3>You <span style='color: {font_color}'>have a heart disease</span></h3>", unsafe_allow_html=True)
                
            st.markdown(f"<h4>Confidence: <span style='color: {font_color}'>{confidence:.2f}%</span></h4>", unsafe_allow_html=True)

show_predict()