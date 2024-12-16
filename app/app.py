import streamlit as st
import pandas as pd
import torch
import matplotlib.pyplot as plt
import re
from load_model import model, tokenizer
from collections import Counter
from wordcloud import WordCloud
from underthesea import word_tokenize


def load_stop_words(stop_words_path):
    stop_words_df = pd.read_csv(stop_words_path, header=None)
    stop_words = set(stop_words_df[0].values)
    return stop_words

def process_sentences(sentence, stop_words):
    sentence = re.sub(r'[^\w\d]', ' ', sentence)
    sentence_tokenizer = word_tokenize(sentence)
    sentence_tokenizer = [
        word.lower().replace(" ", "_")
        for word in sentence_tokenizer
        if word not in stop_words and len(word) > 1
    ]
    return " ".join(sentence_tokenizer)

def app():
    # Giao diện ứng dụng
    st.title("Dự Đoán Nhãn Văn Bản")
    # Tải file dữ liệu
    uploaded_file = st.file_uploader("Chọn file CSV chứa các bình luận", type=["csv"])

    if uploaded_file is not None:
        # Đọc file CSV
        input_data = pd.read_csv(uploaded_file)
        columns = input_data.columns.to_list()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)


        # Kiểm tra cột 'comments'
        if 'comments' not in input_data.columns:
            st.error("File CSV cần có cột 'comments'.")
        else:
            # Tải mô hình
            data = input_data[columns[0]].to_list()
            stopword = load_stop_words(r"..\train_model\Data\vietnamese-stopwords-dash.txt")
            data = [process_sentences(sentence, stopword) for sentence in data]
            data_tokenizers = [
                tokenizer.encode(
                    sentence, 
                    return_tensors="pt", 
                    padding=True, 
                    truncation=True
                ).to(device)
                for sentence in data
            ]
            with torch.no_grad():  # Tắt gradient khi chỉ dự đoán
                outputs = [model(data_tokenizer) for data_tokenizer in data_tokenizers]
            logits = [output.logits for output in outputs]
            predictions = [torch.argmax(logit, dim=-1) for logit in logits]
            y_preds = [
                int(pred.item())
                for pred in predictions
            ]
            y_predictions = []
            for y_pred in y_preds:
                if y_pred == 0:
                    y_predictions.append("NEG")
                elif y_pred == 1:
                    y_predictions.append("POS")
                else:
                    y_predictions.append("NEU")
            # encoder = joblib.load('../train_model/Model/label_encoder.pkl')
            # y_train_decoded = encoder.inverse_transform(y_pred)
            # Chuyển đổi dự đoán thành DataFrame
            input_data['predictions'] = y_predictions

            # Hiển thị kết quả
            st.write("Kết quả dự đoán:")
            st.dataframe(input_data[['comments', 'predictions']])
            df = pd.DataFrame(input_data[['comments', 'predictions']])
            data_analysis(df, data)

def data_analysis(df, data):
    st.title("Phân tích dữ liệu:")
    st.write("Word Cloud")
    all_words = " ".join(data).split()
    word_freq = Counter(all_words)
    wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Word Cloud")
    st.pyplot(plt)

    st.write("Biểu đồ bar")
    df['predictions'].value_counts().plot(kind='bar')
    fig, ax = plt.subplots()
    sentiment_counts = df['predictions'].value_counts()
    ax.bar(sentiment_counts.index, sentiment_counts.values)
    ax.set_xlabel("predictions")
    ax.set_ylabel("Tần số")
    ax.set_title("Biểu đồ tần số phân loại cảm xúc của khách hàng sendo")
    st.pyplot(fig)

    st.write("Biểu đồ tròn")
    sentiment_counts = df['predictions'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(
        sentiment_counts.values, 
        labels=sentiment_counts.index, 
        autopct='%1.1f%%', 
        startangle=90
    )
    ax.set_title("Biểu đồ tròn thể hiện tần xuất phân loại cảm xúc của khách hàng sendo")
    st.pyplot(fig)

if __name__ == "__main__":
    app()