from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from todolist.forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from todolist.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


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


def signup(request):
    """
    회원 가입
    """
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = '당신의 ToDo List 계정을 활성화 하세요.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('회원가입을 마치려면 이메일을 확인해주세요.')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('확인해주셔서 감사합니다. 회원가입이 완료되었습니다.')
    else:
        return HttpResponse('계정 활성 링크가 유효하지 않습니다.')


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
