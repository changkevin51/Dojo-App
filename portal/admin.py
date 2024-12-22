from django.contrib import admin
from .models import *
from django import forms
from django.core.exceptions import ValidationError

# Custom form for the Registration model
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['student', 'unit', 'session']

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        unit = cleaned_data.get('unit')
        session = cleaned_data.get('session')

        # Check if the student is already registered for the same unit and session
        if Registration.objects.filter(student=student, unit=unit, session=session).exists():
            raise ValidationError(f"{student.username} is already registered for {unit.name} in the {session.name} session.")
        
        return cleaned_data


# Inline admin form for Registration
class RegistrationInline(admin.TabularInline):
    model = Registration
    form = RegistrationForm
    extra = 1  # How many empty rows to show by default in the inline
    fields = ['student', 'session']  # Only show student and session here

    def get_queryset(self, request):
        # Show only registrations that are not already assigned to the unit
        queryset = super().get_queryset(request)
        return queryset.filter(unit__isnull=True)


# Register Unit model and include the RegistrationInline for adding students
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'teacher']
    search_fields = ['name', 'code']
    list_filter = ['teacher']
    inlines = [RegistrationInline]  # Include the inline registration form


# Register Registration model with additional behavior (custom delete handling)
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    form = RegistrationForm
    list_display = ['student', 'unit', 'session']
    search_fields = ['student__username', 'unit__name', 'session__name']
    list_filter = ['unit', 'session']
    list_select_related = ['student', 'unit', 'session']
    raw_id_fields = ['student', 'unit', 'session']  # Use raw_id_fields for better performance

    # Optionally, restrict deletion if related objects exist
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['student']  # Make the student field readonly once the registration is created
        return []

    # Customize the delete behavior
    def delete_queryset(self, request, queryset):
        for registration in queryset:
            if registration.student:
                if Submission.objects.filter(student=registration.student).exists():
                    raise ValidationError(f"Cannot delete registration for {registration.student.username} as they have related submissions.")
        super().delete_queryset(request, queryset)

    # Optional: Add a custom message when preventing deletion
    def has_delete_permission(self, request, obj=None):
        if obj and Submission.objects.filter(student=obj.student).exists():
            self.message_user(request, f"Cannot delete registration for {obj.student.username}: Related submissions exist.", level='error')
            return False
        return True


# Register other models
admin.site.register(CustomUser)
admin.site.register(Session)
admin.site.register(Assignment)
admin.site.register(Submission)
