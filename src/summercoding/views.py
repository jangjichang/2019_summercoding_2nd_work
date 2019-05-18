from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class HomeView(TemplateView):
    """
    Home Page를 보여주는 TemplateView
    """
    template_name = 'home.html'


class LoginRequiredMixin:
    """
    사용자의 Login 여부 확인을 위한 View
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UserCreateView(CreateView):
    """
    회원 가입
    """
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    """
    회원 가입 완료 페이지
    """
    template_name = 'registration/register_done.html'


class PageNotFound(TemplateView):
    """
    404 Page Not Found error 발생 시 보여주는 View
    """
    template_name = 'error/page_not_found.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super(TemplateView, self).render_to_response(context, **response_kwargs)


class ServerErrorPage(TemplateView):
    """
    500 Internal Server error 발생 시 보여주는 View
    """
    template_name = 'error/server_error_page.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 500
        return super(TemplateView, self).render_to_response(context, **response_kwargs)
