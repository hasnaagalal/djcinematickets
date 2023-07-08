from django.shortcuts import render
from django.http.response import JsonResponse  
from .models import Guest , Movie ,Reservation
from rest_framework.decorators import api_view
from .serializers import Guestserializer , Movieserializer ,Reservationserializer
from rest_framework import status ,filters , mixins, generics , viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404


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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    
#3.2 get put delete 
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
    
#4 class based view
#4.1 list and create == Get and Post 
class CBV_list (APIView):
    def get (self, request):
        guests = Guest.objects.all()
        serializer = Guestserializer(guests, many=True)
        return Response(serializer.data)
    def post (self, request):
        serializer = Guestserializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )
   
   
#4.2 GET & PUT & DELETE 
class CBV_pk (APIView):
    def get_object (self , pk) :
        try:
         return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
         raise Http404
    def get(self, request,pk):
        guest=self.get_object(pk)
        serializer=Guestserializer(guest)
        return Response(serializer.data)
    def put (self ,request, pk ):
        guest=self.get_object(pk)
        serializer=Guestserializer(guest,data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self ,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#5 mixins 
#5.1 mixins_list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class = Guestserializer
    
    def get(self , request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
#5.2 mixins_pk 
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
    
    def get(self , request ,pk):
        return self.retrieve(request)
    def put(self, request ,pk):
        return self.update(request)
    def delete(self, request ,pk):
        return self.destroy(request)
    
    
#6 generics
#6.1 get and post 
class generics_list (generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer


#6.2 get put delete  
class generics_pk (generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer 
    
#7 
#7.1 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = Guestserializer
        
#7.2
class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = Movieserializer    
    filter_backends=[filters.SearchFilter]
    search_fields=['movie','name']

#7.3
class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = Reservationserializer  
    
    
#8 find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        #hall=request.data['hall'],
        movie=request.data['movie'], 
    )
    serializer=Movieserializer(movies, many=True )
    return Response(serializer.data)

    
 #9 create new reservation 
@api_view(['POST'])
def new_reservation(request):

    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)   
              



        
    



        
        

        
    
