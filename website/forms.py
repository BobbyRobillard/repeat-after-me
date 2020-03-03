from django import forms

# class QueueForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super(QueueForm, self).__init__(*args, **kwargs)
#         makes = Lense.objects.all().values_list('make', flat=True).distinct()
#         make_choices = [(make, make) for make in makes]
#         self.fields['make'] = forms.ChoiceField(choices=make_choices)
#
#         models = Lense.objects.all().values_list('model', flat=True).distinct()
#         model_choices = [(model, model) for model in models]
#         self.fields['model'] = forms.ChoiceField(choices=model_choices)
#
#         self.fields['type'] = forms.ChoiceField(choices=type_choices)
#         self.fields['custom_size'] = forms.ModelChoiceField(queryset=StandardBandit.objects.all(), required=False)
#
#     def clean(self):
#         data = self.cleaned_data
#         if not len(Lense.objects.filter(make=data['make'], model=data['model'], type=data['type'])) == 1:
#             raise forms.ValidationError({"type": "Error, this lense does not have this type!"})
