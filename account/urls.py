from django.urls import path, include
from account.views import * #serRegistrationView,AdminBannerModelViewSet UserLoginView, UserLogoutView,CategoryModelViewSet,ProfileFrameModelViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'category', CategoryModelViewSet)
router.register(r'admin_banners', AdminBannerModelViewSet)
router.register(r'news_articals', NewsArticalModelViewSet)
router.register(r'Liccirclars', LiccirclarsModelViewSet)
router.register(r'Licbanners', LicbannersModelViewSet)
router.register(r'forms', FormsModelViewSet)
router.register(r'profileframe', ProfileFrameModelViewSet)
router.register(r'audiovideo', AudioVideoModelViewSet)
# router.register(r'plancategory', PlanCategoryModelViewSet)
router.register(r'marketingcategory', MarketingCategoryModelViewSet)
router.register(r'marketingsms', MarketingSmsModelViewSet)
router.register(r'mixplancategory', MixPlanCategoryModelViewSet)
router.register(r'mixplan', MixPlanModelViewSet)
router.register(r'leaders', LeadersCornerCategoryModelViewSet)
router.register(r'LeadersCorner', LeadersCornerModelViewSet)
router.register(r'statuscategory', StatusCategoryModelViewSet)
router.register(r'suggestionfeedback', SuggestionFeedbackViewSet)


urlpatterns = [
    #user
    
    path('validate_deviceid/', DeviceValiDataionView.as_view(), name='validate_deviceid'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('validate_otp/', ValidateOTP.as_view()),
    path('getalluser/', UserRegistrationView.as_view(), name='getalluser'),
    path('updateuser/<int:id>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='updateuser'),
    path('getuser/<int:id>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='getuser'),
    path('deleteuser/<int:id>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='deleteuser'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('resend-otp/', ResendUserOtpAPIView.as_view(), name='change-password'),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    #banner   
    path('add_banners/', BanerAPIView.as_view(), name='addbanner'),
    path('category_banners/<int:category_id>/', GetCategoryBanners.as_view(), name='addbanner'),
    path('get_all_banners/', BanerAPIView.as_view(), name='getalluser'),
    path('get_banner/<int:id>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='get_banner'),
    path('update_banner/<int:id>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='updatebanner'),
    path('delete_banner/<int:id>/', BannerRetrieveUpdateDestroyAPIView.as_view(), name='deletebanner'),
    path('recent-banners/', RecentBanners.as_view(), name='recent-banners'),
    
    #category
    path('', include(router.urls)),
    #status
    path('status/', StatusList.as_view()),
    path('status/<int:pk>/', StatusDetail.as_view()),
    # admin side api 
    path('userregistrationadminview/',UserRegistrationAdminView.as_view()),
    path('login/', LoginadminView.as_view(), name='login'),
    # PremiumCalendarView
    path('premiumcalendar/',PremiumCalendarView.as_view()),
    path('premiumcalendarupdate/<int:id>/',PremiumCalendarView.as_view()),
    path('premiumcalendardelete/<int:id>/',PremiumCalendarView.as_view()),
    # PolicyDetailsView
    path('policydetails/',PolicyDetailsView.as_view()),
    path('policydetails/<int:pk>/', PolicyDetailsView.as_view(), name='policy-detail'),

    path('policydetailsupdate/<int:id>/',PolicyDetailsView.as_view()),
    path('policydetailsdelete/<int:id>/',PolicyDetailsView.as_view()),
    # gPolicyCalendarDetailsView get api
    path('PolicyCalendarDetailsView/',PolicyCalendarDetailsView.as_view()),
    path('PolicyCalendarDetailsViewone/',PolicyCalendarDetailsViewOne.as_view()),
]
