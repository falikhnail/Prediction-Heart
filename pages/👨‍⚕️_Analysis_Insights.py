import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Heart Disease Analysis Insights",
    page_icon="👨‍⚕️"
)

def sql_engine():
    postgres_credential = st.secrets["postgres_credential"]
    return create_engine(postgres_credential)

@st.cache_data
def load_data():
    db_engine = sql_engine()
    df = pd.read_sql('SELECT * FROM spktable', db_engine)
    df['HeartDisease'] = df['HeartDisease'].replace({0:'No', 1:'Yes'})
    df = df.loc[(df['Cholesterol'] > 50) & (df['Cholesterol'] < 350)]
    df = df.loc[(df['RestingBP'] > 90) & (df['RestingBP'] < 180)]
    df = df.loc[df['Oldpeak'] >= 0]

    return df

df = load_data()

def show_insight():
    st.title('👨‍⚕️ Heart Disease Insights')

    yes_color = '#f22c2c'
    no_color = '#027302'


    st.markdown("### **1. Umur berapa yang rawan menderita penyakit jantung?**")
    # Lakukan binning untuk age
    bins = [20, 30, 40, 50, 60, 70]
    labels = ['21-30', '31-40', '41-50', '51-60', '61-70']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    plt.figure(figsize=(9, 5))
    ax = sns.countplot(data=df, x='Age Group', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    # Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.title('Heart Disease Berdasarkan Umur')
    st.pyplot(plt)
    st.write('Tampak bahwa umur 51 tahun ke atas cukup rawan terkena penyakit jantung. Semakin bertambahnya umur, manusia harus semakin menjaga pola hidupnya karena peluang terkena penyakit jantung semakin besar.')
    st.write('Hal tersebut masuk akal karena semakin bertambahnya usia, maka pembuluh darah cenderung mengalami penumpukan plak aterosklerotik (plak lemak) yang dapat menyebabkan penyempitan atau penyumbatan pembuluh darah koroner yang memasok darah ke jantung. Hal ini juga dapat meningkatkan risiko terjadinya penyakit jantung.')
    



    st.markdown("### **2. Berapa batas maximum heart rate yang rawan penyakit jantung?**")
    plt.figure(figsize=(10, 5))
    ax = sns.histplot(data=df, x='MaxHR', hue='HeartDisease', palette={'Yes': 'red', 'No': no_color})

    plt.title('Heart Disease Berdasarkan Maximum Heart Rate')
    st.pyplot(plt)
    st.write('Terlihat jelas bahwa sebagian besar orang yang menderita penyakit jantung memiliki maximum heart rate di bawah 130.')
    st.write('Jantung memiliki sistem listrik internal yang mengatur ritme dan frekuensi detak jantung. Gangguan pada sistem ini dapat menyebabkan detak jantung yang terlalu lambat.')
    st.write('Hal tersebut menjadi alasan mengapa kebanyakan penderita penyakit jantung memiliki detak jantung yang cukup rendah.')




    st.markdown("### **3. Apa jenis kelamin yang rawan terhadap penyakit jantung?**")
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='Sex', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')
            
    ax.set_xticklabels(['Male', 'Female'])

    plt.title('Heart Disease Berdasarkan Jenis Kelamin')
    st.pyplot(plt)
    st.write('Laki-laki lebih rawan menderita penyakit jantung. Tampak ada perbedaan yang sangat signifikan mengenai penderita penyakit jantung berdasarkan jenis kelaminnya.')
    st.write('Alasannya karena perempuan memiliki hormon estrogen yang diyakini memiliki efek pelindung dari penyakit jantung.')




    st.markdown("### **4. Jenis sakit dada apa yang rawan memicu penyakit jantung?**")
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='ChestPainType', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    #  Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.title('Heart Disease Berdasarkan Tipe Chest Pain')
    st.pyplot(plt)
    st.write('Keterangan: ATA = Atypical Angina, NAP = Non-anginal Pain, AS = Asymptomatic, TA = Typical Angina')
    st.write('Chestpain asymptomatic adalah jenis sakit dada yang paling mengindikasikan adanya penyakit jantung. Tampak perbedaan yang sangat signifikan dengan jenis sakit dada yang lain.')
    st.write('Hal tersebut karena chestpain asymptomatic terjadi tanpa gejala sehinnga seringkali diabaikan oleh penderitanya. Ketika diabaikan, maka dapat semakin parah dan berujung pada penyakit jantung.')




    st.markdown("### **5. Apakah besar tekanan darah dapat mengindikasikan penyakit jantung?**")
    df['RestingBP'].replace(0, df['RestingBP'].median(),inplace=True)
    plt.figure(figsize=(10, 5))
    ax = sns.histplot(data=df, x='RestingBP', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    plt.title('Heart Disease Berdasarkan Tekanan Darah')
    plt.xlabel('Tekanan Darah (mmHg)')
    st.pyplot(plt)
    st.write('Ya, tekanan darah di atas 130 mmHg dapat menjadi indikasi bahwa seseorang menderita penyakit jantung.')
    st.write('Alasannya karena tekanan darah yang tinggi akan menyebabkan jantung harus bekerja keras dalam memompa darah ke seluruh tubuh. Selain itu, tekanan darah yang tinggi juga merusak pembuluh darah koroner yang memasok darah ke jantung sehingga meningkatkan resiko penumpukan plak lemak dan dampaknya juga mengakibatkan penyakit jantung.')




    st.markdown("### **6. Berapa tingkat kolesterol yang rawan memicu penyakit jantung?**")
    # Lakukan binning untuk kolesterol
    bins = [100, 150, 200, 250, 300, 350]
    labels = ['101-150', '151-200', '201-250', '251-300', '301-350']
    df['Cholesterol Group'] = pd.cut(df['Cholesterol'], bins=bins, labels=labels, right=False)

    plt.figure(figsize=(10, 5))
    ax = sns.countplot(data=df, x='Cholesterol Group', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    # Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.xlabel('Retang Total Kolesterol (mg/dL)')

    plt.title('Heart Disease Berdasarkan Tingkat Kolesterol')
    st.pyplot(plt)
    st.write('Tampak bahwa orang dengan tingkat kolesterol di atas 251 mg/dL rawan menderita penyakit jantung.')
    st.write('Alasan: Kolestrol yang tinggi akan menyebabkan penumpukan plak lemak di dinding arteri. Akibatnya plak tersebut akan menyempitkan arteri dan mengurangi aliran darah yang kaya oksigen ke jantung. Hal inilah yang menyebabkan terjadinya penyakit jantung, terutama penyakit jantung koroner.')




    st.markdown("### **7. Apakah kadar gula darah menunjukkan adanya penyakit jantung?**")
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='FastingBS', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    #  Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')
            
    ax.set_xticklabels(['Kurang dari 120 mg/dL', 'Lebih dari 120 mg/dL'])

    plt.xlabel('Kadar Gula Darah')

    plt.title('Heart Disease Berdasarkan Kadar Gula Darah')
    st.pyplot(plt)
    # st.write('Keterangan:')
    # st.write('0 = Kadar gula darah < 120 mg/dL')
    # st.write('1 = Kadar gula darah > 120 mg/dL')
    st.write('Ya. Tampak bahwa sebagian besar orang yang memiliki kadar gula darah di atas 120 mg/dL memiliki penyakit jantung.')
    st.write('Hal tersebut masuk akal karena tingginya kadar gula darah dapat merusak pembuluh darah dan menyebabkan komplikasi penyakit jantung serius. Selain itu, gula darah yang tinggi dapat menyebabkan gangguan pada sistem kardiovaskular, seperti disfungsi otot jantung, aritmia (ketidakaturan detak jantung), dan kerusakan katup jantung.')



    st.markdown("### **8. Bagaimana hasil resting electrocardiogram yang rawan terhadap penyakit jantung?**")
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='RestingECG', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    #  Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.title('Heart Disease Berdasarkan Hasil Resting Electrocardiogram ')
    st.pyplot(plt)
    st.write('Hasil Resting Electrocardiogram LVH (Left Ventricular Hypertrophy) dan ST abnormal mengindikasikan adanya penyakit jantung.')
    st.write('LVH (Left Ventricular Hypertrophy) adalah kondisi di mana otot ventrikel kiri jantung menebal. Hal ini dapat terjadi sebagai respons terhadap peningkatan tekanan darah (hipertensi) atau karena penyakit jantung lainnya. Selain itu, abnormalitas pada segmen ST, seperti depresi dapat menunjukkan adanya iskemia miokard (kurangnya aliran darah ke jantung). Kondisi inilah yang menjadi tanda adanya penyakit jantung.')



    st.markdown("### **9. Bagaimana tingkat depresi segmen ST (oldpeak) terhadap penyakit jantung?**")
    plt.figure(figsize=(10, 5))
    ax = sns.histplot(data=df, x='Oldpeak', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    plt.title('Heart Disease Berdasarkan Tingkat Depresi Segmen ST')
    plt.xlabel('Tingkat Depresi Segmen ST')
    st.pyplot(plt)
    st.write('Tampak bahwa orang yang memiliki hasil tes depresi segmen ST di atas 1 rawan menderita penyakit jantung.')
    st.write('Dengan kata lain, semakin besar tingkat depresi segmen ST, maka semakin besar pula kemungkinan menderita penyakit jantung.')
    st.write('Hal tersebut terjadi karena depresi segmen ST sering kali menunjukkan adanya iskemia miokard, yaitu kondisi di mana aliran darah ke jantung berkurang. Penyebabnya adalah penyempitan atau penyumbatan arteri koroner yang memasok darah ke jantung.')




    st.markdown("### **10. Apakah nyeri data (angina) akibat olahraga dapat mengindikasikan seseorang menderita penyakit jantung?**")
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='ExerciseAngina', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    #  Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.title('Heart Disease Berdasarkan Angina Akibat Olahraga')
    ax.set_xticklabels(['Tidak', 'Iya'])
    plt.xlabel('Angina')

    st.pyplot(plt)
    st.write('Ya, munculnya angina setelah berolahraga dapat menjadi indikator bahwa seseorang menderita penyakit jantung.')
    st.write('Tampak perbedaan yang sangat signifikan pada grafik di atas bahwa sebagian besar orang yang mengalami angina setelah olahraga ternyata menderita penyakit jantung.')
    st.write('Olahraga meningkatkan kebutuhan oksigen oleh otot jantung. Pada seseorang dengan penyakit arteri koroner atau penyakit jantung, pasokan darah dan oksigen ke otot jantung mungkin tidak mencukupi untuk memenuhi kebutuhan selama olahraga yang intens. Hal ini dapat menyebabkan iskemia miokard (kurangnya pasokan darah dan oksigen ke otot jantung), yang mana gejalanya sering dirasakan sebagai nyeri dada atau angina.')
    st.write('Oleh karena itu, jika seseorang mengalami angina setelah berolahraga, ini dapat menjadi tanda bahwa ada masalah dengan pasokan darah ke otot jantung dan dapat mengindikasikan adanya penyakit jantung. ')





    st.markdown("### **11. Apakah tingkat kemiringan segmen ST dapat mengindikasikan penyakit jantung?**")
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x='ST_Slope', hue='HeartDisease', palette={'Yes': yes_color, 'No': no_color})

    #  Memberi anotasi
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points')

    plt.title('Heart Disease Berdasarkan Kemiringan Segmen ST')
    plt.xlabel('Kemiringan Segmen ST')
    st.pyplot(plt)
    st.write('Ya, kemiringan segmen ST dapat menjadi indikasi apakah seseorang menderita penyakit jantung atau tidak.')
    st.write('Jika hasil tes ST seseorang menunjukkan bahwa segmen ST-nya datar atau menurun, maka orang tersebut diindikasikan menderita penyakit jantung.')
    st.write('Hal tersebut karena segmen ST yang datar atau menurun dapat menjadi tanda bahwa terjadi iskemia miokard, yang terjadi ketika pasokan darah dan oksigen ke otot jantung terganggu. Segmen ST yang datar atau menurun juga dapat terjadi akibat peradangan atau inflamasi pada jantung, seperti pada penyakit pericarditis atau miokarditis. Kondisi ini juga dapat terkait dengan penyakit jantung tertentu.')


    # st.markdown("### **Berapa persentase orang yang menderita penyakit jantung?**")
    # plt.figure(figsize = (5,5))
    # heart_disease_counts = df['HeartDisease'].value_counts()

    # plt.pie(heart_disease_counts, labels=heart_disease_counts.index, autopct='%1.1f%%')

    # plt.title('Heart Disease Distribution')
    # col1, col2 = st.columns([0.3, 0.2])
    # col1.pyplot(plt)
    # st.write('Tampak bahwa distribusi keduanya seimbang sehingga insight yang diambil dari data ini bisa terhindar dari bias (imbalance class).')



    st.markdown("## **⭐ Kesimpulan**")
    st.write('**Ciri-ciri orang yang rawan menderita penyakit jantung:**')
    st.write('1. Laki-laki dan berusia di atas 51 tahun.')
    st.write('2. Detak jantung lemah (di bawah 130 bpm)')
    st.write('3. Memiliki sakit dada asymptomatic')
    st.write('4. Memiliki tekanan darah di atas 130 mm Hg')
    st.write('5. Memiliki kadar gula darah di atas 120 mg/dL')
    st.write('6. Memiliki kolesterol di atas 251 mm/dL')
    st.write('7. Memiliki hasil tes depresi segmen ST (oldpeak) di atas 1')
    st.write('8. Mengalami angina setelah berolahraga')
    st.write('9. Hasil tes kemiringan segmen ST datar atau menurun')

show_insight()