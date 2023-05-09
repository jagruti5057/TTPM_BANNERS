from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, password2=None,**kwargs):
        """
        Creates and saves a User with the given email, name and password.
        """
        
        if not email:
            raise ValueError('Users must have an email address')
        if 'is_admin' in kwargs:
            admin_status=kwargs['is_admin']
        else:
            admin_status=False
        
        if 'phone_number' in kwargs:
            phone_number=kwargs['phone_number']
        else:
            phone_number=None
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin=admin_status,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# /home/koli/Documents/banner_project/banners_01/ba nners/banner_apis/mediafiles/bannerimages/Screenshot_from_2023-01-19_12-28-06.png
#custome user
class Users(AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    phone_number=models.CharField(max_length=10,unique=True)
    device_id=models.CharField(max_length=20,null=True,blank=True,unique=True)
    profile_image = models.ImageField(upload_to='profileimages/', blank=True, null=True)
    full_name=models.CharField(max_length=60,null=True,blank=True)
    designation=models.CharField(max_length=20,null=True,blank=True)
    date_of_birth=models.DateTimeField(null=True,blank=True)
    date_of_joining=models.DateTimeField(null=True,blank=True)
    whatsapp_mobile=models.CharField(max_length=10,null=True,blank=True)
    pincode=models.CharField(max_length=6,null=True,blank=True)
    state=models.CharField(max_length=20,null=True,blank=True)
    city=models.CharField(max_length=30,null=True,blank=True)
    lic_brach_number=models.CharField(max_length=10,null=True,blank=True)
    branch_name=models.CharField(max_length=50,null=True,blank=True)
    website=models.CharField(max_length=40,null=True,blank=True)
    social_caption=models.CharField(max_length=60,null=True,blank=True)
    user_category=models.CharField(max_length=25,null=True,blank=True)
    club_member=models.CharField(max_length=30,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True,blank=True)
    is_mdrt = models.BooleanField(default=False)
    business_profile=models.CharField(max_length=20,null=True,blank=True)
    header_image = models.ImageField(default="logo.jpg",upload_to='headerimages/', blank=True, null=True)
    otp = models.CharField(max_length = 9, blank = True, null= True)
    count = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Categories(models.Model):

    name = models.CharField(unique=True,max_length=50,null=True,blank=True) 
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
     return str(self.id)

class Banners(models.Model):
    banners_choice = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
      )
    type_of_banner = models.CharField(max_length=10, choices=banners_choice,null=True,blank=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    banner_img = models.ImageField(upload_to='bannerimages/', blank=True, null=True)
    banner_url = models.CharField(max_length=20,null=True,blank=True)
    is_frame=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class AdminBanners(models.Model):
    banner_image=models.ImageField(upload_to='admin_banners/')
    
class NewsArticals(models.Model):
    DOCUMENT_CHOICES = (
        ('N', 'News'),
        ('A', 'Articals'),
      )
    type_of_document = models.CharField(max_length=1, choices=DOCUMENT_CHOICES)
    document=models.TextField()
    channel_name=models.CharField(max_length=15,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title =models.CharField(max_length=50,null=True,blank=True)
    articals_img = models.ImageField(upload_to='articalsimages/', blank=True, null=True)

class StatusCategory(models.Model):
    status_name=models.CharField(max_length=50,null=True,blank=True)
    
class Status(models.Model):
    Status_Choice= (
        ('Leaders corner', 'Leaders corner'),
        ('Greeting', 'Greeting'),
        ('Concept', 'Concept'),
        ('AllLC', 'AllLC'),
        ('Daily motivation', 'Daily motivation'),
        ('Sales tip', 'Sales tip'),
        ('AllG', 'AllG'),
        ('Special days', 'Special days'),
        ('Festivals', 'Festivals'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
        ('AllC', 'AllC'),
        ('General', 'General'),
        ('Retirement', 'Retirement'),
        ('Health', 'Health'),
      )
    type_of_status=models.CharField(max_length=30, choices=Status_Choice)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content = models.TextField()
    media = models.FileField(upload_to='status_media/')
    file = models.FileField(upload_to='music_files/',null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_image= models.BooleanField(default=False)

class Liccirclars(models.Model):
    # Category_Choice= (
    #     ('endownment plan', 'endownment plan'),
    #     ('money back plan', 'money back plan'),
    #     ('children single premimum plan', 'children single premimum plan'),
    #     ('term insurance plan', 'term insurance plan'),
    #     ('health plan', 'health plan'),
    #     ('pension plan', 'pension plan'),
    #     ('underwriting', 'underwriting'),
    #     ('genral', 'genral'),
    #     ('ulip', 'ulip'),
    #     ('old circulars', 'old circulars'),
    #   )
    # type_of_category=models.CharField(max_length=30, choices=Category_Choice)
    formname= models.CharField(max_length=50,null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='lic_pdf_files/',null=True,blank=True)
   
class Forms(models.Model):
    formsname= models.CharField(max_length=50,null=True,blank=True) 
    file = models.FileField(upload_to='form_pdf_files/',null=True,blank=True)
    formno = models.CharField(max_length = 20, blank = True, null= True)

class ProfileFrame(models.Model):
    Frame_Choice = (
        ('Withframe', 'Withframe'),
        ('Withoutframe', 'Withoutframe'),
        ('Profileframe', 'Profileframe'),

      )
    type_of_frames=models.CharField(max_length=30, choices=Frame_Choice)
    frame_image = models.ImageField(upload_to='frame_image/', blank=True, null=True)
    is_frame= models.BooleanField(default=False)

class AudioVideo(models.Model):
    AV_Choice = (
        ('Audio', 'Audio'),
        ('Video', 'Video'),
      )
    type_of_av=models.CharField(max_length=50, choices=AV_Choice)
    title =models.CharField(max_length=50,null=True,blank=True)
    file = models.FileField(upload_to='audio_video/',null=True,blank=True)
    description=models.TextField()
    image = models.ImageField(upload_to='frame_image/', blank=True, null=True)

# this model for licplans
# class PlanCategory(models.Model):
#     plans_name =models.CharField(max_length=50,null=True,blank=True)

class licplans(models.Model):
    Category_Choice= (
        ('endownment plan', 'endownment plan'),
        ('money back plan', 'money back plan'),
        ('children single premimum plan', 'children single premimum plan'),
        ('term insurance plan', 'term insurance plan'),
        ('health plan', 'health plan'),
        ('pension plan', 'pension plan'),
        ('underwriting', 'underwriting'),
        ('genral', 'genral'),
        ('ulip', 'ulip'),
        ('old circulars', 'old circulars'),
      )
    category=models.CharField(max_length=30, choices=Category_Choice)
    lic_banners = models.ImageField(upload_to='lic_banners/', blank=True, null=True)
    is_frame= models.BooleanField(default=False)


class PremiumCalendar(models.Model):
    user_type= (
        ('head', 'head'),
        ('member', 'member'),
      )
    type_of_user=models.CharField(max_length=30, choices=user_type)
    username = models.CharField(max_length=50,null=True,blank=True) 
    mobile_no = models.CharField(max_length=10,unique=True)
    date_of_birth=models.DateTimeField(null=True,blank=True)

class PolicyDetails(models.Model):
    type_of_user = models.ForeignKey(PremiumCalendar, on_delete=models.CASCADE,null=True,blank=True)
    insurance= (
        ('Life Insurance', 'Life Insurance'),
        ('Health Insurance', 'Health Hnsurance'),
        ('General Insurance', 'General Insurance'),
      )
    type_of_insurance=models.CharField(max_length=30, choices=insurance)
    product_name = models.CharField(max_length=50,null=True,blank=True) 
    policy_number = models.CharField(max_length=50,null=True,blank=True) 
    sum_assured = models.CharField(max_length=10,unique=True)
    mode = (
        ('yearly', 'yearly'),
        ('quaterly', 'quaterly'),
        ('monthly', 'monthly'),
        ('single', 'single'),
        )
    type_of_mode=models.CharField(max_length=30, choices=mode)
    term = models.CharField(max_length=50,null=True,blank=True) 
    ppt = models.CharField(max_length=50,null=True,blank=True) 
    policy_start_due = models.DateTimeField(null=True,blank=True)
    policy_next_due = models.DateTimeField(null=True,blank=True)
    premium = models.CharField(max_length=50,null=True,blank=True) 


class MarketingCategory(models.Model):
    name =models.CharField(max_length=50,null=True,blank=True)


class MarketingSms(models.Model):
    Category_Choice= (
        ('Greeting SMS', 'Greeting SMS'),
        ('Recruitment', 'Recruitment'),
        ('Reminders', 'Reminders'),
        ('General', 'General'),
        ('Smart Combo Children', 'Smart Combo Children'),
        ('Smart Combo General', 'Smart Combo General'),
        ('Smart Combo HNI', 'Smart Combo HNI'),
        ('Smart Combo Retirement', 'Smart Combo Retirement'),
      )
    marketingcategory=models.CharField(max_length=30, choices=Category_Choice)
    title =models.CharField(max_length=50,null=True,blank=True)
    description=models.TextField()

class MixPlanCategory(models.Model):
    name =models.CharField(max_length=50,null=True,blank=True)

class MixPlan(models.Model):
    Plan_Choice= (
        ('Retirement', 'Retirement'),
        ('Children', 'Children'),
        ('General', 'General'),
        ('HNI', 'HNI'),
      )
    MixPlanCategory=models.CharField(max_length=30, choices=Plan_Choice)
    mixplan_banners = models.ImageField(upload_to='mixplan_banners /', blank=True, null=True)
    is_frame= models.BooleanField(default=False)

class LeadersCornerCategory(models.Model):
    name =models.CharField(max_length=50,null=True,blank=True)

class LeadersCorner(models.Model):

    leaders_Choice= (
        ('Agency Marketing', 'Agency Marketing'),
        ('Appreciation', 'Appreciation'),
        ('Success Stories', 'Success Stories'),
        ('Sales Tip', 'Sales Tip'),
        ('Certificate', 'Certificate'),

      )
    leaderscategory=models.CharField(max_length=30, choices=leaders_Choice)
    leader_banners = models.ImageField(upload_to='leader_banners /', blank=True, null=True)
    is_frame= models.BooleanField(default=False)

class SuggestionFeedback(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    suggestion = models.TextField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.full_name
