# SotaChatbot
Chatbot hỗ trợ các thành viên trong team AI tìm kiếm hội thảo, paper, SOTA, github trending, cập nhật các cuộc thi trên Kaggle.

# Hướng dẫn
1, Cài môi trường
- Install rasa: pip install rasa-x --extra-index-url https://pypi.rasa.com/simple
Sau khi chạy lệnh trên xong bạn sẽ cài được:
+ rasa                      1.10.1                   
+ rasa-sdk                  1.10.1                   
+ rasa-x                    0.28.3 
2, Run
Dùng 2 cửa sổ terminal chạy lệnh
+ chuyển qua môi trường mà bạn cài rasa: source rasa/bin/activate
+ cd tới thu mục lưu project
+ rasa run actions
+ rasa x
Hai cửa sổ trên phải chạy cùng 1 lúc
Sau đó 1 cửa sổ rasa x sẽ chạy trên web browser của bạn. Vào menu, chọn Talk to your bot
Done! Bạn đã có thể chat với bot
