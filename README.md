# SotaChatbot
 - Search paper: em có thể search paper về một bài toán cụ thể , hoặc search paper của các hội thảo qua các năm.
 - Cập nhật các trending: em thường xuyên update các trending trên GitHub và Paperwithcode.
 - Tìm hiểu về các hội thảo: cập nhật danh sách các hội thảo đang được mọi người quan tâm.
 - Cập nhật các cuộc thi trên Kaggle ạ.
 - Suggest các bài viết hay về chủ đề Machine learning trên trang Medium.

# Hướng dẫn
1, Tạo môi trường
  	virtualenv -p python3 chatbotpaper 

2, cài đặt thư viện: 
	source chatbotpaper/bin/activate

	pip3 install rasa 
	pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
	
        pip3 install bs4 
	pip3 install lxml 
	pip3 install shell 
	pip3 install requests 

	cài thư viện kaggle:
	B1: 
		pip3 install kaggle 
	B2: làm theo hướng dẫn tải file kaggle.json để authentication. 
		https://www.kaggle.com/docs/api
	

	
2, Run
	tạo tài khoản chatwork. 
	vào API CHATWORK thiết lập API. 
	lấy user name và secret_token từ webhook trên chatwork điền vào file cerdentials.yml 

	api_token = "YOUR_API_TOKEN" 
	secret_token = "YOUR_SECRET_TOKEN"
	
	khỏi chạy localhost run. 
	copy link localhost run vào webhook.  
	
	activate 2 môi trường chatbotpaper chay 2 câu lệnh song song là: rasa run actions và rasa x 
	Hai cửa sổ trên phải chạy cùng 1 lúc

	activate localhost run. 


	Done! 
