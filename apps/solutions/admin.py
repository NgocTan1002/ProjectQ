from django.contrib import admin
from django.utils.html import format_html
from .models import Solution, SolutionCategory, SolutionProduct, ArchitectureBlock, WorkflowStep, CustomerCase

class SolutionProductInline(admin.TabularInline):
    model = SolutionProduct
    extra = 2
    autocomplete_fields = ['product']
    fields = ['product', 'is_featured', 'role_description', 'sort_order']

class ArchitectureBlockInline(admin.StackedInline):
    model = ArchitectureBlock
    extra = 1
    fields = ['title', 'description', 'image', 'sort_order']
    verbose_name = "Khối kiến trúc"
    verbose_name_plural = "Các khối kiến trúc"

class WorkflowStepInline(admin.TabularInline):
    model = WorkflowStep
    extra = 3
    fields = ['step_number', 'title', 'description', 'icon_class', 'image']
    verbose_name = "Bước quy trình"
    verbose_name_plural = "Các bước quy trình"

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 
                    'title',
                    'solution_category',
                    'status',
                    'is_featured',
                    'view_count'
                    ]
    list_display_links = ['thumbnail_preview', 'title']
    list_filter = ['status', 'solution_category', 'is_featured']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    list_select_related = ['solution_category']
    save_on_top = True

    inlines = [SolutionProductInline, ArchitectureBlockInline, WorkflowStepInline]

    fieldsets = [
        ('Thông tin cơ bản', {
            'fields': ['title', 'subtitle', 'slug', 'solution_category']
        }),

        ('Hình ảnh & Media', {
            'fields': ['thumbnail', 'hero_image', 'hero_video_url']
        }),

        ('Nội dung chính', {
            'fields': ['short_description', 'overview'],
            'classes': ['wide']
        }),

        ('Vấn đề khách hàng', {
            'fields': ['pain_points'],
            'classes': ['collapse']
        }),

        ('Lợi ích', {
            'fields': ['benefits'],
            'classes': ['collapse']
        }),

        ('Quy trình hoạt động', {
            'fields': ['workflow_title', 'workflow_description']
        }),

        ('Kêu gọi hành động (CTA)', {
            'fields': [
                'cta_title',
                'cta_primary_text', 'cta_primary_url',
                'cta_secondary_text', 'cta_secondary_url'
            ]
        }),

        ('Xuất bản', {
            'fields': ['status', 'published_at', 'is_featured', 'sort_order']
        }),
    ]

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;" />', obj.thumbnail.url)
        return '-'
    thumbnail_preview.short_description = ''

@admin.register(SolutionCategory)
class SolutionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'sort_order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'sort_order']
 
 
@admin.register(CustomerCase)
class CustomerCaseAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'solution', 'industry', 'country', 'status']
    list_filter = ['status', 'industry']
    prepopulated_fields = {'slug': ('company_name',)}