from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import BreastCancerResult,LungCancerResult,LeukemiaCancerResult
@admin.register(LungCancerResult)
class LungCancerResultAdmin(admin.ModelAdmin):
    list_display = ( 'user','id', 'air_pollution', 'alcohol_use', 'dust_allergy1', 'dust_allergy2',
                    'occupational_hazard1', 'occupational_hazard2', 'genetic_risk', 'chronic_lung_disease',
                    'balanced_diet', 'obesity', 'passive_smoker', 'chest_pain1', 'chest_pain2', 
                    'coughing_blood', 'fatigue', 'prediction','timestamp')
@admin.register(BreastCancerResult)
class BreastCancerResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'radius_mean', 'perimeter_mean', 'area_mean', 'concavity_mean', 'concave_points_mean', 'radius_worst', 'perimeter_worst', 'area_worst',  'concavity_worst', 'concave_points_worst', 'predicted_result', 'timestamp')

@admin.register(LeukemiaCancerResult)
class LeukemiaCancerResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'sv','prediction','timestamp')


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('email', 'username', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
