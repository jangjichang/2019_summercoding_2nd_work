from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from summercoding.views import LoginRequiredMixin
from .models import Work, Card
from .forms import CardForm, WorkForm, CardInlineFormSet

import datetime
# Create your views here.


class WorkCardLV(LoginRequiredMixin, ListView):
    """
    사용자의 TODO (Work model)를 보여주는 ListView
    """
    model = Work

    def get_queryset(self):
        return Work.objects.filter(owner=self.request.user)

    """마감기한이 지난 TODO (Work, Card model)를 context 변수에 update 하는 메소드"""
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkCardLV, self).get_context_data(**kwargs)
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        deadline_over_works = Work.objects.filter(owner=self.request.user).filter(deadline__lte=today).filter(done=False)
        deadline_over_cards = Card.objects.filter(owner=self.request.user).filter(deadline__lte=today).filter(done=False)
        if deadline_over_works:
            context['deadline_over_works'] = deadline_over_works
        if deadline_over_cards:
            context['deadline_over_cards'] = deadline_over_cards
        return context


class WorkCreateView(LoginRequiredMixin, CreateView):
    """
    사용자의 TODO (Work model)를 만드는 CreateView
    CardInlineFormset을 이용하여 Work와 Card를 한 페이지에서 생성 가능
    """
    model = Work
    form_class = WorkForm
    success_url = reverse_lazy('todolist:index')

    def get_context_data(self, **kwargs):
        context = super(WorkCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = CardInlineFormSet(self.request.POST)
            return context
        context['formset'] = CardInlineFormSet()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        for cardform in formset:
            cardform.instance.owner = self.request.user
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect('todolist:index')
        return self.render_to_response(self.get_context_data(form=form))


class WorkUpdateView(LoginRequiredMixin, UpdateView):
    """
    사용자의 TODO (Work model)를 수정하는 UpdateView
    """
    model = Work
    form_class = WorkForm
    success_url = reverse_lazy('todolist:index')

    """사용자가 소유하지 않은 Work를 수정하는 url 접근시 404 error 발생"""
    def get_queryset(self):
        work_update_obj = Work.objects.filter(owner=self.request.user).filter(id=self.kwargs['pk'])
        return work_update_obj

    def get_context_data(self, **kwargs):
        context = super(WorkUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = CardInlineFormSet(self.request.POST, instance=self.object)
            return context
        context['formset'] = CardInlineFormSet(instance=self.object)
        context['formset_id'] = list(Card.objects.filter(owner=self.request.user).filter(work=self.kwargs['pk']).values_list('id', flat=True))
        print(context['formset_id'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        for cardform in formset:
            cardform.instance.owner = self.request.user
            cardform.instance.work = Work.objects.get(id=self.kwargs['pk'])
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect('todolist:index')
        return self.render_to_response(self.get_context_data(form=form))


class WorkDeleteView(LoginRequiredMixin, DeleteView):
    """
    사용자의 TODO (Work model)를 삭제하는 DeleteView
    """
    model = Work
    success_url = reverse_lazy('todolist:index')

    """사용자가 소유하지 않은 Work를 삭제하는 url 접근시 404 error 발생"""
    def get_queryset(self):
        work_delete_obj = Work.objects.filter(owner=self.request.user).filter(id=self.kwargs['pk'])
        return work_delete_obj


class CardCreateView(LoginRequiredMixin, CreateView):
    """
    사용자의 TODO (Card model)를 생성하는 CreateView
    """
    model = Card
    form_class = CardForm
    success_url = reverse_lazy('todolist:index')

    """사용자가 소유하지 않은 Work에 TODO를 생성하는 url 접근시 404 error 발생"""
    def get_context_data(self, **kwargs):
        work = get_object_or_404(Work, id=self.kwargs['fk'])
        if str(self.request.user) != str(work.owner):
            raise Http404
        return super(CardCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.work = Work.objects.get(id=self.kwargs['fk'])
        return super(CardCreateView, self).form_valid(form)


class CardUpdateView(LoginRequiredMixin, UpdateView):
    """
    사용자의 TODO (Card model)를 수정하는 UpdateView
    """
    model = Card
    form_class = CardForm
    success_url = reverse_lazy('todolist:index')

    """사용자가 소유하지 않은 Card를 수정하는 url 접근시 404 error 발생"""
    def get_context_data(self, **kwargs):
        if self.request.user != Card.objects.get(id=self.kwargs['pk']).owner:
            raise Http404
        context = super(CardUpdateView, self).get_context_data(**kwargs)
        return context


class CardDeleteView(LoginRequiredMixin, DeleteView):
    """
    사용자의 TODO (Card model)를 삭제하는 DeleteView
    """
    model = Card
    success_url = reverse_lazy('todolist:index')

    """사용자가 소유하지 않은 Card를 삭제하는 url 접근시 404 error 발생"""
    def get_context_data(self, **kwargs):
        if self.request.user != Card.objects.get(id=self.kwargs['pk']).owner:
            raise Http404
        context = super(CardDeleteView, self).get_context_data(**kwargs)
        return context
