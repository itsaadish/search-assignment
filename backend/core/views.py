# backend/core/views.py (add these views)
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SearchQuery, ProductResult
from .utils import parse_query_with_ai
from .tasks import start_scraping
import threading

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
    

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt', '')
        
        try:
            parsed_query = parse_query_with_ai(prompt)
            print(parsed_query)
            search = SearchQuery.objects.create(
                user=request.user,
                raw_query=prompt,
                parsed_query=parsed_query,
                status='processing'
            )
            
            # Start async scraping task
            thread = threading.Thread(target=start_scraping, args=(search.id,))
            thread.start()
            
            return Response({
                "search_id": search.id,
                "status": "processing",
                "message": "Search started successfully"
            }, status=status.HTTP_202_ACCEPTED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, search_id):
        try:
            search = SearchQuery.objects.get(id=search_id, user=request.user)
            results = ProductResult.objects.filter(search=search)
            
            return Response({
                "status": search.status,
                "results": [{
                    "website": result.website,
                    "title": result.title,
                    "price": str(result.price),
                    "image_url": result.image_url,
                    "product_url": result.product_url,
                    "size": result.size,
                    "material": result.material
                } for result in results]
            })
            
        except SearchQuery.DoesNotExist:
            return Response({"error": "Search not found"}, status=404)