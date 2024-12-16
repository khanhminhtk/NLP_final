# Một đồ án được xây dựng nhầm phân quan điểm của khách hàng sendo thông qua các mô hình máy học và học sâu được train trên bộ dữ dữ liệu vietnamese-sentiment-analyst
Link data: https://www.kaggle.com/datasets/linhlpv/vietnamese-sentiment-analyst/data

# Cấu trúc đồ án

![image](https://github.com/user-attachments/assets/36d5a1ff-6cd3-468a-a51e-b5fa69fbf4c6)

# Kết quả thu được khi thực hiện train trên 3 model máy học như Decision Tree, Logistic Regression, Naive Bayes

![image](https://github.com/user-attachments/assets/81f6fb50-48b7-474b-ae50-633b6df1574a)

# Kết quả thu được thi thực hiện train trên 2 model học sâu như pho-bert, pho-bert-base-vietnamese-sentiment

## pho-bert
![image](https://github.com/user-attachments/assets/578b1737-2603-4419-a69b-64d0ae770197)

## pho-bert-base-vietnamese-sentiment

![image](https://github.com/user-attachments/assets/a9b3e217-4ed1-4b5b-9600-5da0eaf1ed9e)

# App deploy để áp dụng model vào phân tích quan điểm của khách hàng sendo

![Screenshot 2024-12-15 212848](https://github.com/user-attachments/assets/75d5551c-e17f-4796-bb44-5402667724e5)
![Screenshot 2024-12-15 212942](https://github.com/user-attachments/assets/cc56ecbd-6a95-412f-982b-2735354a6df8)
![Screenshot 2024-12-15 213004](https://github.com/user-attachments/assets/dcdb6474-8342-4d26-b5d7-9f74355ce37e)
![Screenshot 2024-12-15 213056](https://github.com/user-attachments/assets/d40190ec-038c-4517-88d4-9942579dec0e)
![Screenshot 2024-12-15 213136](https://github.com/user-attachments/assets/68919868-72ab-45f4-ab34-fc6b570bc3ef)
![Screenshot 2024-12-15 213157](https://github.com/user-attachments/assets/2f3ac271-351f-4baf-9e72-d6297f848b9d)
![Screenshot 2024-12-15 215719](https://github.com/user-attachments/assets/a9ba16eb-3bb0-4afd-97fa-d1b3e9300f62)

# Nhược điểm
- Tài nguyên GPU của google colab có hạn nên không train đủ số epoch do đó độ chính xác của mô hình học sâu ko chênh lệch nhiều so với các mô hình học máy
- Mô hình pho-bert-base-vietnamese-sentiment có dấu hiệu overfitting do đó có thể thêm các lớp dropout và bacthnorm ở lớp classifycation và có thể tăng dropout của lớp robert hay vì 0.1 như ban đầu, tăng cường dữ liệu cũng là 1 phương pháp giảm overfitting

