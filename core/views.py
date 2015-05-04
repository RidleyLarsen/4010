from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView, DetailView, TemplateView
from django.http import HttpResponseRedirect

from .models import Quiz, QuizAnswer, QuizQuestion


class HomepageView(TemplateView):
    template_name = "base_home.html"

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['quizzes'] = Quiz.objects.all()
        return context


class QuizView(DetailView):
    template_name = "quiz/take_quiz.html"
    model = Quiz


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')


QuestionFormSet = inlineformset_factory(Quiz, QuizQuestion, fields=('quiz', 'question'))
AnswerFormSet = inlineformset_factory(QuizQuestion, QuizAnswer, fields=('question', 'text', 'correct'))


class QuizCreateView(CreateView):
    template_name = "quiz/create.html"
    form_class = QuizForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answer_form = AnswerFormSet()
        question_form = QuestionFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  answer_form=answer_form,
                                  question_form=question_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        answer_form = AnswerFormSet(self.request.POST)
        question_form = QuestionFormSet(self.request.POST)
        if (
            form.is_valid() and
            answer_form.is_valid() and
            question_form.is_valid()
        ):
            return self.form_valid(form, answer_form, question_form)
        else:
            return self.form_invalid(form, answer_form, question_form)

    def form_valid(self, form, answer_form, question_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        answer_form.instance = self.object
        answer_form.save()
        question_form.instance = self.object
        question_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, answer_form, question_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  answer_form=answer_form,
                                  question_form=question_form))
