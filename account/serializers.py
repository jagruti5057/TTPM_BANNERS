from rest_framework import serializers
from account.models import * #Users,Categories,Banners,AdminBanners,NewsArticals,Status,Liccirclars,Forms,LeadersCorner,StatusCategory,licplans,MixPlan,MixPlanCategory,LeadersCornerCategory,ProfileFrame,MixPlan,MixPlanCategory,MarketingSms,AudioVideo,PremiumCalendar,PolicyDetails,MarketingCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'email', 'phone_number', 'profile_image', 'full_name', 'designation', 'date_of_birth', 'date_of_joining', 'whatsapp_mobile', 'pincode', 'state', 'city', 'lic_brach_number', 'branch_name', 'website', 'social_caption', 'user_category', 'club_member', 'gender', 'is_mdrt', 'business_profile', 'header_image', 'otp', 'count', 'is_active', 'is_admin', 'created_at', 'updated_at')
        
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','full_name','designation','date_of_birth' ,'date_of_joining','phone_number','whatsapp_mobile','email','profile_image','pincode','state','city','lic_brach_number','branch_name','website','social_caption','user_category','club_member','gender','is_mdrt','business_profile','header_image']

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                raise serializers.ValidationError({"password": "You cant change password."})
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    

class ChangePasswordSerializer(serializers.Serializer):
    model = Users

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Users
        fields = ['password','password2']
       
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password is not same")
        
        return attrs
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields=['id','name']
        
class BanerSerializers(serializers.ModelSerializer):
    class Meta:
        model=Banners
        fields=['id','category','banner_img','is_frame','type_of_banner']
        
class RecentBanerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'
    
class AdminBannersSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminBanners
        fields=['id','banner_image']
        

class NewsArticalSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsArticals
        fields=['id','type_of_document','document','title','channel_name','articals_img','timestamp']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id',  'content', 'media', 'file','type_of_status','timestamp','is_image')

class LiccirclarsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Liccirclars
        fields=['id','formname','created_at',"file"]

class LicbannersSerializer(serializers.ModelSerializer):
    class Meta:
        model=licplans
        fields=['id','category','lic_banners','is_frame']

class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Forms
        fields=['id','formsname',"file","formno"]

class ProfileFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProfileFrame
        fields=['id','type_of_frames',"frame_image","is_frame"]


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioVideo
        fields = ['id', 'type_of_av', 'title', 'file', 'description', 'image']

    def validate_image(self, value):
        """
        Check if image is null, and set a default value if it is.
        """
        if not value:
            return "NA"
        return value


# class PlanCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model=PlanCategory
#         fields=['id','plans_name']

class StatusCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=StatusCategory
        fields=['id','status_name']

class PremiumCalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = PremiumCalendar
        fields = "__all__"

class PolicyDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PolicyDetails
        fields = "__all__"


class MarketingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=MarketingCategory
        fields=['id','name']


class PremiumCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumCalendar
        fields = ["id","type_of_user","username","mobile_no","date_of_birth"]

class PremiumCalendarGetSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.SerializerMethodField()
    def get_date_of_birth(self, obj):
        if obj.date_of_birth!="None" and  obj.date_of_birth!= None:
            date = obj.date_of_birth.date()
            return str(date)
    class Meta:
        model = PremiumCalendar
        fields = ["id","type_of_user","username","mobile_no","date_of_birth"]

class PolicyDetailsSerializer(serializers.ModelSerializer):
    type_of_user = serializers.SerializerMethodField(source='type_of_user.username')
    class Meta:
        model = PolicyDetails
        fields = ['id','type_of_user',"type_of_insurance","product_name","policy_number","sum_assured","type_of_mode","term","ppt","policy_start_due","policy_next_due","premium"]
    def get_type_of_user(self, obj):
        # print(obj.type_of_user.username)
        if obj.type_of_user!="None" and  obj.type_of_user!= None:
            return str(obj.type_of_user.username)

class PolicyDetailsGetSerializer(serializers.ModelSerializer):
    type_of_user = serializers.SerializerMethodField(source='type_of_user.username')
    policy_start_due = serializers.SerializerMethodField()
    policy_next_due = serializers.SerializerMethodField()

    def get_policy_start_due(self, obj):
        date = obj.policy_start_due.date()
        return str(date)
    def get_policy_next_due(self, obj):
        date = obj.policy_next_due.date()
        return str(date)
    class Meta:
        model = PolicyDetails
        fields = ['id','type_of_user',"type_of_insurance","product_name","policy_number","sum_assured","type_of_mode","term","ppt","policy_start_due","policy_next_due","premium"]
    def get_type_of_user(self, obj):
        if obj.type_of_user!="None" and  obj.type_of_user!= None:
            return str(obj.type_of_user.username)    

class PolicdetailsCalendarSerializer(serializers.ModelSerializer):
    type_of_user = serializers.SerializerMethodField()
    policy_next_due = serializers.SerializerMethodField()

    def get_type_of_user(self, obj):
        if obj.type_of_user!="None" and  obj.type_of_user!= None:
            return str(obj.type_of_user.username)
    
    def get_policy_next_due(self, obj):
        if obj.policy_next_due!="None" and  obj.policy_next_due!= None:
            return str(obj.policy_next_due.date())

    class Meta:
        model = PolicyDetails
        fields = ['id','type_of_user', 'policy_number', 'product_name', 'sum_assured', 'policy_next_due']

class ChildSerializer(serializers.ModelSerializer):
    policy_next_due = serializers.SerializerMethodField()
    def get_policy_next_due(self, obj):
        date = obj.policy_next_due.date()
        return str(date)
    class Meta:
        model = PolicyDetails
        fields = ['policy_number', 'policy_next_due']

class ParentSerializer(serializers.ModelSerializer):
    policydetails_set = ChildSerializer(many=True, read_only=True, source='policydetails_set.all')
    date_of_birth = serializers.SerializerMethodField()
    def get_date_of_birth(self, obj):
        if obj.date_of_birth!="None" and  obj.date_of_birth!= None:
            date = obj.date_of_birth.date()
            return str(date)
    class Meta:
        model = PremiumCalendar
        fields = ['id', 'username', 'mobile_no', 'date_of_birth', 'policydetails_set']


class MarketingSmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketingSms
        fields = "__all__"

class MixPlanCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MixPlanCategory
        fields = "__all__"

class MixPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = MixPlan
        fields = "__all__"

class LeadersCornerCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = LeadersCornerCategory
        fields = "__all__"

class LeadersCornerSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeadersCorner
        fields = "__all__"

class SuggestionFeedbackSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return str(obj)

    def get_created_at(self, obj):
        date = obj.created_at.date()
        return str(date)
        
    class Meta:
        model = SuggestionFeedback
        fields = ['id', 'user','suggestion', 'feedback', 'created_at']