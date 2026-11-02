from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField

class CoachPage(Page):
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name ="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("photo"),
    ]

class CoursPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        context["cours_list"] = Cours.objects.all()
        return context

@register_snippet
class Cours(models.Model):
    nom = models.CharField(max_length=100)
    horaire = models.CharField(max_length=100, blank=True)
    niveau = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel("nom"),
        FieldPanel("horaire"),
        FieldPanel("niveau"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.nom

class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )

class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thankyoutext = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FieldPanel("thankyoutext"),
        FieldPanel("to_address"),
        FieldPanel("from_address"),
        FieldPanel("subject"),
    ]
