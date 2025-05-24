import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

column_names = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']
data = pd.read_csv('car.data', names=column_names)

print("Thông tin dữ liệu:")
print(data.head())
print("\nKích thước dữ liệu:", data.shape)
print("\nThống kê các lớp:")
print(data['class'].value_counts())

encoders = {}
for column in data.columns:
    encoders[column] = LabelEncoder()
    data[column] = encoders[column].fit_transform(data[column])

X = data.drop('class', axis=1)
y = data['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_pred = knn_model.predict(X_test)

print("\n--- Kết quả mô hình KNN ---")
print("Độ chính xác:", accuracy_score(y_test, knn_pred))
print(classification_report(y_test, knn_pred, target_names=encoders['class'].classes_))

def predict_car_class():
    print("\n=== ĐÁNH GIÁ XE HƠI ===")
    print("Vui lòng nhập thông tin về xe:")
    valid_values = {
        'buying': ['vhigh', 'high', 'med', 'low'],
        'maint': ['vhigh', 'high', 'med', 'low'],
        'doors': ['2', '3', '4', '5more'],
        'persons': ['2', '4', 'more'],
        'lug_boot': ['small', 'med', 'big'],
        'safety': ['low', 'med', 'high']
    }
    user_input = {}
    for feature, values in valid_values.items():
        while True:
            print(f"\n{feature} ({', '.join(values)}): ", end="")
            value = input().lower()
            if value in values:
                user_input[feature] = value
                break
            else:
                print(f"Giá trị không hợp lệ. Vui lòng chọn một trong các giá trị: {', '.join(values)}")
    input_encoded = {}
    for feature, value in user_input.items():
        input_encoded[feature] = encoders[feature].transform([value])[0]
    input_df = pd.DataFrame([input_encoded])
    knn_prediction = encoders['class'].inverse_transform([knn_model.predict(input_df)[0]])[0]
    print("\n=== KẾT QUẢ ĐÁNH GIÁ ===")
    print(f"Mô hình KNN: {knn_prediction}")
    class_meanings = {
        'unacc': 'không chấp nhận được',
        'acc': 'chấp nhận được',
        'good': 'tốt',
        'vgood': 'rất tốt'
    }
    print(f"\nĐánh giá: {class_meanings.get(knn_prediction, knn_prediction)}")
    print("\nBạn có muốn đánh giá xe khác không? (y/n): ", end="")
    return input().lower() == 'y'

if __name__ == "__main__":
    print("\n=== CHỨC NĂNG DỰ ĐOÁN ===")
    print("Bạn có muốn đánh giá một chiếc xe? (y/n): ", end="")
    if input().lower() == 'y':
        while predict_car_class():
            pass