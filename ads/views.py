from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import Ad
from .forms import AdCreateForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        ads = Ad.objects.order_by('-created_at')[:3]
        return render(request, 'home.html', {'ads': ads})


class AdsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        q = request.GET.get('q')

        ads_qs = Ad.objects.all().order_by('-created_at')

        if q:
            ads_qs = ads_qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        paginator = Paginator(ads_qs, 10)  # 10 ta ad per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'ads_list.html', {
            'page_obj': page_obj,
            'q': q
        })


class AdsDetailView(View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        try:
            ad = Ad.objects.get(slug=slug)
            return render(request, 'ads_detail.html', {'ad': ad})
        except Ad.DoesNotExist:
            return render(request, 'ads_detail.html', {'error': 'Ad not found'})


class CreateAdsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = AdCreateForm()
        return render(request, 'ads_create.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AdCreateForm(request.POST)
        if form.is_valid():
            ad = form.save()
            return redirect('ads_detail', slug=ad.slug)

        return render(request, 'ads_create.html', {'form': form})


class ContactAdminView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'contact_admin.html')


class AdsCleanupView(View):
    def get(self, request):
        expired_date = timezone.now() - timedelta(days=30)

        deleted_count, _ = Ad.objects.filter(
            created_at__lt=expired_date
        ).delete()

        return HttpResponse(
            f"""
            <h2>Cleanup completed</h2>
            <p>{deleted_count} expired ads have been deleted.</p>
            <a href="/ads/">Back to ads list</a>
            """,
            content_type="text/html"
        )