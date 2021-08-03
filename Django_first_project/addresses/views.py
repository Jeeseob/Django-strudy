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
        serializer = AddressesSerializer(query_set, many=True)  # many?
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