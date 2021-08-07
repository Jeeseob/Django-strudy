from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from addresses.models import Addresses
from .serializers import AddressesSerializer


# Create your views here.
@csrf_exempt
def controlAddress_list(request):
    if request.method == 'GET':
        query_set = Addresses.objects.all()
        serializer = AddressesSerializer(query_set, many=True)  # many = True -> 데이터가 여러개라는 의미
        return JsonResponse(serializer.data, safe=False)  # safe??

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(data=data)
        if serializer.is_valid():  # 클라이언트에서 보낸 데이터와 serializer의 데이터가 같다면,
            serializer.save()  # 들어온 값으로 생성
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def controlAddress(request, pk):
    # column 중에 pk 값을 pk로 지정하겠다. get은 1개 filter는 여러개

    address_object = Addresses.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = AddressesSerializer(address_object)
        return JsonResponse(serializer.data, safe=False)  # safe??

    elif request.method == 'PUT':
        # PUT은 update이기 때문에
        data = JSONParser().parse(request)
        serializer = AddressesSerializer(address_object, data=data)
        if serializer.is_valid():  # 클라이언트에서 보낸 데이터와 serializer의 데이터가 같다면,
            serializer.save()  # 들어온 값으로 생성
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        address_object.delete()
        return HttpResponse(status=204)


# login part

@csrf_exempt
def login(request):
    if request.method == 'POST':
        #jsonParser를 사용하여 request에 대한 json 파일을 가져온다.
        data = JSONParser().parse(request)
        # inputId = request.Post['name'](처음 시도했던 것) -> request 안에 method와 url 정보 밖에 없음
        # inputId에 json의 name 값을 넣는다.
        inputId = data['name']
        # inputId를 key로 Addresses에서 row값을 가져온다.
        userObject = Addresses.objects.get(name=inputId)
        if data['phone_number'] == userObject.phone_number:
            print('login success')
            return HttpResponse(status=200)
        else:
            print('login failed')
            return HttpResponse(status=400)

