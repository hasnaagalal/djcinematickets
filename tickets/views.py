from django.shortcuts import render
from django.http.response import JsonResponse  
from .models import Guest
from rest_framework.decorators import api_view
from .serializers import Guestserializer , Movieserializer ,Reservationserializer
from rest_framework import status ,filters
from rest_framework.response import Response

#1 no rest and no model query FBV
def no_rest_no_model(request):
    guests=[
        {
            'id':1,
            'name':'hasnaa',
            'mobile':123456,
        },
        {
            'id':2,
            'name':'marwa',
            'mobile':456789,   
        }
    ]
    return JsonResponse (guests,safe=False)

#2 model data default django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name','mobile'))
    }
    return JsonResponse(response)

#3 Function Based View 
#3.1 Get Post 
@api_view(['GET','POST'])
def FBV_list(request):
    #Get 
    if request.method =='GET':
        guests=Guest.objects.all()
        serializer=Guestserializer(guests,many=True)
        return Response(serializer.data)
    
    #Post 
    elif request.method =='POST':
        serializer=Guestserializer(data=request.data)
        if serializer.is_valid :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #1 get
    if request.method=='GET':
        serializer=Guestserializer(guest)
        return Response(serializer.data)
    
    #2 put
    if request.method=='PUT':
        serializer=Guestserializer(guest,data=request.data)
        if serializer.is_valid :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    #3 delete
    if request.method=='DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

        
    



        
        

        
    
