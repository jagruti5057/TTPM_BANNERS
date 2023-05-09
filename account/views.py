from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import * 
from django.contrib.auth import authenticate, logout
from account.models import  * #Users,Categories,Banners,AdminBanners,Status,ProfileFrame,Forms,Liccirclars,AudioVideo,LeadersCornerCategory
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.viewsets import ModelViewSet
from account.helpers import send_otp,send_otp_via_email,IsAuthenticatedOrCreate,PermissionPolicyMixin,EmailPhoneBackend
from rest_framework import generics
from .helpers import Custom_Pagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.db.models import Q
import os 
from datetime import datetime
from django.http import Http404


# Create your views here.
from django.core.exceptions import ObjectDoesNotExist

class DeviceValiDataionView(APIView):
    """
       An endpoint for  Validating Device
    """
    def post(self,request):
        phone_number = request.data.get('phone_number')
        device_id = request.data.get('device_id', None)
        
        if device_id:
            try:
                user_obj = Users.objects.get(phone_number=phone_number)
                # user_queryset = Users.objects.filter(device_id=device_id)
                # user_queryset = Users.objects.filter(phone_number=phone_number)
                if len(phone_number) != 10:
                    return Response({'status': False, 'detail': 'Please add a valid phone number'})
                
                if user_obj.phone_number == phone_number:
                    token, created = Token.objects.get_or_create(user=user_obj)
                    return Response({'token': token.key, 'user_id': user_obj.id, 'message': 'Login successful', 'status': True}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'detail': 'Invalid phone number'})
            except ObjectDoesNotExist:
                # Return error response when the object is not found
                try:
                    user_queryset = Users.objects.get(device_id=device_id)
                    user_queryset.device_id = device_id
                    user_queryset.phone_number = phone_number
                    user_queryset.save()
                except ObjectDoesNotExist:
                    users =Users(phone_number=phone_number,device_id=device_id)
                    users.save()
                token, created = Token.objects.get_or_create(user=users)
                return Response({'user_id':user.id,'token': token.key,'status': True, 'message': 'Mobile number registered successfully!'},status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'detail': 'Please provide a device ID or phone number'})
            
        return Response({'status': False, 'detail': 'Please provide a device ID or phone number'})


class UserRegistrationView(APIView):
    """
       An endpoint for  Register User
    """
    def post(self, request, format=None):
        try:
            device_id = request.data.get('device_id', False)
            is_admin = request.data.get('is_admin', False)
            email = request.data.get('email')
            user_obj = Users.objects.get(device_id=device_id)
            if email:
                user = Users.objects.filter(email=email)
                if user.exists():
                    return Response({'status': False, 'detail': 'Email already exists'})
                data = send_otp_via_email(email)
                user_obj.email = email 
                user_obj.otp = data 
                user_obj.set_unusable_password()
                user_obj.is_admin=is_admin
                user_obj.save()   
                token, created = Token.objects.get_or_create(user=user_obj)
                return Response({'status':True, 'token': token.key, 'user_id':user_obj.id,'message': 'Registration successfully'})
            return Response({'status': False, 'detail': 'Please Provide Email to verify'})
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request,format=None):
        try:
            user = Users.objects.all()
            serializer = UserSerializer(user,many=True)
            data = serializer.data
            return Response(data,status=200)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ValidateOTP(APIView):
    """
        An endpoint for Validate OTP  From Email To verify User
    """
    def post(self, request, *args, **kwargs):
        try:
            email = request.data .get('email', False)
            otp_send = request.data.get('otp', False)
           
            if email and otp_send:
                old = Users.objects.get(email=email)
                if old:
                    otp = old.otp
                    if str(otp_send) == str(otp):
                        old.validated = True
                        old.save()
                        
                        token = Token.objects.get_or_create(user=old)[0].key
                       
                        return Response({'token':token,'status': True, 'detail' : "OTP matched."})
                    
                    else:
                        return Response({'status': False, 'detail': 'OTP incoorect'})            
            
            
                else:
                    return Response({'status': False, 'detail' : "First proceed via sending otp request"})
            
                
            else:
                return Response({'status': False, 'detail' : "Please provide both email and otp for validation"})
        except Exception as e:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
