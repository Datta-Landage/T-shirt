from instamojo_wrapper import Instamojo
API_KEY = 'test_a714c1dc0994358b0fdf17ba567'
AUTH_TOKEN ='test_a9f627f8348ad47b18f3a788f4a'

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');
response = api.payment_request_create(
    amount='3499',
    purpose='FIFA 16',
    send_email=True,
    email="dattalandge001@gmail.com",
    redirect_url="http://127.0.0.1:8000/handle_redirect"
    )
print(response['payment_request']['longurl'])