class UserLogoutView(APIView):
    """ 
      An endpoint for  User Logout 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({'mag':'User Logged out successfully','status':True,},status=status.HTTP_200_OK)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UserRetrieveUpdateDestroyAPIView(APIView): 
    """ 
       An endpoint for User Retrieve,Update and Delete 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        try:
            user = Users.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data,status=200)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,id,format=None):
        try:
            user = Users.objects.get(id=id) 
            user.delete()
            return Response({"msg":" User deleted successfully ","status":True})
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView): 
    """ 
       An endpoint for User Retrieve,Update and Delete 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]  
    def get(self,request):
        try:
            user_id=request.user.id
            
            user = Users.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data,status=200)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request,):
        try:
            user_id=request.user.id
            user = Users.objects.get(id=user_id)
            data=request.data
            serializer = UserProfileSerializer(user,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
 
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    model = Users
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ResendUserOtpAPIView(APIView):
    """
        An endpoint for ResendOTP its also Useful in Forgot Aassword Api
    """
    def post(self,request):
        try: 
            email = request.data.get('email')
            user = Users.objects.get(email=email)
            
            if user:
                data=send_otp_via_email(user.email)
                user.otp=data
                user.save()
                response={
                            'msg':'OTP send successfully',
                            'status':True,
                            'OTP':data
                        }
                return Response(response, status=status.HTTP_200_OK)
            response={
                        'msg':'Email is Not Validate',
                        'status':False,
                    }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            response={
                    'msg':'Something went wrong',
                    'status':False,
                }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


class ResetPasswordAPIView(APIView):
    """
        An endpoint For ForgotPassword or ResetPassword 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def patch(self,request):
        try:
            user=request.user.id
            user = Users.objects.get(id=user)
            if user:
                serializer = ResetPasswordSerializer(user,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    response = {
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }
                    return Response(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryModelViewSet(ModelViewSet):    
    """
      An endpoint for Category CRUD 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('category', [])
        if categories == []:
            queryset = Categories.objects.all()
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        name = request.POST.get('name')
    
        if  name:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_data = {
                'status': True,
                'msg': 'Categories created successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return "Field not none"

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'status': True,
            'msg': 'Categories updated successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'status': True,
            'msg': 'Categories deleted successfully.',
        }
        return Response(response_data, status=status.HTTP_200_OK)

class BanerAPIView(APIView):
    """
        An endpoint for Get and Add banner 
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        category_id = request.query_params.get('category_id')
        type_of_banner = request.query_params.get('type_of_banner')
        
        user = Banners.objects.all()
        if category_id:
            user = user.filter(category_id=category_id)
        if type_of_banner:
            user = user.filter(type_of_banner=type_of_banner)
        # user = Banners.objects.all()
        category=Categories.objects.all()
        list_of_data=[]
        for i in category:
            di={}
            fi=[]
            li=[]
            di['category_id']=i.id
            di['category_name']=i.name
            
            for j in user:
                if i.id==j.category.id:
                    li.append(j.banner_img.url)
                    fi.append(j.is_frame)

                di['templates']=li
                di['is_frame']=fi
                di['type_of_banner']=j.type_of_banner
            list_of_data.append(di)
        
        response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'data': list_of_data,
            }
        return Response(response)
    
    def post(self,request):
        try:
            if request.user.is_admin==True:
                seralizer=BanerSerializers(data=request.data)
                if seralizer.is_valid(raise_exception=True):
                    seralizer.save()
                    response={
                        'status':True,
                        'msg':"Banner added successfully",
                        'data':seralizer.data
                    }
                    return Response(response,status=status.HTTP_200_OK)
                response={
                        'msg':"Something went wrong",
                        'status':False,
                        'data':None
                    }    
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BannerRetrieveUpdateDestroyAPIView(APIView):
    """
        An endpoint for  Retrieve,Update and Destroy Banners/templates
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request,id,):
        try:
            user = Banners.objects.get(id=id)
            serializer = BanerSerializers(user)
            data = serializer.data
            return Response(data,status=200)
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request,id,):
        try:
            if request.user.is_admin==True:
                user = Banners.objects.get(id=id)
                serializer = BanerSerializers(user,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    # data['msg'] = "Banner updated successfully"
                    # data['status'] = True
                    response={
                        'status':True,
                        'msg':"Banner updated successfully",
                        'data':data
                    }
                    return Response(response)
                return Response(serializer.errors)
            else:
                    response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                        }  
                    return response
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,id,format=None):
        try:
            if request.user.is_admin==True:
                banner_obj = Banners.objects.get(id=id) 
                # banner_obj.delete()
                # user_object = self.get_object()
                music_file_path = banner_obj.banner_img.path
                # Delete the media file from the server's file system
                os.remove(music_file_path)
                # AdminBanners.objects.filter(id=user_object.id).delete()
                banner_obj.delete()
                return Response({"msg":" Banner deleted successfully "})
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return response
        except :
            return Response ({"msg":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RecentBanners(generics.ListAPIView):
    """
            An endpoint for Get Recent banners 
    """
  
    serializer_class = BanerSerializers
    def get_queryset(self):
        queryset = Banners.objects.order_by('-updated_at')
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(category__name__icontains=search_query)
        return queryset

class GetCategoryBanners(APIView):
    """ 
      An endpoint for  get all templates for specif categorys
    """
    # pagination_class = Custom_Pagination  # Use the custom pagination class
    def get(self, request,category_id):
        results =  Banners.objects.filter(category__id=category_id).all()
        # Paginate the results and return the current page
        # paginator = self.pagination_class()
        # page = paginator.paginate_queryset(results, request)
        serializer = BanerSerializers(results, many=True)
        # response_data = paginator.get_paginated_response(serializer.data)
        response_data=serializer.data
        # cache.set(cache_id, response_data,timeout_in_seconds)
        return Response(response_data)
    
class AdminBannerModelViewSet(PermissionPolicyMixin, ModelViewSet):
    """
    An endpoint for admin banners/templates
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated, IsAuthenticatedOrCreate],
        "update": [IsAuthenticated, IsAuthenticatedOrCreate]
    }
    serializer_class = AdminBannersSerializer
    queryset = AdminBanners.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                # do your customization here
                user_object = self.get_object()
                music_file_path = user_object.banner_image.path
                # Delete the media file from the server's file system
                os.remove(music_file_path)
                user_object.delete()
                response = {
                    "msg": "Banner deleted successfully",
                    "status": True
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': False,
                    'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    'msg': "NON_AUTHORITATIVE_INFORMATION",
                }
                return Response(response, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            response = {
                'status': False,
                'msg': "Something went wrong",
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        response = {
            'msg':"Banner created successfully",
            'status':True,
            'data':data
        }
        return Response(response, status=status.HTTP_200_OK, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        response = {
            'msg':"Banner updated successfully",
            'status':True,
            'data':data
        }
        return Response(data, status=status.HTTP_200_OK)
        
class NewsArticalModelViewSet(ModelViewSet):
    """
      An endpoint for News and Article CRUD
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated, IsAuthenticatedOrCreate],
        "update": [IsAuthenticated, IsAuthenticatedOrCreate]
    }
    serializer_class = NewsArticalSerializer
    queryset = NewsArticals.objects.all()

    def list(self, request):
        news_queryset = NewsArticals.objects.filter(type_of_document='N')
        articles_queryset = NewsArticals.objects.filter(type_of_document='A')

        news_serializer = NewsArticalSerializer(news_queryset, many=True)
        articles_serializer = NewsArticalSerializer(articles_queryset, many=True)

        return Response({'news': news_serializer.data, 'articles': articles_serializer.data})

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin:
                user_object = self.get_object()
                NewsArticals.objects.filter(id=user_object.id).delete()
                if user_object.type_of_document == 'A':
                    music_file_path = user_object.articals_img.path
                    os.remove(music_file_path)
                user_object.delete()
                response = {
                    "msg": "NewsArtical deleted successfully",
                    "status": True
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': False,
                    'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    'msg': "NON_AUTHORITATIVE_INFORMATION",
                }
                return Response(response, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            response = {
                'status': False,
                'msg': "Something went wrong",
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "msg": "NewsArtical created successfully",
                    "status": True,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": False,
                    "msg": serializer.errors
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except:
            response = {
                "status": False,
                "msg": "Something went wrong"
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "msg": "NewsArtical updated successfully",
                    "status": True,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": False,
                    "msg": serializer.errors
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            response = {
                "status": False,
                "msg": "Something went wrong"
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StatusList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]  
    def get(self, request):
        category = request.query_params.get('category')
        if category:
            statuses = Status.objects.filter(type_of_status=category)
        else:
            statuses = Status.objects.all()

        statuses = statuses.order_by('-timestamp')
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            user=Users.objects.get(id=request.user.id)
            serializer.save(user=user)
            response = {
                'serializer':serializer.data,
                'message': 'Status created successfully',
                'status': True
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class StatusDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Status.objects.get(pk=pk)
#         except Status.DoesNotExist:
#             raise status.HTTP_404_NOT_FOUND

#     def get(self, request, pk):
#         status = self.get_object(pk)
#         serializer = StatusSerializer(status)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         status = self.get_object(pk)
#         serializer = StatusSerializer(status, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         instance = self.get_object(pk)
#         media_file_path = instance.media.path
#         music_file_path = instance.file.path
#         # Delete the media file from the server's file system
#         os.remove(media_file_path)
#         os.remove(music_file_path)
#         instance.delete()
#         response={
#             'message':'status deleted successfully',
#             'status':True
#         }
#         return Response(response,)

class StatusDetail(APIView):
    def get_object(self, pk):
        try:
            return Status.objects.get(pk=pk)
            print(Status.objects.get(pk=pk))
        except Status.DoesNotExist:
            raise Http404("Status not found")

    def get(self, request, pk):
        try:

            status = self.get_object(pk)
            serializer = StatusSerializer(status)
            return Response(serializer.data)
        except Status.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def put(self, request, pk):
        statu = self.get_object(pk)
        serializer = StatusSerializer(statu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'serializer':serializer.data,
                'message': 'Status updated successfully',
                'status': True
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'message': 'Invalid data',
                'status': False
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            instance = self.get_object(pk)
            media_file_path = instance.media.path
            music_file_path = instance.file.path
            # Delete the media file from the server's file system
            os.remove(media_file_path)
            os.remove(music_file_path)
            instance.delete()
            response={
                'message':'Status deleted successfully',
                'status':True
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response={
                'message': str(e),
                'status': False
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework import status

class LiccirclarsModelViewSet(ModelViewSet):
    """
    An endpoint for Liccirclars CRUD
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated, IsAuthenticatedOrCreate],
        "create": [IsAuthenticated, IsAuthenticatedOrCreate],
        "update": [IsAuthenticated, IsAuthenticatedOrCreate],
        "destroy": [IsAuthenticated, IsAuthenticatedOrCreate],
    }
    queryset = Liccirclars.objects.all()
    serializer_class = LiccirclarsSerializer

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('category', [])
        if categories == []:
            queryset = Liccirclars.objects.all().order_by('-created_at')  
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            'status': True,
            'msg': 'TTPM created successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = {
            'status': True,
            'msg': 'TTPM updated successfully.',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
            'status': True,
            'msg': 'TTPM deleted successfully.',
        }
        return Response(response_data, status=status.HTTP_200_OK)

class LicbannersModelViewSet(ModelViewSet):
    """
    An endpoint for Licbanners CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = licplans.objects.all()
    serializer_class = LicbannersSerializer

    def list(self, request, *args, **kwargs):
        """
        list of licplans filtered by category
        """
        categories = request.GET.getlist('category', [])
        if categories==[]:
            queryset = licplans.objects.all()
        else:
            queryset = self.get_queryset().filter(category__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            "status": True,
            "message": "licplan created successfully",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": True,
            "message": "licplan updated successfully",
            "data": serializer.data
        }
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        return Response(response)


    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                licplans.objects.filter(id=user_object.id).delete()
                licbanner_file_path = user_object.lic_banners.path
                # Delete the media file from the server's file system
                os.remove(licbanner_file_path)
                user_object.delete()
                response={
                        "msg":"licplans deleted successfully",
                        "status":True
                        }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FormsModelViewSet(ModelViewSet):
    """
        An endpoint for Forms CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                Forms.objects.filter(id=user_object.id).delete()
                forms_file_path = user_object.file.path
            # Delete the media file from the server's file system
                os.remove(forms_file_path)
                user_object.delete()
                response={
                        "msg":"Forms deleted successfully",
                        "status":True
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileFrameModelViewSet(ModelViewSet):
    """
    An endpoint for ProfileFrame CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = ProfileFrame.objects.all()
    serializer_class = ProfileFrameSerializer

    def list(self, request, *args, **kwargs):
        """
            list of ProfileFrame filtered by category
        """
        categories = request.GET.getlist('category', [])
        if categories==[]:
            queryset = ProfileFrame.objects.all() 
        else:
            queryset = self.get_queryset().filter(type_of_frames__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "msg": "ProfileFrame created successfully",
                "status": True,
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "msg": "Bad Request",
                "status": False,
                "data": serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                "msg": "ProfileFrame updated successfully",
                "status": True,
                "data": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                "msg": "Bad Request",
                "status": False,
                "data": serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                ProfileFrame.objects.filter(id=user_object.id).delete()
                profile_file_path = user_object.frame_image.path
                # Delete the media file from the server's file system
                os.remove(profile_file_path)
                user_object.delete()
                response={
                            "msg":"ProfileFrame deleted successfully",
                            "status":True
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AudioVideoModelViewSet(ModelViewSet):
    """
    An endpoint for ProfileFrame CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = AudioVideo.objects.all()
    serializer_class = AudioSerializer
    # serializer_class = VideoSerializer

    def list(self, request, *args, **kwargs):
        """
            list of AudioVideo filtered by category
        """
        categories = request.GET.getlist('category', [])
        if categories==[]:
            queryset = AudioVideo.objects.all() 
        else:
            queryset = self.get_queryset().filter(type_of_av__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response={
            "msg":"AudioVideo created successfully",
            "status":True,
            "data": serializer.data
        }
        return Response(response,status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response={
            "msg":"AudioVideo updated successfully",
            "status":True,
            "data": serializer.data
        }
        return Response(response)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                AudioVideo.objects.filter(id=user_object.id).delete()
                audio_file_path = user_object.image.path
                video_file_path = user_object.file.path
                # Delete the media file from the server's file system
                os.remove(audio_file_path)
                os.remove(video_file_path)
                user_object.delete()
                response={
                        "msg":"AudioVideo deleted successfully",
                        "status":True
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StatusCategoryModelViewSet(ModelViewSet):
    """
        An endpoint for StatusCategory CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = StatusCategory.objects.all()
    serializer_class = StatusCategorySerializer
    # parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
            try:
                if request.user.is_admin==True:
                    # do your customization here
                    user_object = self.get_object()
                    StatusCategory.objects.filter(id=user_object.id).delete()
                    user_object.delete()
                    response={
                            "msg":"StatusCategory deleted successfully",
                            "status":True
                    }
                    return Response(response,status=status.HTTP_200_OK)
                else:
                    response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                        }  
                    return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except :
                return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class PlanCategoryModelViewSet(ModelViewSet):
#     """
#         An endpoint for PlanCategory CRUD
#     """
#     authentication_classes=[TokenAuthentication]
#     permission_classes=[IsAuthenticated]
#     permission_classes_per_method = {
#         "list": [IsAuthenticated],
#         "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
#         "create": [IsAuthenticated,IsAuthenticatedOrCreate],
#         "update": [IsAuthenticated,IsAuthenticatedOrCreate]
#     }
#     queryset = PlanCategory.objects.all()
#     serializer_class = PlanCategorySerializer
#     # parser_classes = (MultiPartParser, FormParser,)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         else:
#             return Response(serializer.errors, status=400)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)

#     def destroy(self, request, *args, **kwargs):
#             try:
#                 if request.user.is_admin==True:
#                     # do your customization here
#                     user_object = self.get_object()
#                     PlanCategory.objects.filter(id=user_object.id).delete()
#                     user_object.delete()
#                     response={
#                             "msg":"PlanCategory deleted successfully",
#                             "status":True
#                     }
#                     return Response(response,status=status.HTTP_200_OK)
#                 else:
#                     response = {
#                             'status': False,
#                             'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
#                             'msg': "NON_AUTHORITATIVE_INFORMATION",
#                         }  
#                     return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#             except :
#                 return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarketingCategoryModelViewSet(ModelViewSet):
    """
        An endpoint for MarketingCategory CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = MarketingCategory.objects.all()
    serializer_class = MarketingCategorySerializer
    # parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
            try:
                if request.user.is_admin==True:
                    # do your customization here
                    user_object = self.get_object()
                    MarketingCategory.objects.filter(id=user_object.id).delete()
                    user_object.delete()
                    response={
                            "msg":"MarketingCategory deleted successfully",
                            "status":True
                    }
                    return Response(response,status=status.HTTP_200_OK)
                else:
                    response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                        }  
                    return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except :
                return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarketingSmsModelViewSet(ModelViewSet):
    """
    An endpoint for MarketingSms CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = MarketingSms.objects.all()
    serializer_class = MarketingSmsSerializer

    def list(self, request, *args, **kwargs):
        """
        list of ProfileFrame filtered by category
        """
        categories = request.GET.getlist('category', [])
        if categories==[]:
            queryset = MarketingSms.objects.all() 
        else:
            queryset = self.get_queryset().filter(marketingcategory__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                MarketingSms.objects.filter(id=user_object.id).delete()
                user_object.delete()
                response={
                        "msg":"MarketingSms deleted successfully",
                        "status":True
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                    'status': False,
                    'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    'msg': "NON_AUTHORITATIVE_INFORMATION",
                }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except:
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "msg": "MarketingSms created successfully",
            "status": True,
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "msg": "MarketingSms updated successfully",
            "status": True,
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class PremiumCalendarView(APIView): 
   
    def post(self, request, format=None):
        serializer = PremiumCalendarSerializer(data=request.data)
        user = PremiumCalendar.objects.all()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Data added successfully ',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,format=None):
        user = PremiumCalendar.objects.all()
        serializer = PremiumCalendarGetSerializer(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request,id,):
        user = PremiumCalendar.objects.get(id=id)
        serializer = PremiumCalendarSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = PremiumCalendar.objects.get(id=id) 
            user.delete()
            return Response({"msg":" data deleted successfully "},status=status.HTTP_200_OK)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class PolicyDetailsView(APIView): 
   
    def post(self, request, format=None):
        serializer = PolicyDetailsSerializer(data=request.data)
        user = PolicyDetails.objects.all()
        type_of_user = request.data.get('type_of_user')
        if serializer.is_valid(raise_exception=True):
            type_of_users = PremiumCalendar.objects.get(pk=type_of_user)
            serializer.save(type_of_user=type_of_users)
            response={
                'msg':'Data added successfully ',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, format=None):
        if pk:
            policy = PolicyDetails.objects.get(pk=pk)
            serializer = PolicyDetailsGetSerializer(policy)
        else:
            policies = PolicyDetails.objects.all()
            serializer = PolicyDetailsGetSerializer(policies, many=True)
        return Response(serializer.data)
    
    def put(self, request,id,):
        user = PolicyDetails.objects.get(id=id)
        serializer = PolicyDetailsSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id,format=None):
        try:
            user = PolicyDetails.objects.get(id=id) 
            user.delete()
            return Response({"msg":" data deleted successfully "},status=status.HTTP_200_OK)   
        except:
            return Response ({"msg":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)

class PolicyCalendarDetailsView(APIView):
    serializer_class = PolicdetailsCalendarSerializer

    def get(self, request, format=None):
        search = request.GET.get('search')
        if search:
            policy_details = PolicyDetails.objects.filter(
                Q(type_of_user__username__icontains=search) | Q(policy_number__icontains=search) | 
                Q(product_name__icontains=search) | Q(sum_assured__icontains=search) |
                Q(policy_next_due__icontains=search)
            )
        else:
            policy_details = PolicyDetails.objects.all()

        serializer = self.serializer_class(policy_details, many=True)
        return Response(serializer.data)

class PolicyCalendarDetailsViewOne(APIView):
    def get(self, request, format=None):
        # Retrieve search parameters from the request
        search_username = request.GET.get('search_username', None)
        search_mobile_no = request.GET.get('search_mobile_no', None)
        policy_next_due_start = request.GET.get('policy_next_due_start', None)
        policy_next_due_end = request.GET.get('policy_next_due_end', None)

        # Build query set filters based on search parameters
        queryset_filters = Q()
        if search_username:
            queryset_filters &= Q(username__icontains=search_username)
        if search_mobile_no:
            queryset_filters &= Q(mobile_no__icontains=search_mobile_no)
        if policy_next_due_start and policy_next_due_end:
            policy_next_due_start = datetime.strptime(policy_next_due_start, '%Y-%m-%d').date()
            policy_next_due_end = datetime.strptime(policy_next_due_end, '%Y-%m-%d').date()
            queryset_filters &= Q(policydetails__policy_next_due__date__range=[policy_next_due_start, policy_next_due_end])

        # Apply filters to query set
        queryset = PremiumCalendar.objects.filter(queryset_filters).distinct()

        # Serialize the query set and return the response
        serializer = ParentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MixPlanCategoryModelViewSet(ModelViewSet):
    """
        An endpoint for MixPlanCategory CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = MixPlanCategory.objects.all()
    serializer_class = MixPlanCategorySerializer
    # parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
            try:
                if request.user.is_admin==True:
                    # do your customization here
                    user_object = self.get_object()
                    MixPlanCategory.objects.filter(id=user_object.id).delete()
                    user_object.delete()
                    response={
                            "msg":"MixPlanCategory deleted successfully",
                            "status":True
                    }
                    return Response(response,status=status.HTTP_200_OK)
                else:
                    response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                        }  
                    return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except :
                return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MixPlanModelViewSet(ModelViewSet):
    """
        An endpoint for MixPlanCategory CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = MixPlan.objects.all()
    serializer_class = MixPlanSerializer

    def list(self, request, *args, **kwargs):
        """
            list of ProfileFrame filtered by category
        """
        categories = request.GET.getlist('category', [])
        if categories==[]:
            queryset = MixPlan.objects.all() 
        else:
            queryset = self.get_queryset().filter(MixPlanCategory__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                MixPlan.objects.filter(id=user_object.id).delete()
                mixplan_file_path = user_object.mixplan_banners.path
                # Delete the media file from the server's file system
                os.remove(mixplan_file_path)
                user_object.delete()
                response={
                            "msg":"MixPlan deleted successfully",
                            "status":True
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LeadersCornerCategoryModelViewSet(ModelViewSet):
    """
        An endpoint for LeadersCornerCategory CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = LeadersCornerCategory.objects.all()
    serializer_class = LeadersCornerCategorySerializer
    parser_classes = (MultiPartParser, FormParser,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
            try:
                if request.user.is_admin==True:
                    # do your customization here
                    user_object = self.get_object()
                    LeadersCornerCategory.objects.filter(id=user_object.id).delete()
                    user_object.delete()
                    response={
                            "msg":"LeadersCornerCategory deleted successfully",
                            "status":True
                    }
                    return Response(response,status=status.HTTP_200_OK)
                else:
                    response = {
                            'status': False,
                            'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                            'msg': "NON_AUTHORITATIVE_INFORMATION",
                        }  
                    return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except :
                return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LeadersCornerModelViewSet(ModelViewSet):
    """
        An endpoint for LeadersCorner CRUD
    """
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    permission_classes_per_method = {
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated,IsAuthenticatedOrCreate],
        "create": [IsAuthenticated,IsAuthenticatedOrCreate],
        "update": [IsAuthenticated,IsAuthenticatedOrCreate]
    }
    queryset = LeadersCorner.objects.all()
    serializer_class = LeadersCornerSerializer

    def list(self, request, *args, **kwargs):
        """
            list of ProfileFrame filtered by category
        """
        categories = request.GET.getlist('category', [])
        if categories==[]:
            queryset = LeadersCorner.objects.all() 
        else:
            queryset = self.get_queryset().filter(leaderscategory__in=categories)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            if request.user.is_admin==True:
                # do your customization here
                user_object = self.get_object()
                LeadersCorner.objects.filter(id=user_object.id).delete()
                leadercorner_file_path = user_object.leader_banners.path
                # Delete the media file from the server's file system
                os.remove(leadercorner_file_path)
                user_object.delete()
                response={
                            "msg":"LeadersCorner deleted successfully",
                            "status":True
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status': False,
                        'code': status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                        'msg': "NON_AUTHORITATIVE_INFORMATION",
                    }  
                return Response(response,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except :
            return Response (status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SuggestionFeedbackViewSet(ModelViewSet):
    """
    API endpoint for SuggestionFeedback CRUD.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = SuggestionFeedback.objects.all()
    serializer_class = SuggestionFeedbackSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all suggestions and feedbacks.
        """
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a suggestion/feedback.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {"message": "Suggestion/Feedback created successfully."},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a suggestion/feedback.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update a suggestion/feedback.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Suggestion/Feedback updated successfully."},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a suggestion/feedback.
        """
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Suggestion/Feedback deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

#**********************************************admin site*************************************

# admin side api 
class UserRegistrationAdminView(APIView):
    """
    An endpoint for Register User
    """

    def post(self, request, format=None):
        # try:
        query = Users.objects.all()
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')
            full_name = request.data.get('full_name')
            designation = request.data.get('designation')
            phone_number = request.data.get('phone_number')
            date_of_birth = request.data.get('date_of_birth')
            date_of_joining = request.data.get('date_of_joining')
            pincode = request.data.get('pincode')
            state = request.data.get('state')
            city = request.data.get('city')
            profile_image = request.data.get('profile_image')
            is_admin = request.data.get('is_admin', False)
            
            # check for none values
            if not email:
                return Response({'status': False, 'detail': 'Email is required'})
            if not password:
                return Response({'status': False, 'detail': 'Password is required'})
            if not full_name:
                return Response({'status': False, 'detail': 'Full name is required'})
            if not designation:
                return Response({'status': False, 'detail': 'Designation is required'})
            if not phone_number:
                return Response({'status': False, 'detail': 'Phone number is required'})
            if not date_of_birth:
                return Response({'status': False, 'detail': 'Date of birth is required'})
            if not date_of_joining:
                return Response({'status': False, 'detail': 'Date of joining is required'})
            if not pincode:
                return Response({'status': False, 'detail': 'Pincode is required'})
            if not state:
                return Response({'status': False, 'detail': 'State is required'})
            if not city:
                return Response({'status': False, 'detail': 'City is required'})
            
            date_of_birth_ = datetime.strptime(date_of_birth, "%d-%m-%Y").strftime("%Y-%m-%d")
            date_of_joining_ = datetime.strptime(date_of_joining, "%d-%m-%Y").strftime("%Y-%m-%d")
            
            # check if email or phone number already exists
            if Users.objects.filter(email=email).exists():
                return Response({'status': False, 'detail': 'Email already exists'})
            elif Users.objects.filter(phone_number=phone_number).exists():
                return Response({'status': False, 'detail': 'Phone number already exists'})
            
            user = Users(
                email=email,
                password=password,
                full_name=full_name,
                designation=designation,
                phone_number=phone_number,
                date_of_birth=date_of_birth_,
                date_of_joining=date_of_joining_,
                pincode=pincode,
                state=state,
                city=city,
                profile_image=profile_image,
                is_admin=is_admin
            )
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': True, 'token': token.key, 'user_id': user.id, 'message': 'Registration successfully'})
        return Response({'status': False, 'detail': 'Please Provide Email to verify'})

    
class LoginadminView(APIView):
    authentication_classes = [EmailPhoneBackend]

    def post(self, request):
        # Get email and phone_number from request data
        email = request.data.get('email')
        password = request.data.get('password')
        obj = Users.objects.filter(email=email,password=password).first()
        if obj:
            # Authenticate user using custom authentication class
            user = self.authentication_classes[0].authenticate(self,request,email=email, password=password)

            if user is not None:
                # Generate token for authenticated user
                token, created = Token.objects.get_or_create(user=user)

                # Return token and any other additional data in the response
                return Response({'token': token.key, 'user_id':user.id,'message': 'Login successful'})
        else:
            return Response({'message': 'Invalid email or password'}, status=401)

